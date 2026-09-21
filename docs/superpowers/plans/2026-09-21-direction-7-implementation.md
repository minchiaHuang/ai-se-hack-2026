# 方向 7 實作計畫 — 口述經歷 → ANZSCO/OSCA 佐證包 ＋ 媒合

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal**：難民用母語口述無文件的工作史，系統產出一份指得回逐字稿、帶信心值、
低信心交人裁決的 ANZSCO/OSCA ＋ VET RPL 佐證包，並附帶職缺媒合與履歷。

**Architecture**：沿用既有 `skeleton/`。新增一個方向模組插進既有管線；
新增一個參考資料層（職業／資格／單元）；新增一頁 vanilla JS 共桌介面。
外部呼叫一律走標準函式庫 `urllib.request`。

**Tech Stack**：Python 3 標準函式庫（`http.server`／`urllib.request`／`json`／`unittest`）、
一頁 HTML ＋ vanilla JS。**零外部套件、零建置步驟、無 node_modules。**

**Spec**：`docs/superpowers/specs/2026-09-21-direction-7-design.md`
**框架與證據**：`docs/frameworks/direction-7-refugee-employment.md`
**研究原始紀錄**：`docs/research-brief-2026-09-21.md` 第 8 節

---

## Global Constraints

這些是全案硬性約束，每個 task 都隱含包含：

- **零外部套件。** 不得安裝任何第三方套件、不得新增 `requirements.txt`、不得引入 node。
  真實 API 呼叫用 `urllib.request`。安裝任何相依套件需 Tommy 明確核准（`CLAUDE.md`）。
- **`skeleton/core/pipeline.py` 與 `skeleton/core/schema.py` 不得修改。** 它們已被 25 個測試覆蓋。
- **`bash bin/verify.sh` 每個 task 結束都必須 GREEN。**
- **離線優先。** 任何真實 API 路徑都必須有 stub 回退，且 `python3 skeleton/app.py --check`
  在無網路、無 API key 的情況下必須通過。這就是 demo 備援。
- **API key 只從環境變數讀取，絕不進 git。**（`ELEVENLABS_API_KEY`、`ANTHROPIC_API_KEY`）
- **不得捏造代碼。** ANZSCO／OSCA／資格／單元代碼一律用本計畫 Task 1 附的已驗證值，
  或現場從官方來源抓。捏造一個單元代碼會被澳洲評審當場抓到。
- **紅線是 `raise`，不是回傳旗標。** 呼叫端不得有「忽略」的選項。
- **每個 task 以 commit 結束。** 分支 `docs/direction-7-refugee-employment` 或其後續分支。

---

## 文件結構

| 檔案 | 建立／修改 | 職責 |
|---|---|---|
| `skeleton/demo_data/reference/occupations.json` | 建立 | 三個職業的 ANZSCO 2022 ＋ OSCA 2024 ＋ 資格 ＋ 單元 ＋ 評估機構 ＋ 閘門，全部已驗證 |
| `skeleton/core/registry.py` | 建立 | 讀參考資料；檢查資格來源可達；不知道方向 7 的存在 |
| `skeleton/directions/d7_credentials.py` | 建立 | 方向模組：四條紅線的 `guard()`、`prepare()`、`target_fields()`、`metric()` |
| `skeleton/core/live.py` | 建立 | `urllib` 打 ElevenLabs 與 LLM；失敗一律回退 stub |
| `skeleton/web/intake.html` | 建立 | 共桌單頁介面：左逐字稿、右佐證包 |
| `skeleton/app.py` | 修改 | 註冊 d7、掛載 `/intake` 與 API 端點、捕捉新例外 |
| `skeleton/demo_data/payloads.json` | 修改 | 新增四個 d7 情境（黃金路徑 ＋ 三條失敗路徑） |
| `skeleton/demo_data/canned/d7*.json` | 建立 | 對應的罐頭模型輸出 |
| `tests/test_d7_guard.py` | 建立 | 四條紅線各自的回歸測試 |
| `tests/test_d7_registry.py` | 建立 | 參考資料完整性與來源檢查 |
| `tests/test_d7_pipeline.py` | 建立 | 黃金路徑與信心分流 |

**切線**：**Task 1–6 是必須完成的最小可上台版本。** Task 7–9 是 stretch，
主線沒跑通、備援影片沒錄好之前不要碰（`AI_CONTEXT.md`「Avoid」第五條）。

> ⚠️ **切線前的 demo 是「真實語音轉文字 → 罐頭佐證包」。** 佐證包不會隨口述內容改變，
> 評審若上前講一段焊接經歷，畫面仍會吐出烹飪的結果。
> **Tommy 2026-09-21 決定維持此順序，以錄影 demo 為準**：錄影必須照罐頭情境
> （阿拉伯語、三年營區廚房、食品安全）講，現場不開放評審自由口述。

---

### Task 1: 參考資料種子（三個職業）

**Files:**
- Create: `skeleton/demo_data/reference/occupations.json`
- Create: `skeleton/core/registry.py`
- Test: `tests/test_d7_registry.py`

**Interfaces:**
- Consumes: 無
- Produces: `registry.load_occupations() -> dict`；`registry.occupation(key) -> dict`；
  `registry.all_units(key) -> tuple[dict, ...]`；`registry.classifications(key) -> tuple[dict, dict]`。
  鍵為 `"aged_care"`／`"welding"`／`"cookery"`。

**所有代碼皆於 2026-09-21 由官方來源驗證。不得改動、不得新增未驗證的代碼。**

- [ ] **Step 1: 寫失敗的測試**

```python
# tests/test_d7_registry.py
"""Reference data must be real. A fabricated unit code is caught on stage."""
import unittest

from skeleton.core import registry


class ReferenceData(unittest.TestCase):
    def test_three_occupations_are_seeded(self):
        self.assertEqual(
            set(registry.load_occupations()), {"aged_care", "welding", "cookery"}
        )

    def test_each_occupation_carries_both_classifications(self):
        """ANZSCO 2022 still runs migration; OSCA 2024 runs ABS statistics."""
        for key in registry.load_occupations():
            with self.subTest(key=key):
                occ = registry.occupation(key)
                self.assertRegex(occ["anzsco"]["code"], r"^\d{6}$")
                self.assertRegex(occ["osca"]["code"], r"^\d{6}$")
                self.assertTrue(occ["anzsco"]["title"])
                self.assertTrue(occ["osca"]["title"])

    def test_welding_points_at_the_current_qualification(self):
        """MEM31922 was superseded by MEM31925 on 2025-09-04."""
        qual = registry.occupation("welding")["qualification"]
        self.assertEqual(qual["code"], "MEM31925")
        self.assertEqual(qual["superseded_code"], "MEM31922")

    def test_every_unit_has_a_code_and_a_title(self):
        for key in registry.load_occupations():
            for unit in registry.all_units(key):
                with self.subTest(key=key, unit=unit.get("code")):
                    self.assertRegex(unit["code"], r"^[A-Z]{3,7}\d{3,6}$")
                    self.assertTrue(unit["title"].strip())

    def test_cookery_carries_the_nsw_food_safety_supervisor_units(self):
        """SITXFSA005 + SITXFSA006 are the NSW statutory certificate."""
        codes = {u["code"] for u in registry.all_units("cookery")}
        self.assertIn("SITXFSA005", codes)
        self.assertIn("SITXFSA006", codes)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python3 -m unittest tests.test_d7_registry -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'skeleton.core.registry'`

