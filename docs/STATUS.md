# Status

**BridgeWork** turns a refugee jobseeker's spoken work history, in their own
language, into two things a caseworker can act on: an evidence pack mapped to
Australian qualifications (ANZSCO/OSCA codes and VET units of competency), and
matched job ads with a resume drafted for each one. Built for the AI for Social
Enterprise Hackathon 2026 (UTS Startups, 21–22 September 2026).

See `README.md` for what it does, how it runs, where AI is used, where a human
decides, and the limits the team states openly.

## Run it

```
python3 skeleton/app.py        # http://127.0.0.1:8000
bash bin/verify.sh             # the whole check
```

Standard library only: no dependency to install and no build step. Without API
keys every page still runs, and says on screen what it could not do rather than
filling the gap with invented text. `?mock=1` runs the flow against fixtures
with no network at all.

## Last verification

2026-09-22: `bash bin/verify.sh` → GREEN, 330 tests.

## What is built

- `/` → `/start` → `/start/path`: a photo-led homepage, the caseworker's entry, then two ways
  in. The photos are Unsplash stock: the people are models, not refugees.
- `/interview`: the fixed questions read aloud in Mandarin when the caseworker
  taps the orb, answers recorded and transcribed, or an ElevenLabs AI interviewer
  the jobseeker talks to on their own phone; the transcript is sorted into the
  questions, Mandarin verbatim.
- `/upload`: a resume the jobseeker already has, in any language, translated and
  tidied, shown side by side with the original.
- `/review`: every section as a draft the caseworker edits and confirms, with the
  occupation suggested from the resume and changeable.
- `/jobs`: real Adzuna ads from a committed snapshot, each required unit quoted
  from the ad it came from, gap training named, and a resume per job. Applying is
  simulated and the page says so.

## Known limits

- Three occupations have reference data: commercial cook, welder, aged care
  worker. Anything else matches no jobs and says so rather than the nearest.
- Mandarin is the validated demo language; Arabic is configured but has not been
  checked with a native speaker, so it is not claimed.
- The job board is a snapshot taken on 2026-09-21, so the demo runs offline.
