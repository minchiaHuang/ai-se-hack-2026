# Status

**BridgeWork** turns a refugee jobseeker's spoken work history, in their own
language, into two things a caseworker can act on: an evidence pack mapped to
Australian qualifications (ANZSCO/OSCA codes and VET units of competency), and
matched job ads with a resume drafted for each one. Built for the AI for Social
Enterprise Hackathon 2026 (UTS Startups, 21–22 September 2026).

See `README.md` for what it does, how it runs, where AI is used, where a human
decides, and the limits the team states openly.

## Run it

Live at **https://bridgework.onrender.com**. The free instance sleeps when idle, so the
first request after a quiet spell can take about 50 seconds.

```
python3 skeleton/app.py        # http://127.0.0.1:8000
bash bin/verify.sh             # the whole check
```

Standard library only: no dependency to install and no build step. Without API
keys every page still runs. `?mock=1` uses fixture answers and transcripts, but
still requests spoken questions and the phone Agent link from the server.
Without the ElevenLabs settings, mock mode shows a silent speaking animation
and omits the phone link.

## Last verification

2026-09-22: `bash bin/verify.sh` → GREEN, 337 tests.

## Demo deployment in progress

The phone-link fix is committed at `c4b0d18` on `fix/d7-demo-call-link` but has
not reached `origin/main`. The live site was checked on 2026-09-22: it still
served the old interview page, `/api/speak` reported no `ELEVENLABS_API_KEY`,
and `/api/talk/link` reported that the Agent was not configured.

Local browser verification of the fix: mock mode displayed the configured
ElevenLabs Agent URL, completed 12 fixture turns, and showed Review the answers.
This verifies link display and the simulated transcript, not a real phone call
or live Mandarin audio playback.

Next: merge the reviewed fix into `main`, deploy it, and manually add
`ELEVENLABS_API_KEY` and `ELEVENLABS_AGENT_ID` to the existing Render service's
Environment settings. Save with a redeploy, then verify both endpoints and tap
the interview orb on the live site. `sync: false` only prompts during initial
Blueprint creation; it does not add these values to an existing service.

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