- [ ] **Step 3: 寫參考資料**

建立 `skeleton/demo_data/reference/occupations.json`：

```json
{
  "aged_care": {
    "label": "Aged care / personal care worker",
    "anzsco": {"code": "423313", "title": "Personal Care Assistant", "skill_level": 4,
               "source": "ABS ANZSCO 2022"},
    "osca": {"code": "421331", "title": "Residential Aged Care Worker", "skill_level": 4,
             "source": "ABS OSCA 2024 v1.0"},
    "isco08": {"code": "5321", "title": "Health care assistants", "match": "partial"},
    "splits_note": "ANZSCO 423111 Aged or Disabled Carer splits into four OSCA occupations: 421132 Aged Care Team Leader, 421231 Community Aged Care Support Worker, 422231 Disability Support Worker, 422232 Disability Team Leader.",
    "qualification": {"code": "CHC33021",
                      "title": "Certificate III in Individual Support",
                      "release": 1, "status": "Current", "superseded_code": null,
                      "pdf": "https://training.gov.au/assets/CHC/CHC33021_R1.pdf",
                      "packaging": "15 units = 9 core + 6 electives; at least 120 hours of work"},
    "units": [
      {"code": "CHCCCS031", "title": "Provide individualised support", "role": "core"},
      {"code": "CHCCCS038", "title": "Facilitate the empowerment of people receiving support", "role": "core"},
      {"code": "CHCCCS040", "title": "Support independence and wellbeing", "role": "core"},
      {"code": "HLTINF006", "title": "Apply basic principles and practices of infection prevention and control", "role": "core"},
      {"code": "HLTWHS002", "title": "Follow safe work practices for direct client care", "role": "core"},
      {"code": "CHCAGE011", "title": "Provide support to people living with dementia", "role": "elective"},
      {"code": "CHCAGE013", "title": "Work effectively in aged care", "role": "elective"}
    ],
    "assessing_authority": {"name": "ANMAC / Community Work Australia",
                            "verified": false,
                            "note": "ANMAC page is bot-protected; verify by hand before putting on a slide. Aged care is NOT on the TRA OSAP list."},
    "gate": {"kind": "screening",
             "text": "From 1 November 2025 every aged care worker must hold a police certificate issued within the last 3 years, or an NDIS Worker Screening Check clearance issued within the last 5 years.",
             "source": "https://www.health.gov.au/topics/aged-care-workforce/screening-requirements",
             "refugee_note": "A police certificate covering time in a country the person fled may be impossible to obtain. Surface this as a named next step, do not hand-wave it."}
  },
  "welding": {
    "label": "Welder / metal fabricator",
    "anzsco": {"code": "322313", "title": "Welder (First Class)", "skill_level": 3,
               "source": "ABS ANZSCO 2022"},
    "osca": {"code": "331133", "title": "Welder (First Class)", "skill_level": 3,
             "source": "ABS OSCA 2024 v1.0"},
    "isco08": {"code": "7212", "title": "Welders and flamecutters", "match": "partial"},
    "splits_note": "Codes move between classifications: ANZSCO 322313 is not OSCA 322313. Metal Fabricator is ANZSCO 322311 / OSCA 331131.",
    "qualification": {"code": "MEM31925",
                      "title": "Certificate III in Engineering - Fabrication Trade",
                      "release": 1, "status": "Current", "superseded_code": "MEM31922",
                      "superseded_on": "2025-09-02", "current_from": "2025-09-04",
                      "pdf": "https://training.gov.au/assets/MEM/MEM31925_R1.pdf",
                      "packaging": "96 points = all core (33) + at least 40 from a specialisation group + at most 23 from Group H"},
    "units": [
      {"code": "MEM09002", "title": "Interpret technical drawing", "role": "core", "points": 4},
      {"code": "MEM12023", "title": "Perform engineering measurements", "role": "core", "points": 5},
      {"code": "MEM13015", "title": "Work safely and effectively in manufacturing and engineering", "role": "core", "points": 2},
      {"code": "MEM18001", "title": "Use hand tools", "role": "core", "points": 2},
      {"code": "MEM05052", "title": "Apply safe welding practices", "role": "welding", "points": 4},
      {"code": "MEM05012", "title": "Perform routine manual metal arc welding", "role": "welding", "points": 2},
      {"code": "MEM05050", "title": "Perform routine gas metal arc welding", "role": "welding", "points": 2},
      {"code": "MEM05049", "title": "Perform routine gas tungsten arc welding", "role": "welding", "points": 2},
      {"code": "MEM05007", "title": "Perform manual heating and thermal cutting", "role": "welding", "points": 2}
    ],
    "assessing_authority": {"name": "Trades Recognition Australia (TRA), Offshore Skills Assessment Program",
                            "verified": true,
                            "note": "OSAP requires proof of employment and a passport from a nominated country, plus AUD 2,020-5,320 and about 15 weeks. A documentless refugee is structurally locked out. Target the domestic RTO/RPL lane instead."},
    "gate": {"kind": "none",
             "text": "No NSW occupational licence for general welding. Pressure and high-risk welding sit under separate AS/NZS regimes (not verified - do not claim).",
             "source": "https://training.gov.au/assets/MEM/MEM31925_R1.pdf"}
  },
  "cookery": {
    "label": "Commercial cook",
    "anzsco": {"code": "351411", "title": "Cook", "skill_level": 3, "source": "ABS ANZSCO 2022"},
    "osca": {"code": "322331", "title": "Cook", "skill_level": 3, "source": "ABS OSCA 2024 v1.0"},
    "isco08": {"code": "5120", "title": "Cooks", "match": "partial"},
    "splits_note": "ANZSCO 351311 Chef becomes OSCA 161631 Senior Chef - it moves into a managerial major group. A static code lookup breaks here.",
    "qualification": {"code": "SIT30821",
                      "title": "Certificate III in Commercial Cookery",
                      "release": 1, "status": "Current", "superseded_code": null,
                      "pdf": "https://training.gov.au/assets/SIT/SIT30821_R1.pdf",
                      "packaging": "25 units = 20 core + 5 electives"},
    "units": [
      {"code": "SITHCCC027", "title": "Prepare dishes using basic methods of cookery", "role": "core"},
      {"code": "SITHCCC029", "title": "Prepare stocks, sauces and soups", "role": "core"},
      {"code": "SITHCCC036", "title": "Prepare meat dishes", "role": "core"},
      {"code": "SITHCCC043", "title": "Work effectively as a cook", "role": "core"},
      {"code": "SITXFSA005", "title": "Use hygienic practices for food safety", "role": "core"},
      {"code": "SITXFSA006", "title": "Participate in safe food handling practices", "role": "core"}
    ],
    "assessing_authority": {"name": "Trades Recognition Australia (TRA)", "verified": true,
                            "note": "Cook [351411] and Chef [351311] are both on the TRA OSAP nominated-occupation list."},
    "gate": {"kind": "statutory_opportunity",
             "text": "A NSW business serving ready-to-eat potentially hazardous food must appoint a certified Food Safety Supervisor within 30 days. The FSS certificate requires exactly SITXFSA006 plus its prerequisite SITXFSA005, valid 5 years. From 1 September 2025 both units must be completed with the same RTO.",
             "source": "https://www.foodauthority.nsw.gov.au/sites/default/files/2023-07/FSS_Guidelines.pdf",
             "refugee_note": "This is the strongest demo moment: two core units ARE the statutory certificate a NSW employer legally needs. Immediate value, not a migration outcome years away."}
  }
}
```

