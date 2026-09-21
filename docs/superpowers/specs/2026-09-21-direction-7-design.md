# 設計規格 — 方向 7：難民就業（口述經歷 → 佐證包 ＋ 媒合）

**日期**：2026-09-21
**分支**：`docs/direction-7-refugee-employment`
**狀態**：設計已由 Tommy 核准（2026-09-21 傍晚）；已實作並合入本分支（`b980247`），§4／§7／§11 已對齊出貨程式碼
**脈絡**：`docs/frameworks/direction-7-refugee-employment.md`（框架與證據）
　　　　`docs/research-brief-2026-09-21.md` 第 8 節（研究原始紀錄）

---

## 1. 要解決的問題

安置機構的就業顧問與一位**沒有任何文件**的難民求職者共桌。
求職者的工作史沒有證書、沒有紀錄、沒有澳洲推薦人。
顧問只能靠斷續的英文問答拼湊，寫出一份雇主無法判斷真偽的履歷。
雇主在篩選那一刻缺乏可信資訊，於是把人當成風險，**在面試之前就刷掉**。

**斷點**：把口述的、無文件的經歷，變成澳洲制度看得懂並且敢信的東西。

**證據**（Guo & Tani, BJIR 2026, n=3,757）：難民抵澳時就業機率低約 88 個百分點，
五年後仍低超過 51 個百分點，**主因是雇主在無法驗證海外資歷時的篩選行為**。

## 2. 使用者

**兩個人共桌，一台電腦放中間。**

| 角色 | 是誰 | 在系統裡做什麼 |
|---|---|---|
| **求職者** | 無文件的難民 | 選語言、用母語口述工作史、決定要不要送出 |
| **顧問** | HSP／SETS／Workforce Australia 供應商的 employment consultant | 看即時雙語逐字稿、當場追問、裁決低信心欄位 |

**買家**：該機構。錢來自既有的 4/12/26 週成效付款線。
**受益人**：求職者。**他不付錢。**

## 3. 範圍 —— 兩條主線，地位平起平坐

**2026-09-21 由 Tommy 拍板：兩條都是正式功能，不是一主一副。**

```
                共桌口述訪談
                     │
              結構化經歷檔
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
    A. 佐證包                B. 媒合與履歷
    ANZSCO 代碼              職缺吻合度
    VET RPL units            依職缺調整的履歷
    每項要補的證據
    須送正式評估的旗標
```

### 已知風險，明寫在此

**B 線所在的車道是滿的**：Jobright（美國限定）、Simplify、LazyApply、Careerflow；
Kickresume／AIApply **免費**翻譯履歷；**澳洲政府自己免費翻 10 份官方文件**；
JobSparrow 在澳紐本地已明文鎖定 migrants。

**這個風險是明知並選擇承擔的。** 上台的答法（照念）：

> *"We are honest that this lane is crowded. We build it because the structured
> intake already produced the data — generating a resume from it is zero marginal
> cost. We do not claim to win on that lane."*

差異化的主張只放在 A 線：**澳洲制度（ANZSCO／VET RPL／TRA／VETASSESS）鎖死，
SkillLab 的 ESCO 對映搬不過來——這正是它不在澳洲的原因。**

### 明確不做

- ❌ 朗讀整個介面（30 分鐘的按鈕，撐不起 Effective Use of AI）
- ❌ AI 口譯通話（TIS National 有免費真人服務，踩下去就死）
- ❌ 對人評分、排名、評級
- ❌ 把 `match rate` 給雇主看
- ❌ 完整 ANZSCO 圖譜（demo 只手工整理 3 個職業）

## 4. 架構

### 重用既有骨架，不重寫

`skeleton/core/pipeline.py` 與 `skeleton/core/schema.py` **不改**。
它們已經提供本方向需要的全部形狀，且有 25 個測試在護：

| 既有機制 | 方向 7 怎麼用 |
|---|---|
| `pipeline.run()` 先呼叫 `direction.guard()` **再呼叫模型** | 紅線在資料進模型之前就擋下 |
| `Suggestion.__post_init__` 強制 `sources` 非空 | 每個抽出的經歷欄位都必須指回逐字稿的某一句 |
| `sort_by_confidence()` | 高信心顯示；低信心進 `needs_human` 交顧問裁決 |
| `Result.gaps` | 沒問到的欄位列出來，提示顧問補問 |
| `Result.metric_*` | 吐出那一個數字 |

### 實際新增的檔案（對齊 `b980247` 出貨的程式碼）

原設計寫的是「只新增一個檔案」。實作後新增的是下面這些，`pipeline.py` 與 `schema.py` 仍然沒改：

