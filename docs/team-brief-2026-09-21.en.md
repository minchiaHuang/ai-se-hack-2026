# Team brief — frameworks and skeleton

2026-09-21

> Local copy of the shared team doc (English tab).
> Live version: https://claude.ai/code/artifact/de59487e-7908-4442-b651-97a4611eb9ee
> The live doc is the one teammates edit; update both if you change either.

Six problem directions were competitor-checked and **all six are still on the table**, each with a
framework ready to use. A shared code skeleton is already running, so whichever problem we pick goes
into something that works rather than a blank editor.

## Where we landed

An earlier pass eliminated four directions for having existing competitors. **That was withdrawn.**
None of the seven weighted judging criteria rewards novelty (the list is in `AI_CONTEXT.md`), so
"someone already does this" was a test the judges never set. A competitor usually means demand is
proven, which helps Pathway to Sustainability. It is a question to answer, not a disqualification.

| Direction | The strongest argument for it |
| --- | --- |
| 2. Op shop intake triage | Hardest Australian evidence, and three candidate payers |
| 6. WISE outcomes reporting | The payer is government money already allocated |
| 3. Social enterprise evidence layer | Best thematic fit — one judge is Social Traders' Digital Enablement Specialist |
| 1. NDIS document marshalling | Strongest community evidence of pain; 44% of certified social enterprises serve people with disability |
| 5. Food relief | OzHarvest's own 2026 report: 74,000 people turned away every month |
| 4. Renter rights | Huge volume of need, but the user is an individual, not a social enterprise |

Two competitors we found are dead rather than absent: Amplify Social Impact Online closed after low
take-up, and Yume Food was liquidated in November 2024. That cuts both ways and we should say both
sides out loud. It is evidence that adoption is hard — and evidence that serious institutions judged
these problems real enough to put $12M and a decade behind them.

## What each direction actually is

Every direction has its own framework in `docs/frameworks/`, all built on the same seven slots, so
they can be compared side by side and a live proposal can be slotted into one quickly. The AI never
does more than one constrained job in any of them.

| Direction | The one job AI does | The number the organisation keeps |
| --- | --- | --- |
| 1. NDIS documents | Extract — file, page number, exact sentence; generates nothing | Hours spent marshalling evidence per case |
| 2. Intake triage | Classify and suggest a destination | Disposal cost avoided today |
| 3. Evidence layer | Extract and map; never writes a claim | Times one piece of evidence was reused |
| 4. Renter rights | Retrieve only; deliberately drafts no letters | Not settled — see the objection below |
| 5. Food relief | Extract offer details from free-text messages | Kilograms refused per month for lack of capacity |
| 6. WISE outcomes | Aggregate and map to the funder's format | Reporting preparation hours |

