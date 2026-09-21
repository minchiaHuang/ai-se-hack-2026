# BridgeWork

A refugee jobseeker with no papers describes their work in their own language. BridgeWork turns
what they said into the terms the Australian system already uses: ANZSCO and OSCA occupation codes,
VET units of competency, and the qualification they point towards — then matches that against real
Sydney job ads and drafts a resume for each one. Every item cites the line it came from.

Built at the AI for Social Enterprise Hackathon 2026.

**Live site: https://bridgework.onrender.com** — the free instance sleeps when idle, so the
first request after a quiet spell can take about 50 seconds. No API keys are set there: every
page still runs and says on screen what it could not do, and **Live demo** on the homepage
opens the whole flow against fixtures.

**Why this problem.** A peer-reviewed UNSW study (Guo & Tani, *British Journal of Industrial
Relations*, 2026, n=3,757) found refugees' probability of employment on arrival in Australia is
about 88 percentage points lower, and still more than 51 points lower after five years, and
concluded the main cause is employers screening on experience they cannot verify. That is an
information gap, which is something software can close.

## Run it

```
python3 skeleton/app.py       # http://127.0.0.1:8000
bash bin/verify.sh            # the full check: VERIFY: GREEN or RED
```

Python 3 standard library only: nothing to install, no build step, no database. Add
`?mock=1` to any page to run the whole flow against fixtures with no network at all. No page
says so on screen, and the homepage's **Live demo** button opens the flow this way, so it reads
as the product: nothing is recorded or sent, the client is fictional, and an application is
never actually submitted — say this when demoing.

Optional keys, each one adding a live step: `ANTHROPIC_API_KEY` (mapping, translation, resume
drafting), `ELEVENLABS_API_KEY` (speech to text, the spoken questions, the phone interviewer).
Without them every page still works and says on screen what it could not do — nothing is invented
to fill the gap.

The phone interviewer needs an agent as well as the key. `python3 -m skeleton.tools.phone_agent`
creates one and prints the ids to set (`ELEVENLABS_AGENT_ID`, and `ELEVENLABS_PHONE_NUMBER_ID` to
dial out rather than hand over a link); re-run it with `--update-agent` after changing the
questions or the prompt. Without an agent, `/interview` says so and points at the browser
interview instead.

`/scenarios` lists the earlier directions' pipelines. It is a developer page, served only when no
`PORT` is set in the environment, so a deployment does not carry it.

## The flow

`/` → `/start` (who the session is for) → `/start/path`, then either:

- **`/interview`** — the fixed questions read aloud in Mandarin, answers recorded and transcribed.
  Or the jobseeker talks to an ElevenLabs AI interviewer on their own phone, and the transcript
  comes back sorted into the questions with the Mandarin kept word for word.
- **`/upload`** — a resume they already have, in any language, translated and tidied, shown beside
  the original.

Both land on **`/review`**: every section as a draft the caseworker edits and confirms with the
jobseeker, with the occupation suggested from the resume and changeable. Then **`/jobs`**: real
Adzuna ads, each required unit quoted from the ad it came from, the units still missing named as
gap training, and a resume tailored per job.

## Where AI is used, and where a person decides

The model reads and maps; it never scores the person. One call turns transcript or resume lines
into codes and units, choosing only from the candidates for that occupation, and code drops any
item that cites a line which does not exist. Matching, gap units and the legal gate are counts and
lookups over the reference data — no model at all.

A person decides everything that matters. Nothing is processed without the jobseeker's consent. An
item the model is unsure about is shown as **"Withheld: a person decides"**, with the line it came
from and no value. A question the answers did not cover is listed as still to ask. The resume is a
draft, marked "Recognition of Prior Learning in progress, not yet assessed", until the jobseeker
confirms it. Applying is simulated, and the page says so.

## Limits we state up front

- **No first-hand interviews.** The problem rests on published research, not on refugees or
  caseworkers we spoke to.
- **Three occupations have reference data**: commercial cook, welder, aged care worker. Anything
  else matches no jobs and says so, rather than the nearest wrong ones.
- **Mandarin is the validated demo language.** Arabic is configured but has not been checked with a
  native speaker, so we do not claim it. We claim no accuracy figure for Chinese speech to text.
- **The demo transcripts are fictional**, written with AI help.
- **The homepage photos are stock images** (Unsplash License, copied into
  `skeleton/web/img/`). The people in them are models, not refugees, and the skills labelled
  on them are illustrative.
- **The job ads are real; the mapping is a model's reading of a short teaser**, checked only in that
  the quote must appear verbatim in the ad. No employer has confirmed any of it.

## Reference data

Two JSON files in `skeleton/demo_data/reference/`: the occupations with their ANZSCO 2022 and
OSCA 2024 codes and VET units, and a snapshot of Sydney job ads taken from Adzuna on 2026-09-21 so
the demo runs offline. The migration system still uses ANZSCO while ABS has moved to OSCA, so both
codes are carried. Job ads link back to Adzuna, as their licence requires.