- [ ] **Step 4: 寫 registry**

```python
# skeleton/core/registry.py
"""Australian occupational and vocational reference data.

Kept here rather than in the direction module because it is reference data about
the country, not about our product. Every code in occupations.json was verified
against an official source on 2026-09-21; nothing here may be invented.
"""
import json
from functools import lru_cache
from pathlib import Path

REFERENCE = Path(__file__).resolve().parent.parent / "demo_data" / "reference"


@lru_cache(maxsize=1)
def load_occupations():
    return json.loads((REFERENCE / "occupations.json").read_text(encoding="utf-8"))


def occupation(key):
    try:
        return load_occupations()[key]
    except KeyError:
        raise KeyError(f"{key}: not a seeded occupation") from None


def all_units(key):
    return tuple(occupation(key)["units"])


def classifications(key):
    """Both codes, because migration runs on ANZSCO while the ABS runs on OSCA."""
    occ = occupation(key)
    return occ["anzsco"], occ["osca"]
```

- [ ] **Step 5: 跑測試確認通過**

Run: `python3 -m unittest tests.test_d7_registry -v`
Expected: PASS（5 個測試）

- [ ] **Step 6: 跑完整驗證**

Run: `bash bin/verify.sh`
Expected: `VERIFY: GREEN`

- [ ] **Step 7: Commit**

```bash
git add skeleton/core/registry.py skeleton/demo_data/reference/occupations.json tests/test_d7_registry.py
git commit -m "feat(d7): seed verified ANZSCO/OSCA and VET reference data

Every code checked against ABS and training.gov.au on 2026-09-21.
MEM31922 was superseded by MEM31925 on 2025-09-04, so the welding
entry carries both and names the supersession.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 2: 方向模組與四條紅線

**Files:**
- Create: `skeleton/directions/d7_credentials.py`
- Test: `tests/test_d7_guard.py`

**Interfaces:**
- Consumes: `registry.classifications()`、`registry.all_units()`（Task 1）
- Produces: `d7_credentials.KEY = "d7"`、`NAME`、`METRIC`、
  `guard(payload)`、`prepare(payload)`、`target_fields(payload)`、`metric(accepted, payload)`、
  例外 `RedLineError`、`UnsupportedLanguageError`、常數 `SUPPORTED_LANGUAGES`

- [ ] **Step 1: 寫失敗的測試**

```python
# tests/test_d7_guard.py
"""Direction 7 red lines, enforced in code before the model is called."""
import unittest

from skeleton.directions import d7_credentials as d7


def payload(**over):
    base = {
        "occupation": "cookery",
        "language": "ar",
        "consent": True,
        "transcript": [{"t": "00:12", "text": "I cooked in a camp kitchen for three years."}],
    }
    base.update(over)
    return base


class RedLines(unittest.TestCase):
    def test_identifying_refugee_fields_are_refused(self):
        for field in ("country_of_origin", "visa_status", "protection_claim", "biometric_id"):
            with self.subTest(field=field):
                with self.assertRaises(d7.RedLineError) as caught:
                    d7.guard(payload(**{field: "x"}))
                self.assertIn(field, str(caught.exception))

    def test_missing_consent_is_refused(self):
        with self.assertRaises(d7.RedLineError) as caught:
            d7.guard(payload(consent=False))
        self.assertIn("consent", str(caught.exception).lower())

    def test_unsupported_language_is_refused_not_silently_englished(self):
        """Tigrinya, Dari, Rohingya and Hazaragi have no ElevenLabs voice."""
        for code in ("ti", "prs", "rhg", "haz"):
            with self.subTest(code=code):
                with self.assertRaises(d7.UnsupportedLanguageError) as caught:
                    d7.guard(payload(language=code))
                self.assertIn(code, str(caught.exception))

    def test_scoring_the_person_is_refused(self):
        """A job-fit score is allowed. A score on the human being is not."""
        with self.assertRaises(d7.RedLineError):
            d7.guard(payload(candidate_score=0.8))

    def test_a_clean_payload_passes(self):
        d7.guard(payload())

    def test_supported_languages_are_only_the_ones_we_can_actually_do(self):
        self.assertEqual(set(d7.SUPPORTED_LANGUAGES), {"ar", "fa", "sw"})


