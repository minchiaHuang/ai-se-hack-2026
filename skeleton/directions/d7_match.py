"""Direction 7, line B - which representative jobs fit the evidenced units.

A plain module, not a pipeline direction: it runs after a human has accepted
the evidence pack, so it only ever sees units that already point at a line of
the transcript.

The fit is a count of evidenced units, never a percentage or a score, because
it describes a job against the evidence, not the person. It is never shown to
an employer, which is why resume_for() leaves it out.
"""
import json
from pathlib import Path

REFERENCE = Path(__file__).resolve().parent.parent / "demo_data" / "reference"
# Read directly rather than through skeleton.core.registry, which is being
# written in parallel; both read the same file, so they cannot disagree.
OCCUPATIONS = REFERENCE / "occupations.json"
JOBS = REFERENCE / "jobs.json"

COURSE_NOTE = "Gap training through a Registered Training Organisation"


def _occupations():
    return json.loads(OCCUPATIONS.read_text(encoding="utf-8"))


def load_jobs():
    return json.loads(JOBS.read_text(encoding="utf-8"))


def _units_by_code():
    """Every seeded unit, with the qualification it belongs to."""
    units = {}
    for occ in _occupations().values():
        qual = occ["qualification"]
        for unit in occ["units"]:
            units[unit["code"]] = {"title": unit["title"],
                                   "qualification": f"{qual['code']} {qual['title']}"}
    return units


def _evidenced(evidenced_units):
    """A unit with no source is a claim, not evidence, so it does not count."""
    return {u["code"]: [list(s) for s in u["sources"]]
            for u in evidenced_units if u.get("sources")}


def match_jobs(occupation, evidenced_units):
    if occupation not in _occupations():
        raise KeyError(f"{occupation}: not a seeded occupation")
    units = _units_by_code()
    evidence = _evidenced(evidenced_units)
    jobs = []
    for job in load_jobs():
        if job["occupation"] != occupation:
            continue
        required = job["required_units"]
        matched = [{"code": c, "title": units[c]["title"], "sources": evidence[c]}
                   for c in required if c in evidence]
        missing = [{"code": c, "title": units[c]["title"]}
                   for c in required if c not in evidence]
        jobs.append({"id": job["id"], "title": job["title"], "setting": job["setting"],
                     "note": job["note"], "matched": matched, "missing": missing,
                     "fit": f"{len(matched)} of {len(required)} required units evidenced"})
    # Stable sort: ties keep the order jobs.json lists them in.
    jobs.sort(key=lambda j: -len(j["matched"]))
    return jobs


def courses_for(jobs):
    """The RPL gap statement: missing units, and which jobs each would open.

    A list of units, never a judgement about the person.
    """
    units = _units_by_code()
    courses = {}
    for job in jobs:
        for unit in job["missing"]:
            course = courses.setdefault(unit["code"], {
                "code": unit["code"], "title": unit["title"],
                "qualification": units[unit["code"]]["qualification"],
                "for_jobs": [], "note": COURSE_NOTE})
            course["for_jobs"].append(job["id"])
    return sorted(courses.values(), key=lambda c: -len(c["for_jobs"]))


def _timestamp(locator):
    return locator[2:] if locator.startswith("t=") else locator


def resume_for(job, evidenced_units, transcript):
    """A plain-text draft for the jobseeker to check, built without a model.

    Only what the person said and what they evidenced goes in. No name,
    employer, date or fit is written, because none of them were evidenced and
    a guessed one on a resume is a false claim made in the person's name.
    """
    units = _units_by_code()
    evidence = _evidenced(evidenced_units)
    lines = {line["t"]: line["en"] for line in transcript}

    cited = set()
    skills = []
    qualifications = []
    for code, sources in evidence.items():
        if code not in units:
            continue
        stamps = [_timestamp(loc) for label, loc in sources if label == "transcript"]
        cited.update(t for t in stamps if t in lines)
        skills.append(f"- {code} {units[code]['title']} (described at {', '.join(stamps)})")
        if units[code]["qualification"] not in qualifications:
            qualifications.append(units[code]["qualification"])

    out = [f"DRAFT RESUME - for: {job['title']}, {job['setting']}",
           "", "WORK EXPERIENCE (the jobseeker's own account, translated)"]
    out += [f"- {lines[t]} [transcript {t}]" for t in sorted(cited)]
    out += ["", "SKILLS MAPPED TO AUSTRALIAN UNITS OF COMPETENCY"] + skills
    out += ["", "QUALIFICATIONS"]
    out += [f"- {q}: Recognition of Prior Learning in progress, not yet assessed"
            for q in qualifications]
    out += ["", "Name, contact details, employers and dates are for the jobseeker to add."]
    return "\n".join(out)