| 檔案 | 做什麼 |
|---|---|
| `skeleton/directions/d7_credentials.py` | 方向模組：`guard()` 四條紅線、`prepare()`、`target_fields()`、`metric()` |
| `skeleton/directions/d7_match.py` | B 線：職缺媒合（吻合度是「幾個單元已佐證」的計數，不是分數）、缺口單元→課程、依職缺產生履歷草稿；不呼叫模型 |
| `skeleton/core/registry.py` | 讀參考資料：ANZSCO／OSCA 兩組代碼、單元、資格；`source_check()` 只證明資格 PDF 還在，不證明它是現行版本 |
| `skeleton/core/live.py` | 用 `urllib` 直打 ElevenLabs Scribe（`scribe_v2`）與 Anthropic Messages API；任何失敗都退回離線，不拋例外；丟掉引用不存在的代碼或時間戳的模型輸出 |
| `skeleton/web/intake.html` | 共桌 intake 頁：一個內嵌 vanilla JS 的 HTML 檔，含 `?mock=1` 無後端模式 |
| `skeleton/demo_data/reference/occupations.json`、`jobs.json` | 三個職業的參考資料；六個代表性職缺（非真實職缺） |
| `skeleton/demo_data/canned/d7*.json`、`payloads.json` 內的 d7 情境 | stub 模型的罐頭輸出與示範情境 |

`skeleton/app.py` 另外接上 `/intake`、`/api/transcribe`、`/api/extract`、`/api/match`，
並在有 `ANTHROPIC_API_KEY` 時改用 `live.LiveModel`（失敗時退回 stub）。

```python
KEY = "d7"
METRIC = "evidence items mapped to a transcript line"

SUPPORTED_LANGUAGES = ("zh", "ar")   # 只列真的支援的，見 §7

def guard(payload):
    """四條紅線。raise，不回傳旗標 —— 呼叫端沒有忽略的選項。"""

def prepare(payload):
    """逐字稿 → 受限抽取任務的輸入。不是生成，不是評分。"""

def target_fields(payload):
    """anzsco_code、osca_code、qualification、units_evidenced。
    法規門檻（gate）不問模型，由 registry 查表附上。"""

def metric(shown, payload):
    """N 項已對映並指回逐字稿。"""
```

### `guard()` 的四條紅線

| # | 條件 | 行為 |
|---|---|---|
| 1 | payload 含 `country_of_origin`／`visa_status`／`protection_claim`／生物特徵欄位 | `raise RedLineError` |
| 2 | 缺 consent flag | `raise RedLineError` |
| 3 | `payload["language"]` 不在 `SUPPORTED_LANGUAGES` | `raise UnsupportedLanguageError`（**不靜默退回英文**） |
| 4 | 出現對「人」本身評分的欄位（非職缺吻合度） | `raise RedLineError` |

與方向 6 的 `check_aggregate()` 同一個位置、同一個原則：**拋例外，不是回傳旗標**。

## 5. 資料流（黃金路徑）

```
① 顧問與求職者共桌 → 求職者選語言（使用者選，不自動偵測）
      ↑ ElevenLabs 的語言偵測只在通話開始執行、無法中途切換，所以一律讓使用者選
② 母語口述工作史與學歷 → Scribe STT → 逐字稿（每句帶時間戳）
③ 即時雙語顯示 → 顧問看得懂、當場可追問
④ guard(payload)                        ← 模型之前
⑤ model.suggest() → Suggestion(value, reason, confidence, sources=(("transcript","t=03:12"),))
⑥ sort_by_confidence(threshold=0.6) → shown ｜ needs_human
⑦ 輸出 A（佐證包）＋ 輸出 B（媒合與履歷）
```

## 6. 三條失敗路徑（Working Prototype 15% 的關鍵，一定要演）

| # | 觸發 | 畫面行為 |
|---|---|---|
| 1 | 信心 < 門檻 | 欄位不自動填，標「需要顧問確認」，**附上它聽到的原句** |
| 2 | ASR 聽錯 | 顧問點該句可回放原音、修正，修正後重跑該欄位 |
| 3 | 語言不支援 | 明確拒絕畫面，說明支援哪幾種，**不靜默退回英文** |

第 3 條同時是加分的誠實：
> *"We shipped three languages, not seven, because ElevenLabs has no Tigrinya,
> Dari, Rohingya or Hazaragi voice. We will not fake a language we cannot pronounce."*

## 7. 語言支援清單（依 ElevenLabs 實際能力，不是願望）