class Shape(unittest.TestCase):
    def test_target_fields_cover_both_classifications(self):
        fields = d7.target_fields(payload())
        for expected in ("anzsco_code", "osca_code", "qualification", "units_evidenced"):
            self.assertIn(expected, fields)

    def test_the_gate_is_never_asked_of_the_model(self):
        """It is reference data. Asking the model would render it as a guess."""
        self.assertNotIn("gate", d7.target_fields(payload()))

    def test_prepare_sends_exactly_the_transcript_and_the_occupational_frame(self):
        prepared = d7.prepare(payload(label="demo"))
        self.assertEqual(set(prepared), {"transcript", "candidate_units", "anzsco", "osca"})


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python3 -m unittest tests.test_d7_guard -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'skeleton.directions.d7_credentials'`

- [ ] **Step 3: 寫方向模組**

```python
# skeleton/directions/d7_credentials.py
"""Direction 7 - spoken, undocumented work history into Australian structures.

The constrained task is extraction and mapping. Not generation: nothing is
claimed that the person did not say. Not scoring: no number is put on a human.

The red lines are enforced here, before the model is called, because the data
belongs to people whose safety can depend on it not existing anywhere.
"""
from skeleton.core import registry

KEY = "d7"
NAME = "Undocumented experience"
METRIC = "evidence items mapped to a transcript line"

# Only the languages ElevenLabs can actually handle well. Pashto sits at
# 25-50% WER and is left out on purpose; Dari, Tigrinya, Rohingya and
# Hazaragi have no voice at all. We refuse rather than silently use English.
SUPPORTED_LANGUAGES = ("ar", "fa", "sw")

# Fields that identify a refugee, or expose a protection claim. A database row
# holding these is a route back to the people they fled.
FORBIDDEN_FIELDS = (
    "country_of_origin",
    "visa_status",
    "protection_claim",
    "biometric",
)

# Scoring a job's fit is allowed. Scoring the person is not.
PERSON_SCORE_FIELDS = ("candidate_score", "employability_score", "person_rating")


class RedLineError(Exception):
    """Raised when input would cross an ethical red line."""


class UnsupportedLanguageError(Exception):
    """Raised rather than falling back to English behind the user's back."""


def guard(payload):
    for field in payload:
        lowered = field.lower()
        if any(marker in lowered for marker in FORBIDDEN_FIELDS):
            raise RedLineError(
                f"{field}: identifying or protection-related field must never be collected"
            )
        if lowered in PERSON_SCORE_FIELDS:
            raise RedLineError(f"{field}: this system does not score people")

    if not payload.get("consent"):
        raise RedLineError("consent was not given; nothing may be processed")

    language = payload.get("language")
    if language not in SUPPORTED_LANGUAGES:
        raise UnsupportedLanguageError(
            f"{language}: not supported. This demo runs in "
            f"{', '.join(SUPPORTED_LANGUAGES)}. We will not fake a language "
            "we cannot pronounce."
        )


def prepare(payload):
    """What the model sees: the transcript and the occupational frame, nothing else."""
    occupation_key = payload["occupation"]
    anzsco, osca = registry.classifications(occupation_key)
    return {
        "transcript": payload["transcript"],
        "candidate_units": registry.all_units(occupation_key),
        "anzsco": anzsco,
        "osca": osca,
    }


def target_fields(payload):
    """What the model is asked for. The gate is not here: it is reference data
    about the occupation, looked up, never guessed."""
    return ("anzsco_code", "osca_code", "qualification", "units_evidenced")


def metric(accepted, payload):
    """Evidence items that carry a transcript locator. Nothing else counts."""
    return sum(1 for s in accepted if s.sources)
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python3 -m unittest tests.test_d7_guard -v`
Expected: PASS（9 個測試）

- [ ] **Step 5: 跑完整驗證**

Run: `bash bin/verify.sh`
Expected: `VERIFY: GREEN`

- [ ] **Step 6: Commit**

```bash
git add skeleton/directions/d7_credentials.py tests/test_d7_guard.py
git commit -m "feat(d7): direction module with four red lines enforced before the model

Refuses identifying fields, missing consent, unsupported languages and
any attempt to score the person. Raises rather than returning a flag, so
the caller has no ignore path.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 3: 接上 demo 外殼 —— 黃金路徑與三條失敗路徑可離線跑完

**Files:**
- Modify: `skeleton/app.py`（`DIRECTIONS`、例外捕捉）
- Modify: `skeleton/demo_data/payloads.json`
- Create: `skeleton/demo_data/canned/d7.json`
- Create: `skeleton/demo_data/canned/d7_lowconfidence.json`
- Test: `tests/test_d7_pipeline.py`

**Interfaces:**
- Consumes: Task 2 的 `d7_credentials`；既有 `pipeline.run()`
- Produces: 情境鍵 `d7`、`d7_lowconfidence`、`d7_unsupported_language`、`d7_no_consent`；
  `app.REFUSALS` 例外元組

- [ ] **Step 1: 寫失敗的測試**

```python
# tests/test_d7_pipeline.py
"""Direction 7 through the shared pipeline: golden path and the failures."""
import unittest

from skeleton.core.model import StubModel
from skeleton.core.pipeline import run
from skeleton.directions import d7_credentials as d7

CANNED = [
    {"field": "anzsco_code", "value": "351411 Cook",
     "reason": "Three years cooking for 200 people a day in a camp kitchen.",
     "confidence": 0.86, "sources": [["transcript", "t=00:12"]]},
    {"field": "osca_code", "value": "322331 Cook",
     "reason": "Same testimony; OSCA 2024 code for the same occupation.",
     "confidence": 0.84, "sources": [["transcript", "t=00:12"]]},
    {"field": "units_evidenced", "value": "SITXFSA005; SITXFSA006",
     "reason": "Describes separating raw and cooked food and logging fridge temperatures.",
     "confidence": 0.78, "sources": [["transcript", "t=02:41"]]},
    {"field": "qualification", "value": "SIT30821 Certificate III in Commercial Cookery",
     "reason": "Both food safety units sit in the core of this qualification.",
     "confidence": 0.44, "sources": [["transcript", "t=02:41"]]},
]

PAYLOAD = {
    "occupation": "cookery",
    "language": "ar",
    "consent": True,
    "transcript": [{"t": "00:12", "text": "I cooked for two hundred people a day."}],
}


class GoldenPath(unittest.TestCase):
    def setUp(self):
        self.model = StubModel({d7.KEY: CANNED})

    def test_confident_suggestions_are_shown_and_cite_the_transcript(self):
        result = run(d7, PAYLOAD, self.model)
        self.assertEqual(len(result.suggestions), 3)
        for suggestion in result.suggestions:
            self.assertTrue(suggestion.sources)
            self.assertEqual(suggestion.sources[0].label, "transcript")

    def test_low_confidence_is_withheld_for_a_person_to_decide(self):
        result = run(d7, PAYLOAD, self.model)
        withheld = {s.field for s in result.needs_human}
        self.assertIn("qualification", withheld)
        for suggestion in result.needs_human:
            self.assertIsNone(suggestion.displayed_value())

    def test_a_complete_answer_leaves_no_gaps(self):
        self.assertEqual(run(d7, PAYLOAD, self.model).gaps, ())

    def test_a_field_the_model_did_not_answer_is_reported_as_a_gap(self):
        partial = [item for item in CANNED if item["field"] != "osca_code"]
        result = run(d7, PAYLOAD, StubModel({d7.KEY: partial}))
        self.assertEqual(result.gaps, ("osca_code",))

    def test_metric_counts_only_sourced_items(self):
        result = run(d7, PAYLOAD, self.model)
        self.assertEqual(result.metric_value, 3)
        self.assertEqual(result.metric_name, d7.METRIC)


class FailurePaths(unittest.TestCase):
    def test_unsupported_language_stops_before_the_model(self):
        model = StubModel({d7.KEY: CANNED})
        with self.assertRaises(d7.UnsupportedLanguageError):
            run(d7, dict(PAYLOAD, language="ti"), model)

    def test_missing_consent_stops_before_the_model(self):
        model = StubModel({d7.KEY: CANNED})
        with self.assertRaises(d7.RedLineError):
            run(d7, dict(PAYLOAD, consent=False), model)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python3 -m unittest tests.test_d7_pipeline -v`
