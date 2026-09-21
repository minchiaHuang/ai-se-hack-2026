# Undocumented work history → Australian evidence

A consultant at a refugee employment service and a jobseeker who has no papers sit at one screen.
The jobseeker describes their work in their own language. The system turns what they said into an
**evidence pack**: the ANZSCO and OSCA occupation codes, the Australian units of competency the
account supports, and the qualification it points towards. Every item links back to the transcript
line it came from. It also matches the evidenced units against sample jobs, lists the units still to
evidence as gap training, and drafts a resume.

Built for the AI for Social Enterprise Hackathon 2026.

## The problem

Refugees who arrive in Australia with work experience but no documents struggle to have that
experience believed. A peer-reviewed UNSW study (Guo & Tani, *British Journal of Industrial
Relations*, 2026, n=3,757) found that refugees' probability of employment on arrival in Australia is
about 88 percentage points lower, and still more than 51 percentage points lower after five years,
and concluded that the main cause is how employers screen when they cannot verify overseas
experience. This project goes after that information gap. It turns a spoken, undocumented work
history into the terms the Australian system already uses, and every claim cites the words it came
from.

## How to run

Python 3 standard library only. No third-party dependencies, no build step and no database.

```
python3 skeleton/app.py
```

Then open **http://127.0.0.1:8000/intake**. The root page, http://127.0.0.1:8000, is the earlier
multi-direction skeleton. Its direction-7 scenarios run the same pipeline, including a welding case
and each refusal.

`python3 -m skeleton.app` also works. The server binds to port 8000 on `127.0.0.1`.

Offline smoke test, which renders every scenario without starting a server. It prints nothing and
exits 0 when everything renders:

```
python3 skeleton/app.py --check
```

### Optional API keys

| Variable | With it | Without it |
|---|---|---|
| `ELEVENLABS_API_KEY` | Recorded audio goes to ElevenLabs Scribe (`scribe_v2`) for transcription. | `/api/transcribe` returns one fixed English placeholder line marked `offline`, and the page shows an "Offline" banner saying the line is not what was said. |
| `ANTHROPIC_API_KEY` | The evidence pack comes from one Claude Messages API call (default `claude-sonnet-5`, override with `ANTHROPIC_MODEL`). | Canned demo output comes back through the same pipeline. |