**出貨的設定：`SUPPORTED_LANGUAGES = ("zh", "ar")`**（Tommy 2026-09-21 傍晚決定，取代原本的阿拉伯語／波斯語／史瓦希里語三語）。

| 語言 | 納入 demo | 理由 |
|---|---|---|
| 中文（Mandarin，送 Scribe 時用 `zho`） | ✅ 測試與錄影語言 | 團隊能逐字核對。ElevenLabs 對中文的準確率**未查證，不引用數字** |
| 阿拉伯語 `ar` | ✅ 設定語言 | **未經母語者驗證，不宣稱效果** |
| 波斯語 Farsi | ❌ 拒絕畫面 | 團隊沒人能核對；intake 頁保留此選項用來演示拒絕 |
| 史瓦希里語 | ❌ 拒絕 | 團隊沒人能核對 |
| 普什圖語 | ❌ 拒絕 | WER 25–50%「Moderate」，錯誤率太高 |
| **Dari／Tigrinya／Rohingya／Hazaragi** | ❌ 拒絕畫面（Tigrinya 在 intake 頁用來演示） | **不在 ElevenLabs 清單上** |

## 8. 那一個數字

> **「N 項經歷已對映並指回逐字稿、M 項待顧問確認、K 項必須送正式評估」**

對照基準：**AMES FY2024-25 的 8.5% 媒合率**（17,951 客戶 → 1,533 成效）。
講的是顧問每個案子省下的時間，**不是「AI 幫你找到工作」**。

## 9. demo 資料與誠實邊界

- ANZSCO 有上千個代碼。**手工整理 3 個**：aged care／welding-fabrication／commercial cookery
- **上台必須講**：「這是為 demo 手工整理的三個職業對映，不是完整 ANZSCO 圖譜。」
- 逐字稿使用**虛構示範案例**，不得使用任何真實個案資料
- stub 模型讓黃金路徑可離線跑完，**這同時就是 demo 備援**

## 10. 測試

沿用既有作法（`tests/`），新增：

- `guard()` 擋下四種紅線欄位各一個案例
- 缺 consent flag 被擋
- 不支援的語言回傳拒絕而非空值或英文
- 信心門檻分流正確
- 每個 `Suggestion` 必有 source（`schema.py` 已強制，補一個回歸測試）
- `metric()` 在空輸入時不爆炸

**驗證**：`bash bin/verify.sh` 必須維持 GREEN。

## 11. 相依套件 —— 零外部套件（已定案）

**出貨的堆疊只用 Python 標準函式庫 ＋ 一頁 vanilla JS，零外部套件、零建置步驟。**
真實 API（ElevenLabs Scribe、Anthropic Messages）在 `skeleton/core/live.py` 用 `urllib.request` 直打，
沒有安裝任何 SDK，因此不需要安裝核准。`skeleton/core/model.py` 的 stub 仍保留，作為沒有金鑰或
呼叫失敗時的退路，這本身是 demo 備援的一部分。
依 `CLAUDE.md`：往後若要安裝任何相依套件，仍須先取得 Tommy 明確核准，列出套件名稱與理由。

## 12. 工時分配建議

**分數集中在 Usability 15% ＋ Working Prototype 15% ＋ Effective Use of AI 15% = 45%**，
全部在 24 小時內做得出來，且指向同一個產出物。

| 優先序 | 工作 | 理由 |
|---|---|---|
| 1 | `d7_credentials.py` ＋ `guard()` ＋ 測試 | 主線，且紅線是 Effective Use of AI 的論證核心 |
| 2 | 三個職業的 ANZSCO／RPL 對映資料 | 沒有它佐證包是空的 |
| 3 | 共桌雙語逐字稿畫面 | Usability 的主場 |
| 4 | 三條失敗路徑 | Working Prototype 的主場 |
| 5 | **錄製備援影片** | 場地網路與現場噪音是 prototype 的標準死法 |
| 6 | B 線（媒合與履歷） | 地位平等但技術風險低，用同一份結構化資料生成 |

## 13. 未解事項

- **Problem Validation（10%）目前是零第一手來源。** 依專案規則不得宣稱有訪談。
  上台照講：*"Zero primary interviews so far. Here is our secondary evidence,
  here is our recruitment plan, here is the first provider we approach."*
- **TIS 的 HSP 供應商資格**：推論 HSP 供應商因年領 1.2 億澳幣而不符「無大額政府資助」，
  ⚠️ **上台前必須打開官網確認，不得直接宣稱。**
- **本方向的研究只有一輪、未經人工複驗。** 要念的每個數字上台前逐條開 URL 確認。
  不要引用的數字清單見框架檔與交接文件 8.5。