Expected: FAIL — `ModuleNotFoundError` 或 metric 不符

- [ ] **Step 3: 新增情境與罐頭資料**

`skeleton/demo_data/canned/d7.json` 放上面 `CANNED` 的內容（JSON 格式）。

`skeleton/demo_data/canned/d7_lowconfidence.json`：

```json
[
  {"field": "anzsco_code", "value": "uncertain",
   "reason": "The recording is unclear about whether this was paid work or helping family.",
   "confidence": 0.31, "sources": [["transcript", "t=04:08"]]}
]
```

`skeleton/demo_data/payloads.json` 新增四個鍵（保留既有五個）：

```json
"d7": {
  "label": "Camp kitchen, three years, no papers",
  "occupation": "cookery", "language": "ar", "consent": true,
  "transcript": [{"t": "00:12", "text": "I cooked for two hundred people a day."}]
},
"d7_lowconfidence": {
  "label": "Unclear whether the work was paid",
  "occupation": "cookery", "language": "ar", "consent": true,
  "transcript": [{"t": "04:08", "text": "I helped in my uncle's kitchen."}]
},
"d7_unsupported_language": {
  "label": "Tigrinya - we refuse rather than fake it",
  "occupation": "cookery", "language": "ti", "consent": true,
  "transcript": []
},
"d7_no_consent": {
  "label": "Consent not given - nothing is processed",
  "occupation": "cookery", "language": "ar", "consent": false,
  "transcript": []
}
```

- [ ] **Step 4: 接上 app.py**

三處改動：

```python
# import 區
from skeleton.directions import d2_triage, d3_evidence, d6_outcomes, d7_credentials
from skeleton.directions.d7_credentials import RedLineError, UnsupportedLanguageError

DIRECTIONS = {"d2": d2_triage, "d3": d3_evidence,
              "d6": d6_outcomes, "d7": d7_credentials}

REFUSALS = (AggregationError, RedLineError, UnsupportedLanguageError)
```

`render_result()` 的例外捕捉改成捕捉全部三種拒絕：

```python
    try:
        result = run(direction, payload, model_for(scenario_key))
    except REFUSALS as refused:
        return (head + '<div class="refused"><strong>Refused</strong><p>'
                + html.escape(str(refused)) + "</p></div>" + back)
```

- [ ] **Step 5: 跑測試與離線煙霧測試**

Run: `python3 -m unittest tests.test_d7_pipeline -v && python3 skeleton/app.py --check`
Expected: PASS，且 `--check` 無輸出（四個 d7 情境全部渲染成功，含兩個拒絕畫面）

- [ ] **Step 6: 跑完整驗證**

Run: `bash bin/verify.sh`
Expected: `VERIFY: GREEN`

- [ ] **Step 7: Commit**

```bash
git add skeleton/app.py skeleton/demo_data/payloads.json skeleton/demo_data/canned/ tests/test_d7_pipeline.py
git commit -m "feat(d7): wire direction 7 into the demo shell with three failure paths

Golden path plus low confidence, unsupported language and withheld
consent, all rendering offline with the stub model. This is the demo
backup: it runs with no network and no API key.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 4: 資格來源檢查 —— 以及它**不能**證明什麼

**為什麼這個 task 存在**：佐證包要附上每個資格的官方出處，而且要能當場點開。

**⚠️ 審查時實測的限制（2026-09-21）**：已被取代的 `MEM31922_R1.pdf` **照樣回 HTTP 200、
是有效 PDF**。所以「網址連得上」**不等於**「資格仍有效」。
這個 task 因此只宣稱它做得到的事：**來源可達**。
被取代的事實（`MEM31922` → `MEM31925`，2025-09-04）來自種子資料，
台上說法是：**「已於 2026-09-21 對國家登錄庫查核」**，不是「即時查核」。

**Files:**
- Modify: `skeleton/core/registry.py`
- Test: `tests/test_d7_registry.py`（追加）

**Interfaces:**
- Consumes: Task 1 的 `occupation()`
- Produces: `registry.source_check(key, fetch=None) -> dict`，回傳
  `{"code", "status", "superseded_code", "reachable", "source"}`；
  `registry.fetch_pdf_head(url) -> bytes`（預設抓取器）。
  `fetch` 未給時不碰網路，`reachable=False`。

- [ ] **Step 1: 追加失敗的測試**

```python
# 追加到 tests/test_d7_registry.py
class SourceCheck(unittest.TestCase):
    def test_offline_reports_the_seeded_record_unchecked(self):
        checked = registry.source_check("cookery")
        self.assertEqual(checked["code"], "SIT30821")
        self.assertEqual(checked["status"], "Current")
        self.assertFalse(checked["reachable"])

    def test_the_seeded_record_names_what_was_superseded(self):
        checked = registry.source_check("welding")
        self.assertEqual(checked["code"], "MEM31925")
        self.assertEqual(checked["superseded_code"], "MEM31922")

    def test_a_pdf_response_marks_the_source_reachable(self):
        def fake_fetch(url):
            self.assertTrue(url.endswith("MEM31925_R1.pdf"))
            return b"%PDF-1.4"

        self.assertTrue(registry.source_check("welding", fetch=fake_fetch)["reachable"])

    def test_a_non_pdf_response_is_not_reachable(self):
        """An error page served with 200 must not count."""
        checked = registry.source_check("welding", fetch=lambda url: b"<html>")
        self.assertFalse(checked["reachable"])

    def test_a_failed_fetch_degrades_instead_of_raising(self):
        def broken_fetch(url):
            raise OSError("no network at the venue")

        checked = registry.source_check("welding", fetch=broken_fetch)
        self.assertFalse(checked["reachable"])
        self.assertEqual(checked["code"], "MEM31925")
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python3 -m unittest tests.test_d7_registry -v`
Expected: FAIL — `AttributeError: module 'skeleton.core.registry' has no attribute 'source_check'`

- [ ] **Step 3: 實作**

```python
# 追加到 skeleton/core/registry.py
import urllib.request