**Two objections survive, and neither is about competitors.** Direction 4's user is an individual
renter, not a social enterprise, at a social enterprise hackathon — the framework offers reframing the
user as a tenancy advocacy caseworker, but marks that as an untested recommendation. And food fraud
(direction 5's other branch) needs isotope forensics we cannot build in 48 hours, with the ACCC
already investigating; the framework is built on food relief instead.

Whichever we choose, we will be asked "someone already does this". Do not deny it. Name the competitor
more precisely than the asker can, say what it proves about demand, then say the one specific thing we
do differently — and label it honestly as a bet or as evidence. If we cannot say that third thing,
that is the one moment a competitor should change our mind. Two examples already written down:

- **Recycle Mate** (free, government funded) answers "which bin does this go in" for a consumer before
  they throw something out. We answer "what is this item's highest-value destination" for a shop after
  it arrives, from the shop's own route list.
- **Social Enterprise Australia's shared data system** is sector-level statistics: how big the sector
  is and what it looks like. We are one WISE preparing one return.

If we cannot say those lines cleanly, we are rebuilding something that already exists.

## Framing whatever we hear at 10:00

The real problem will probably come from a social enterprise in the room, not from our list. Every
direction is written as the same seven slots, so anything new can be framed the same way in a few
minutes.

1. One user, one moment, one blocked outcome. If the answer is "everyone, all the time", keep asking
   until it is one person.
2. The break point: which step costs the most or goes wrong most. Ask for the number — hours, dollars,
   how often.
3. **The ideal human workflow, with no AI in it.**
4. The one constrained task AI gets: classify, retrieve, extract, summarise, recommend, or warn.
   Exactly one.
5. The decision a human must keep.
6. The golden path, plus one low-confidence or failure path.
7. The single number the organisation walks away with.

Slot 3 is a gate, not a step. If we cannot describe how the work should go without AI, we do not move
to slot 4. That is what stops us picking a technique and then hunting for a problem to justify it.

Before committing to anything, it also has to clear: is there a free or mature product already doing
it; is the beneficiary actually a social enterprise (a grant-funded charity is not one); who pays,
given the enterprise itself is usually cash-poor; and can we say honestly where the demo data came from.

## For the designer

The happy path is the least interesting screen we have. Three states carry the pitch, and all three
already run in the skeleton — they need design, not engineering.

| State | What the screen has to say | Where it runs |
| --- | --- | --- |
| Suggested | The value, the reason in plain words, a confidence number, and the source it came from — all four, on one row a volunteer reads in a second | `/run?s=d2` |
| Not confident | The value is **withheld**, not shown greyed out, plus why the system struggled and who to ask | `/run?s=d2_lowconfidence` |
| Refused | The system will not answer at all, and says so plainly without blaming the user | `/run?s=d6_small_group` |

The refusal exists because reporting on a group of three people would narrow in on individuals. It is
a deliberate ethical limit made visible, and it is the screen most likely to be remembered.

Two things worth knowing before sketching. First, a human confirms every single row — nothing the model
says takes effect on its own, so the confirm action needs to feel light rather than like a chore.
Second, the strongest evidence we found for direction 2 is that op shop staff resent being *told to
throw away usable things*; a screen that feels like it is ordering someone to bin an item repeats
exactly what they already hate.

Current styling is deliberately minimal. Nothing in the layout is precious — the logic underneath will
not break when it is replaced.

## For the data scientist

Two rules are enforced in code rather than left to whoever writes the next module, both in
`skeleton/core/schema.py`:

- A suggestion with no source is rejected outright, as an error, not a warning.
- Below the confidence threshold the value is withheld — `displayed_value()` returns nothing, so it
  cannot reach the screen even by accident.

The threshold is currently 0.6 and is a guess. Picking it properly is a job worth taking: it is the
trade-off between withholding too often (the tool feels useless) and showing a wrong destination (the
tool gets someone to bin a sellable item). A small labelled set and an error taxonomy would give us the
answer, and judges ask about exactly this.

Direction 6 has a hard floor on top: fields that look individual (name, employee id, date of birth,
email, address, phone) and any group under five are refused before the model is called at all.
Aggregate only — no scoring, monitoring or capability inference about a supported employee. Breaking
that invalidates the entry regardless of how good the work is.

What we may not claim, and these are already written into the research notes:

- No public dataset exists for donation condition, and none for employee-level WISE data. Demos use
  synthetic or self-made samples and must say so on screen.
- We have run no interviews, no validation and no testing. We cannot say we have.
- PlanMind's self-reported traction figures, and NDS turnover figures about paid support staff, are
  both off limits — the second describes a different population from WISE supported employees.
- The WISE impact costs report may hold the cost figures we are missing, but nobody has opened the full
  PDF yet, so nothing from it is citable.

## Run it, and what is still open

From the repo root:

```
python3 skeleton/app.py       # then open http://127.0.0.1:8000
bash bin/verify.sh            # 25 tests, all green
```

No packages to install and no API key. The model layer is a stub, so every scenario runs with no
network — which is also our demo backup if the venue wifi dies. One model call, no RAG, no agents, no
vector database.

Adding a direction on the day means one new file with five things in it: a name, the metric, a guard,
what gets prepared for the model, and which fields are expected. Register it, add a demo scenario, and
it runs.

Still open:

- [ ] Push the branches — commits are still only on one laptop
- [ ] Find the source URL for OzHarvest's Frontline Report 2026; without it the 74,000 figure cannot be
      used on stage
- [ ] Open the WISE impact costs PDF by hand; it may close the one quantified gap direction 6 has
- [ ] Pick the confidence threshold with something better than intuition
- [ ] For whichever direction we choose, write the one-sentence answer to "someone already does this"

**On the day, a real problem from a real social enterprise beats everything above.** These frameworks
exist to give us a shape and verified evidence to reach for, not to decide what we build.