If a live call fails (no network, a non-2xx response, output that doesn't parse), the code falls back
to the offline behaviour instead of raising. The golden path runs with no key and no network, and that
offline run is the demo backup.

On the intake page, tick consent, then **Use demo transcript** loads a Mandarin example interview
and builds the pack in one step. `/intake?mock=1` runs the whole page against in-page fixtures with no backend.

## Architecture

```
 jobseeker speaks ──► /api/transcribe ──► transcript lines {t, text, en}
 (language chosen      refuses an unsupported         │
  by the user, not     language before any            │  consultant presses
  auto-detected)       audio is sent                  ▼  "Build evidence pack"
                                         ┌─────────── /api/extract ───────────┐
                                         │ guard()    red lines; raises before │
                                         │            the model is called      │
                                         │ prepare()  transcript + candidate   │
                                         │            codes from reference data│
                                         │ model      one call: extract & map  │
                                         │ pipeline   no source → rejected;    │
                                         │            confidence < 0.6 →       │
                                         │            value withheld           │
                                         └──────────────────┬──────────────────┘
                                                            ▼
                     evidence pack: codes, units, qualification, each citing t=MM:SS
                     + withheld items + unanswered fields + the occupation's legal gate
                                                            │ evidenced units only
                                                            ▼
                                         /api/match ──► sample jobs for the occupation
                                                        (fit = "N of M required units evidenced")
                                                    ──► gap units (missing units → RTO)
                                                    ──► a draft resume tailored to each job
```

| Module | What it does |
|---|---|
| `skeleton/app.py` | Standard-library HTTP server. It serves `/intake` and the three JSON routes (`/api/transcribe`, `/api/extract`, `/api/match`), plus the older scenario pages at `/`. It also picks the stub or the live model. `/api/match` returns a tailored resume for every job (`resumes`), and keeps the best-fit job's draft as `resume`. |
| `skeleton/web/intake.html` | The two-person intake page: one inline HTML file with vanilla JS. It has language choice, consent, recording, a bilingual transcript, the evidence pack and the legal gate. Matches appear as a job-board list, with location and employment-type filters. Each card shows a count panel ("N of M required units evidenced") instead of a percentage. There are also the gap units and a side panel with the selected job's resume, which can be copied or printed on its own. |
| `skeleton/core/pipeline.py` | The shared path every direction runs through: `guard` → `prepare` → model → split by confidence → gaps → metric. |
| `skeleton/core/schema.py` | Data shapes. A suggestion with no source cannot be constructed, and anything below the confidence threshold is withheld. |
| `skeleton/core/model.py` | `StubModel`, which returns canned suggestions so the pipeline runs offline. |
| `skeleton/core/live.py` | Real ElevenLabs Scribe and Anthropic Messages calls over `urllib`, both falling back to offline. It drops any model item whose code is not among the candidates or whose timestamp is not in the transcript. |
| `skeleton/core/registry.py` | Reads the reference data: both classification codes, the units, the qualification, and an optional check that the qualification's source PDF is reachable. |
| `skeleton/directions/d7_credentials.py` | Direction 7: the red lines (`guard`), what the model sees (`prepare`), the fields asked for, and the metric. |
| `skeleton/directions/d7_match.py` | Job matching, gap units and one draft resume per job, all built without a model. A resume is tailored by ordering alone: the units a job requires, and the lines that evidence them, move to the top, and nothing is added. |

### Where AI is used

- **Speech to text** (ElevenLabs Scribe, when `ELEVENLABS_API_KEY` is set). Mandarin is sent as `zho`
  and Arabic as `ar`.
- **One extraction-and-mapping call** (Claude, when `ANTHROPIC_API_KEY` is set). It reads the
  transcript lines and the candidate codes for the occupation, and returns the ANZSCO code, OSCA code,
  qualification and evidenced units. Each item has a reason, a confidence and a transcript timestamp.
  The call is told to copy codes only from the candidates, never to rate the person, and to ignore
  anything about the person's journey or why they fled. Code then drops any item that breaks the
  first rule or cites a line that doesn't exist.

Matching, gap units, the resume and the legal gate involve **no model**. They are counts and lookups
over the reference data.

### Where a human decides

- The **jobseeker** chooses the language and gives consent. Nothing is processed without consent.
- The **consultant** asks the questions and sees what was said, in the original language with an
  English gloss.
- An item below confidence 0.6 is shown as **"Withheld: a person decides"**, with the line it came
  from, and no value is shown.
- A field the transcript did not answer is listed as **"Not answered yet: ask about these"**.
- The resume is a **draft** for the jobseeker to check. It says "Recognition of Prior Learning in
  progress, not yet assessed", and it leaves name, contact details, employers and dates for the
  jobseeker to add.

## Data

There is **no database**. The reference data is two JSON files in the repository, read by the server:

- `skeleton/demo_data/reference/occupations.json` holds three occupations prepared by hand for the
  demo: aged care / personal care worker, welder / metal fabricator, and commercial cook. Each
  carries:
  - its **ANZSCO 2022** code and its **OSCA 2024** code (ABS);
  - its qualification and a subset of its units of competency, from **training.gov.au**, with a
    link to the qualification's PDF;
  - its assessing authority. `verified: false` marks the ones not yet confirmed;
  - the **legal gate** for the occupation, with its government source. Examples are the aged care
    worker screening requirement and the NSW Food Safety Supervisor rule.
- `skeleton/demo_data/reference/jobs.json` holds 17 sample jobs: 9 for cooks, 4 for welders and 4
  for aged care. Each has a title, a setting, a location in NSW, an employment type (full-time,
  part-time or casual), a level, a shift and the units it requires. Each is marked "Representative
  sample, not a real listing".

**Why both ANZSCO and OSCA:** OSCA has replaced ANZSCO at the ABS, but migration still runs on
ANZSCO, so each occupation carries both codes. Codes also move between the two. For example, ANZSCO
322313 is not OSCA 322313.

**A superseded qualification:** the welding qualification `MEM31922` has been replaced by `MEM31925`,
which is current from 2025-09-04. The data points at `MEM31925` and records `MEM31922` as superseded.
The superseded PDF still downloads, so the optional reachability check proves only that a source
exists, not that it is current. Currency comes from the seeded record.

Three occupations are not the full ANZSCO. They were prepared by hand for this demo.

## Red lines and failure paths

These are enforced in code before the model is called, and tests cover them
(`tests/test_d7_guard.py`, `tests/test_d7_pipeline.py`, `tests/test_http.py`). A refusal comes back as
HTTP 200 `{"refused": "..."}` and the page shows a refusal panel. Nothing is switched to English or
guessed in its place.

| Trigger | What happens |
|---|---|
| Input carries `country_of_origin`, `visa_status`, `protection_claim` or a biometric field | Refused: *"identifying or protection-related field must never be collected"* |
| Input carries a score of the person (`candidate_score`, `employability_score`, `person_rating`) | Refused: *"this system does not score people"* |
| Consent not given | Refused: *"consent was not given; nothing may be processed"* |
| Language other than Mandarin (`zh`) or Arabic (`ar`) | Refused before any audio is sent. The page offers Tigrinya and Farsi precisely to show this refusal. |
| A suggestion with no source | Cannot be constructed. The live model's items are also dropped if they cite a timestamp the transcript does not have, or a code that is not among the candidates. |
| Confidence below 0.6 | The value is withheld for the consultant. In the demo, the qualification (confidence 0.44) is withheld. |
| No speech service | The offline banner appears, and placeholder lines are marked as not what was said. |
| No model / model call fails | The canned answer comes back through the same pipeline. |

Two further rules hold in `d7_match.py`. A job's fit is a count ("2 of 4 required units evidenced"),
never a percentage or a score of the person. And the fit never appears in the resume.

## Honest limits

- **No first-hand interviews.** We have not interviewed refugees, consultants or settlement
  providers. The problem rests on published research.
- **Arabic is configured but not validated** by a native speaker. We do not claim it works well.
- **The Mandarin demo transcripts were written with AI help.** They are fictional examples, not a
  real person's account.
- **The jobs are representative samples**, not real listings.
- **No ElevenLabs accuracy figure for Chinese is claimed.** We have not checked one.
- **Audio retention settings at ElevenLabs have not been verified.** We make no claim of zero
  retention.
- The intake page is fixed to the commercial cook frame. The welding scenario runs from the root page.

## Tests

```
bash bin/verify.sh
```

It runs the shell syntax check, a few repository checks and the Python test suite
(`python3 -m unittest discover -s tests`). It ends with `VERIFY: GREEN` or `VERIFY: RED`.