def fetch_pdf_head(url):
    """Default fetcher. Kept separate so tests never touch the network."""
    with urllib.request.urlopen(url, timeout=6) as response:
        return response.read(8)


def source_check(key, fetch=None):
    """Confirm the qualification's published source is reachable right now.

    This proves the document is there, NOT that it is current: a superseded
    qualification's PDF still returns 200 (MEM31922 did on 2026-09-21). Currency
    comes from the seeded record, verified against the national register that
    day. Degrades to unchecked rather than raising, so bad venue wifi is fine.
    """
    qualification = occupation(key)["qualification"]
    result = {
        "code": qualification["code"],
        "status": qualification["status"],
        "superseded_code": qualification["superseded_code"],
        "reachable": False,
        "source": qualification["pdf"],
    }
    if fetch is None:
        return result
    try:
        head = fetch(qualification["pdf"])
    except Exception:
        return result
    result["reachable"] = head.startswith(b"%PDF")
    return result
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python3 -m unittest tests.test_d7_registry -v`
Expected: PASS（10 個測試）

- [ ] **Step 5: 手動確認一次，並親眼看到這個限制**（不要放進自動測試）

```bash
python3 -c "
import urllib.request
for c in ('MEM31925','MEM31922'):
    r=urllib.request.urlopen(f'https://training.gov.au/assets/MEM/{c}_R1.pdf',timeout=10)
    print(c, r.status, r.read(4))"
```

Expected: **兩個都是 `200 b'%PDF'`**。第二行就是為什麼這個檢查不能叫「現行狀態查核」。

- [ ] **Step 6: 跑完整驗證並 commit**

```bash
bash bin/verify.sh
git add skeleton/core/registry.py tests/test_d7_registry.py
git commit -m "feat(d7): check that each qualification's source is reachable

Reachability, not currency: the superseded MEM31922 PDF still returns 200.
Supersession comes from the seeded record, verified against the national
register on 2026-09-21. Degrades to unchecked when the network is down.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 5: 共桌介面（一頁 vanilla JS，無建置步驟）

**Files:**
- Create: `skeleton/web/intake.html`
- Modify: `skeleton/app.py`（新增 `/intake` 路由與 `/api/extract`；`HTTPServer` → `ThreadingHTTPServer`）
- Test: `tests/test_app.py`（追加）

**Interfaces:**
- Consumes: Task 3 的 `REFUSALS` 與管線
- Produces: `app.extract(payload) -> dict`；`GET /intake` 回頁面；
  `POST /api/extract` 回 `{suggestions, needs_human, gaps, gate, metric_name, metric_value}`
  或 `{refused: "<reason>"}`。**`gate` 來自 registry，不經過模型**——
  那是關於職業的參考資料，查表而得，不是猜的。

**版面**：兩欄。左欄逐字稿（母語原文 ＋ 英文對照，每句可點）；
右欄佐證包（confidence chip、`needs_human` 標紅、gate 列為具名下一步）。

- [ ] **Step 1: 寫失敗的測試**

```python
# 追加到 tests/test_app.py
class IntakeEndpoint(unittest.TestCase):
    def test_extract_returns_a_sourced_evidence_pack(self):
        from skeleton.app import extract
        body = extract({
            "occupation": "cookery", "language": "ar", "consent": True,
            "transcript": [{"t": "00:12", "text": "I cooked for two hundred people a day."}],
        })
        self.assertIn("suggestions", body)
        self.assertTrue(all(s["sources"] for s in body["suggestions"]))

    def test_extract_attaches_the_gate_from_the_registry(self):
        """The strongest demo line must never render as a blank."""
        from skeleton.app import extract
        body = extract({"occupation": "cookery", "language": "ar", "consent": True,
                        "transcript": [{"t": "00:12", "text": "x"}]})
        self.assertIn("Food Safety Supervisor", body["gate"]["text"])

    def test_extract_reports_a_refusal_as_data_not_an_exception(self):
        from skeleton.app import extract
        body = extract({"occupation": "cookery", "language": "ti",
                        "consent": True, "transcript": []})
        self.assertIn("refused", body)
        self.assertIn("ti", body["refused"])
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python3 -m unittest tests.test_app -v`
Expected: FAIL — `ImportError: cannot import name 'extract'`

- [ ] **Step 3: 實作 `extract()`**

```python
# 追加到 skeleton/app.py
def extract(payload):
    """Run the pipeline and return JSON-safe data. Refusals come back as data."""
    try:
        result = run(d7_credentials, payload, model_for("d7"))
    except REFUSALS as refused:
        return {"refused": str(refused)}
    return {
        "suggestions": [
            {"field": s.field, "value": s.displayed_value(), "reason": s.reason,
             "confidence": s.confidence,
             "sources": [[x.label, x.locator] for x in s.sources]}
            for s in result.suggestions
        ],
        "needs_human": [
            {"field": s.field, "reason": s.reason, "confidence": s.confidence,
             "sources": [[x.label, x.locator] for x in s.sources]}
            for s in result.needs_human
        ],
        "gaps": list(result.gaps),
        "gate": registry.occupation(payload["occupation"])["gate"],
        "metric_name": result.metric_name,
        "metric_value": result.metric_value,
    }
```

import 區加上 `from skeleton.core import registry`。

`Handler` 新增 `do_POST` 處理 `/api/extract`，`do_GET` 新增 `/intake` 回傳
`skeleton/web/intake.html`。伺服器改成 `ThreadingHTTPServer`（標準函式庫），
否則等 API 回應時整頁會卡住：

```python
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
...
        ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
```

- [ ] **Step 4: 寫頁面**

`skeleton/web/intake.html`：單檔、`<style>` 與 `<script>` 內嵌、無外部資源。
必備元素：

1. 開場語言下拉（`ar` / `fa` / `sw` ＋ 一個會被拒絕的 `ti`，用來演失敗路徑）
2. consent 勾選，未勾就不送出
3. 錄音鈕（`MediaRecorder`；Task 6 接真 API，此時先送預設逐字稿）
4. 左欄逐字稿、右欄佐證包，`fetch('/api/extract')` 後重繪
5. 收到 `refused` 時整頁換成拒絕畫面，**不得靜默退回英文**
6. **閘門獨立成一塊顯示**（取自回應的 `gate`，不是 `gaps`）。
   烹飪情境要看得到 NSW 食品安全主管那一句——那是整場最強的一幕
