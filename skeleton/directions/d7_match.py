"""Direction 7, line B - which representative jobs fit the evidenced units.

A plain module, not a pipeline direction: it runs after a human has accepted
the evidence pack, so it only ever sees units that already point at a line of
the transcript.

The fit this module returns is a count of evidenced units and nothing else:
"N of M required units evidenced". The only percentage allowed anywhere, the
page's coverage ring included, is evidenced required units divided by required
units, worked out from those same two counts. A similarity or match score, or
a "good match" / "strong match" style label about the person, is still
forbidden: the fit describes a job against the evidence, not the person. It is
never shown to an employer, which is why resume_for() leaves it out.
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
    jobs = [_counted(job, units, evidence) for job in load_jobs()
            if job["occupation"] == occupation]
    # Stable sort: ties keep the order jobs.json lists them in.
    jobs.sort(key=lambda j: -len(j["matched"]))
    return jobs


def _counted(job, units, evidence):
    required = job["required_units"]
    matched = [{"code": c, "title": units[c]["title"], "sources": evidence[c]}
               for c in required if c in evidence]
    missing = [{"code": c, "title": units[c]["title"]}
               for c in required if c not in evidence]
    return {"id": job["id"], "title": job["title"], "setting": job["setting"],
            "location": job["location"], "employment_type": job["employment_type"],
            "level": job["level"], "shift": job["shift"],
            "note": job["note"], "matched": matched, "missing": missing,
            "fit": f"{len(matched)} of {len(required)} required units evidenced"}


def all_jobs(occupation, evidenced_units):
    """Every job in jobs.json, counted the same way, for a board that hides nothing.

    The occupation's jobs come first in match_jobs() order; the rest follow,
    best evidenced first. They are counted, not assumed to be 0, so a unit two
    occupations share would show on both. Each job says which occupation it is
    for, so the page can mark the others honestly instead of dropping them.
    """
    occupations = _occupations()
    if occupation not in occupations:
        raise KeyError(f"{occupation}: not a seeded occupation")
    units = _units_by_code()
    evidence = _evidenced(evidenced_units)
    ours, others = [], []
    for job in load_jobs():
        counted = _counted(job, units, evidence)
        counted.update({"occupation": job["occupation"],
                        "occupation_label": occupations[job["occupation"]]["label"],
                        "for_occupation": job["occupation"] == occupation})
        (ours if counted["for_occupation"] else others).append(counted)
    # Stable sorts: ties keep the order jobs.json lists them in.
    ours.sort(key=lambda j: -len(j["matched"]))
    others.sort(key=lambda j: -len(j["matched"]))
    return ours + others


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


RPL_STATUS = "Recognition of Prior Learning in progress, not yet assessed"
TO_ADD = "Name, contact details, employers and dates are for the jobseeker to add."


def _line_number(locator):
    return locator[5:] if locator.startswith("line=") else locator


def resume_sections(job, evidenced_units, transcript, source="interview"):
    """The resume as data, tailored to one job by ordering alone.

    Only what the person said and what they evidenced goes in. No name,
    employer, date or fit is written, because none of them were evidenced and
    a guessed one on a resume is a false claim made in the person's name.
    Tailoring never adds anything: the units this job requires, and the lines
    that evidence them, move to the top; everything else keeps its place.

    With source="resume", transcript holds the resume the person brought, as
    {"line", "en"} rows, and every reference is a resume line number instead
    of a timestamp. Only then do the sections carry "source", so the
    interview's output is unchanged.
    """
    units = _units_by_code()
    evidence = _evidenced(evidenced_units)
    resume = source == "resume"
    if resume:
        label, where, order = "resume", _line_number, int
        lines = {str(line["line"]): line["en"] for line in transcript}
    else:
        label, where, order = "transcript", _timestamp, str
        lines = {line["t"]: line["en"] for line in transcript}
    # What match_jobs() matched is exactly required-and-evidenced.
    required = {u["code"] for u in job["matched"]}

    skills = []
    qualifications = []
    for code, sources in evidence.items():
        if code not in units:
            continue
        stamps = [where(loc) for cited, loc in sources if cited == label]
        skills.append({"code": code, "title": units[code]["title"], "described_at": stamps,
                       "for_this_job": code in required})
        if units[code]["qualification"] not in qualifications:
            qualifications.append(units[code]["qualification"])
    # Stable sort: within each group, the order the pack evidenced them in.
    skills.sort(key=lambda s: not s["for_this_job"])

    # A line is only ever here because a unit cites it, so a line about the
    # journey, which no unit cites, cannot reach the resume.
    for_job = {t for s in skills if s["for_this_job"] for t in s["described_at"]}
    cited = {t for s in skills for t in s["described_at"] if t in lines}
    key = "line" if resume else "t"
    experience = [{key: t, "en": lines[t], "for_this_job": t in for_job}
                  for t in sorted(cited, key=lambda t: (t not in for_job, order(t)))]

    sections = {"job": {"id": job["id"], "title": job["title"], "setting": job["setting"],
                        "location": job["location"]},
                "experience": experience, "skills": skills,
                "qualifications": [{"title": q, "status": RPL_STATUS} for q in qualifications],
                "to_add": TO_ADD}
    if resume:
        sections["source"] = "resume"
    return sections


def resume_text(sections):
    job = sections["job"]
    if sections.get("source") == "resume":
        account = "WORK EXPERIENCE (from the jobseeker's own resume)"
        experience = [f"- {line['en']} [resume line {line['line']}]"
                      for line in sections["experience"]]
        described = "resume line"
    else:
        account = "WORK EXPERIENCE (the jobseeker's own account, translated)"
        experience = [f"- {line['en']} [transcript {line['t']}]"
                      for line in sections["experience"]]
        described = "described at"
    out = [f"DRAFT RESUME - for: {job['title']}, {job['setting']}, {job['location']}",
           "", account]
    out += experience
    out += ["", "SKILLS MAPPED TO AUSTRALIAN UNITS OF COMPETENCY"]
    out += [f"- {s['code']} {s['title']} ({described} {', '.join(s['described_at'])})"
            for s in sections["skills"]]
    out += ["", "QUALIFICATIONS"]
    out += [f"- {q['title']}: {q['status']}" for q in sections["qualifications"]]
    out += ["", sections["to_add"]]
    return "\n".join(out)


def resume_for(job, evidenced_units, transcript):
    """A plain-text draft for the jobseeker to check, built without a model."""
    return resume_text(resume_sections(job, evidenced_units, transcript))