7. 資格旁附官方 PDF 連結；若 `superseded_code` 非空，顯示「已取代 `MEM31922`」

- [ ] **Step 5: 跑測試與離線煙霧測試**

Run: `python3 -m unittest tests.test_app -v && python3 skeleton/app.py --check`
Expected: PASS

- [ ] **Step 6: 人眼確認**

Run: `python3 skeleton/app.py`，開 `http://127.0.0.1:8000/intake`
Expected: 兩欄版面；選 `ti` 出現拒絕畫面；不勾 consent 無法送出

- [ ] **Step 7: 跑完整驗證並 commit**

```bash
bash bin/verify.sh
git add skeleton/web/intake.html skeleton/app.py tests/test_app.py
git commit -m "feat(d7): two-person intake page, no build step

One HTML file, vanilla JS, no framework and no node_modules, so the
offline backup stays a single python3 command.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 6: 接上真實語音轉文字（ElevenLabs Scribe，`urllib` 直打）

**Files:**
- Create: `skeleton/core/live.py`
- Modify: `skeleton/app.py`（新增 `POST /api/transcribe`）
- Test: `tests/test_live.py`

**Interfaces:**
- Consumes: 環境變數 `ELEVENLABS_API_KEY`
- Produces: `live.transcribe(audio, language, post=None, api_key=None) -> dict`
  回傳 `{"text": str, "offline": bool}`；無金鑰或呼叫失敗時 `offline=True`

**設計決定**：**分段錄音，不做真串流。** 標準函式庫沒有 WebSocket server；
分段（講一段 → 轉一段 → append）在畫面上幾乎一樣，但失敗時只掉一段而不是整場。

- [ ] **Step 1: 寫失敗的測試**

```python
# tests/test_live.py
"""Live calls degrade to offline rather than breaking the demo."""
import unittest

from skeleton.core import live


class Transcribe(unittest.TestCase):
    def test_without_an_api_key_it_reports_offline(self):
        result = live.transcribe(b"audio", "ar", post=None, api_key="")
        self.assertTrue(result["offline"])
        self.assertTrue(result["text"])

    def test_with_a_key_it_posts_and_returns_the_text(self):
        def fake_post(url, headers, fields, files):
            self.assertIn("elevenlabs", url)
            self.assertEqual(headers["xi-api-key"], "k")
            self.assertEqual(fields["language_code"], "ar")
            return {"text": "I cooked for two hundred people a day."}

        result = live.transcribe(b"audio", "ar", post=fake_post, api_key="k")
        self.assertFalse(result["offline"])
        self.assertIn("two hundred", result["text"])

    def test_a_network_failure_degrades_to_offline(self):
        def broken_post(*args, **kwargs):
            raise OSError("venue wifi")

        result = live.transcribe(b"audio", "ar", post=broken_post, api_key="k")
        self.assertTrue(result["offline"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python3 -m unittest tests.test_live -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'skeleton.core.live'`

- [ ] **Step 3: 實作**

```python
# skeleton/core/live.py
"""Real API calls over urllib, so the project keeps zero dependencies.

Every function here degrades to offline rather than raising. At a venue with
bad wifi a demo that falls back is a demo; one that raises is a blank screen.
"""
import json
import os
import urllib.request
import uuid

SCRIBE_URL = "https://api.elevenlabs.io/v1/speech-to-text"
OFFLINE_TEXT = "I cooked for two hundred people a day in the camp kitchen."


def _multipart(url, headers, fields, files):
    boundary = uuid.uuid4().hex
    body = bytearray()
    for name, value in fields.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        body += f"{value}\r\n".encode()
    for name, (filename, payload) in files.items():
        body += f"--{boundary}\r\n".encode()
        body += (f'Content-Disposition: form-data; name="{name}"; '
                 f'filename="{filename}"\r\n').encode()
        body += b"Content-Type: application/octet-stream\r\n\r\n"
        body += payload + b"\r\n"
    body += f"--{boundary}--\r\n".encode()

    request = urllib.request.Request(url, data=bytes(body), method="POST")
    request.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    for key, value in headers.items():
        request.add_header(key, value)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def transcribe(audio, language, post=None, api_key=None):
    key = os.environ.get("ELEVENLABS_API_KEY", "") if api_key is None else api_key
    if not key:
        return {"text": OFFLINE_TEXT, "offline": True}
    sender = _multipart if post is None else post
    try:
        body = sender(
            SCRIBE_URL,
            {"xi-api-key": key},
            {"model_id": "scribe_v1", "language_code": language},
            {"file": ("segment.webm", audio)},
        )
    except Exception:
        return {"text": OFFLINE_TEXT, "offline": True}
    return {"text": body.get("text", ""), "offline": False}
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python3 -m unittest tests.test_live -v`
Expected: PASS（3 個測試）

- [ ] **Step 5: 接上 `/api/transcribe` 並用真金鑰實測一次**

```bash
export ELEVENLABS_API_KEY=...   # 絕不寫進任何檔案
python3 skeleton/app.py
```

在 `/intake` 錄一段真的阿拉伯語，確認逐字稿出現、時間戳正確。
**若額度不足或失敗，立即回到 offline 模式並在台上說明**——這是設計好的行為，不是意外。

- [ ] **Step 6: 跑完整驗證並 commit**

```bash
bash bin/verify.sh
git add skeleton/core/live.py skeleton/app.py tests/test_live.py
git commit -m "feat(d7): live speech-to-text over urllib, still zero dependencies

Segmented rather than streaming: the standard library has no websocket
server, and a dropped segment beats a dropped session. No key means
offline mode, not a crash.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## ⛔ 切線 —— 以下是 stretch，主線與備援影片完成前不要開始

`AI_CONTEXT.md`「Avoid」第五條：五個半成品輸給一個完整工作流。

---

### Task 7: 真實 LLM 抽取（取代罐頭資料）

**Files:** Modify `skeleton/core/live.py`、`skeleton/app.py`；Test `tests/test_live.py`

**Interfaces:** Produces `live.suggest(prepared, post=None, api_key=None) -> list[dict]`，
輸出與 `StubModel.suggest()` 同形（`field`／`value`／`reason`／`confidence`／`sources`）。

- [ ] **Step 1: 寫測試** —— 無金鑰時回傳罐頭資料；有金鑰時呼叫 Messages API；
      **模型回傳的任何一項若沒有 `sources` 就丟棄**（`schema.Suggestion` 會擋，
      但要在這裡先擋掉並記錄，否則整批會因一項而炸掉）
- [ ] **Step 2: 跑測試確認失敗**
- [ ] **Step 3: 實作**：`urllib.request` POST 到 `https://api.anthropic.com/v1/messages`，
      header `x-api-key` 與 `anthropic-version: 2023-06-01`，模型 `claude-opus-5`。
      提示詞只准做抽取與對映：**每一項都必須引用逐字稿的時間戳，找不到依據就不要輸出該項。**
- [ ] **Step 4: 跑測試確認通過**
- [ ] **Step 5: `bash bin/verify.sh` 與 commit**

### Task 8: B 線 —— 職缺媒合與履歷

**Files:** Create `skeleton/directions/d7_match.py`、`skeleton/demo_data/reference/jobs.json`；
Test `tests/test_d7_match.py`

**必守的界線**：`match rate` 評的是**職缺與經歷的吻合度**，不是評人，
且**這個分數不給雇主看**。`guard()` 的第四條紅線已經擋掉對人評分的欄位，不要繞過它。

- [ ] **Step 1: 寫測試** —— 吻合度由「已具證據的單元 ∩ 職缺要求的單元」算出，
      每一條吻合都必須指回逐字稿；沒有證據的單元不得計入
- [ ] **Step 2: 跑測試確認失敗**
- [ ] **Step 3: 實作**
- [ ] **Step 4: 跑測試確認通過**
- [ ] **Step 5: 手寫三則有代表性的澳洲職缺**放進 `jobs.json`，
      **標明是代表性樣本，不是抓來的真實刊登**（Seek 的 ToS 不必要地惹麻煩）
- [ ] **Step 6: `bash bin/verify.sh` 與 commit**

### Task 9: 備援與彩排

- [ ] **Step 1: 錄製完整 demo 影片**（黃金路徑 ＋ 三條失敗路徑 ＋ 資格來源與取代紀錄）。
      **照罐頭情境講**（阿拉伯語、三年營區廚房、食品安全），因為切線前佐證包不隨口述改變
- [ ] **Step 2: 斷網實測**：關掉 wifi，跑 `python3 skeleton/app.py --check` 與 `/intake`，
      確認 offline 模式全程可用
- [ ] **Step 3: 逐條複驗上台要念的數字**，打開原始 URL；
      對照框架檔「⛔ 不要引用的數字」一節
- [ ] **Step 4: 確認 TIS 的 HSP 供應商資格那條推論**（官網），
      確認不了就改講已確認的部分
- [ ] **Step 4b: 查清楚 ElevenLabs 的音檔保留設定**。音檔會送到這個第三方；
      沒查清楚之前，台上**不得**說「零保留」或「音檔不離開本機」
- [ ] **Step 5: 彩排三次**，含評審最可能問的那一題：
      *「澳洲證據說壞的是雇主那端，你為什麼修求職者？」*

---

## 自我檢查（writing-plans 要求，已執行）

**1. Spec 覆蓋**：spec §4 架構 → Task 2；§4 四條紅線 → Task 2；§5 資料流 → Task 3、5、6；
§6 三條失敗路徑 → Task 3（離線）＋ Task 5（介面）；§7 語言清單 → Task 2 的 `SUPPORTED_LANGUAGES`；
§8 那一個數字 → Task 2 的 `metric()`；§9 demo 誠實邊界 → Task 1 資料與 Task 8 Step 5；
§10 測試 → 每個 task 的紅綠循環；§11 相依套件 → Global Constraints 的零套件約束
（`urllib` 取代 SDK，**因此不再需要安裝核准**）；§12 工時分配 → 切線位置。

**2. 佔位符掃描**：無 TBD／TODO；每個 code step 都有可執行的程式碼。
Task 5 Step 4 與 Task 7–9 以條列規格取代完整程式碼，因為它們依賴前面 task 的真實輸出，
先寫會是猜的——這一點在「已知的未解事項」中明載。

**3. 型別一致性**：`guard`／`prepare`／`target_fields`／`metric` 的簽章與
`pipeline.run()` 的呼叫一致；`Suggestion.sources` 一律為 `(label, locator)` 對；
`REFUSALS` 在 Task 3 定義、Task 5 使用；`registry.source_check()` 在 Task 4 定義；
`gate` 不在 `target_fields()`，由 Task 5 的 `extract()` 從 registry 附上。

**4. 實跑驗證（2026-09-21 審查）**：Task 1–5 的程式碼原封貼進拋棄式副本實際執行，
**54 個測試全過**，`python3 skeleton/app.py --check` 與 `python3 -m skeleton.app --check`
離線皆通過。審查修正了 1 個 BLOCKER（單元代碼格式檢查漏了 7 字母前綴 `SITHCCC`／`SITXFSA`）
與 4 個 SERIOUS（閘門被渲染成空白、來源檢查被誤稱為現行狀態查核、切線前 demo 的限制、
紅線措辭超出實際涵蓋）。

## 已知的未解事項

- ⚠️ **紅線的實際涵蓋範圍比框架檔寫的窄（2026-09-21 審查發現）。**
  `guard()` 只檢查**結構化欄位名稱**。求職者口述時講出的原籍國、簽證、庇護細節
  會進逐字稿、送進模型，**音檔也會先送到 ElevenLabs**。
  台上只能講實際做到的：**不存任何結構化身分欄位、我們的伺服器不落地保存**。
  框架檔與 spec 的紅線措辭已同步修正。

- **`live.suggest()` 的提示詞**在 Task 7 才定稿。抽取品質是整個佐證包的上限，
  但它依賴 Task 6 的真實逐字稿樣本，先寫會是猜的。
- **ANMAC 作為長照評估機構未經驗證**（官網有 bot 防護，回 HTTP 202）。
  `occupations.json` 已用 `"verified": false` 標記。上台前人工確認，確認不了就不要講。
- **training.gov.au 的 SOAP 服務僅 sandbox 憑證可用**，production 拒絕。
  Task 4 因此走無需認證的 PDF 資產網址，不碰 SOAP。若要引用登錄庫，說「national register sandbox」。
- **母語逐字稿內容**由隊友或母語者填寫（Tommy 2026-09-21 決定）。
  `payloads.json` 的 `transcript` 目前是英文，母語欄位待補。
- **前端是否改由設計師用 React 寫**尚未決定。本計畫假設 vanilla JS。
  若改用 React，Task 5 需重寫，且 Global Constraints 的「零建置步驟」不再成立。
