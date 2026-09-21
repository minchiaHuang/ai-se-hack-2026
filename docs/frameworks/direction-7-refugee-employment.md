# 框架 — 方向 7：難民就業（口述經歷 → 佐證包 ＋ 媒合）

**2026-09-21 傍晚新增。這是選定的參賽題目。**
決策：方向 6 正式放棄（見 `docs/STATUS.md`），全力壓方向 7。

本檔填的是 `docs/superpowers/specs/2026-09-21-direction-frameworks-design.md` 的七格模板。
研究原始紀錄見 `docs/research-brief-2026-09-21.md` 第 6 節（三份 agent 報告全文證據與 URL）。

> ## ⚠️ 這份框架與方向 1–6 有一個重大差別
>
> 方向 1–6 都經過兩到四輪研究與競品盤點。**方向 7 的研究只有一輪**，
> 在 2026-09-21 下午由三個 agent 平行跑出，**沒有經過人工逐條複驗**。
> 上台前要念的每一個數字，必須自己打開原始 URL 確認一次。
> 「不要引用的數字」清單見本檔末，那一節比正文更重要。

---

## ⛔ 倫理紅線 —— 這條寫進程式，不只寫在文件

**不對人評分、不改名字、不評口音、不存結構化的身分欄位。**

對應 `skeleton/directions/d7_credentials.py` 的 `guard()`，
由 `skeleton/core/pipeline.py` **在呼叫模型之前**執行（與方向 6 的 `check_aggregate()` 同一個位置）。

四條會 `raise` 的紅線：

1. payload 含 `country_of_origin`／`visa_status`／`protection_claim`／生物特徵欄位 → 拒絕
2. 缺 consent flag → 拒絕
3. 使用者選的語言不在支援清單 → 回傳明確拒絕，**不靜默退回英文**
4. 任何對「人」本身的評分欄位（而非對「職缺吻合度」的分數）→ 拒絕

> ### ⚠️ 涵蓋範圍 —— 2026-09-21 計畫審查時發現，上台前必讀
>
> `guard()` 檢查的是**結構化欄位名稱**，不是口述內容。
> 求職者開口講出的原籍國、簽證、庇護細節**會進逐字稿、會送進模型**，
> 而且**音檔會先送到 ElevenLabs 這個第三方**。
>
> | 可以講 | 不能講 |
> |---|---|
> | 系統不設、也拒收任何身分欄位（原籍國、簽證狀態、庇護聲請、生物特徵） | 「我們不蒐集原籍國」 |
> | 我們的伺服器不落地保存逐字稿或音檔 | 「音檔當場刪除」「音檔不離開本機」 |
> | 送出給雇主必須求職者親手按下 | 「資料完全不外流」 |
>
> **ElevenLabs 的音檔保留設定**：計畫 Task 9 Step 4b 要求上台前查清楚，
> 查清楚之前**不得**宣稱零保留。

**最強的那句話（HRW 2021，EVIDENCE）**：孟加拉把**至少 83 萬筆**羅興亞人姓名與生物特徵
交給他們逃離的緬甸，難民發現後躲了起來。
https://www.hrw.org/news/2021/06/15/un-shared-rohingya-data-without-informed-consent

> 上台照念：*"For an asylum seeker, a database row is not a privacy inconvenience —
> it is a route back to the people they fled. So our system has no field for where
> someone came from, and it refuses one if you try to add it."*
>
> （原句「We designed for the day we get breached」已撤下：音檔會經過第三方，
> 這句話講得比我們實際做到的多。）

---

## 1. 一位使用者、一個時刻、一個被卡住的結果

**使用者**：**兩個人共桌**——安置機構（HSP／SETS／Workforce Australia 供應商）的
就業顧問，與一位沒有文件的難民求職者。一台電腦放中間。

**時刻**：第一次就業諮詢面談。顧問要在這一小時內弄清楚對方做過什麼。

**被卡住的結果**：
- 求職者的工作史**沒有任何文件背書**——母國的證書拿不到、營中的工作沒人發證、
  非正式受僱沒有紀錄。
- 顧問只能靠斷續的英文問答拼湊，寫出一份雇主看了無法判斷真偽的履歷。
- 雇主在篩選那一刻沒有可信資訊，於是把人當成風險，**在面試之前就刷掉**。

## 2. 斷點：最高成本的那一步

**把口述的、無文件的經歷，變成澳洲制度（雇主／RTO／評估機構）看得懂並且敢信的東西。**

⭐ **這個斷點有同儕審查的證據支持，這是本方向最強的一張牌：**

> **Guo & Tani, _British Journal of Industrial Relations_, 2026（UNSW）**，n=3,757
> （BNLA + HILDA，人道移民 2,155 ＋ 非難民移民 1,602，2013–2017 抵澳）。
> 難民抵澳時就業機率比其他移民**低約 88 個百分點**，五年後仍**低超過 51 個百分點**。
> 作者結論原話：
>
> *"differences in education and language explain some of the employment disadvantage
> faced by refugees in Australia, but the primary driver is discrimination by employers
> due to how they screen candidates **when they lack reliable information about overseas
> qualifications or experience**."*
>
> https://www.unsw.edu.au/newsroom/news/2025/11/refugees-Australia-employer-discrimination
> DOI https://doi.org/10.1111/bjir.70016

**這句話同時做三件事**：證明問題是真的；證明它是資訊／驗證問題（軟體打得到）；
而且**預先擋掉「你在修沒壞的那一端」這個質疑**——因為壞的那一端壞在缺資訊。

## 3. 理想的人類工作流（AI 之前）—— 閘門格

沒有 AI 的話，理想流程是：**一位雙語的、懂澳洲 VET 制度的專業人員，
花兩小時訪談，再花四小時把口述內容對映到 ANZSCO 與 RPL 單元。**

這件事政府做過，而且做得不好——見下方「政府自己試過」一節。
**流程本身是清楚的、可描述的**，所以通過閘門。瓶頸是**產能**，不是不知道該怎麼做。

## 4. AI 的受限任務

只挑一項（`AI_CONTEXT.md` 建構順序第 5 條）：**抽取（extraction）＋ 對映（mapping）**。

- **不是生成**：不編造求職者沒講過的經歷
- **不是評分**：不對人打分
- **不是決定**：信心不足就交給顧問

兩條輸入輔助：
- **語音轉文字**：ElevenLabs Scribe，讓求職者用母語口述（見「語言覆蓋」一節的限制）
- **即時雙語逐字稿**：顧問看得懂求職者在講什麼，**這是共桌場景，不是取代口譯**

## 5. 人類保留決定權的節點

| 決定 | 誰決定 |
|---|---|
| 這段經歷算不算數 | **顧問**（信心低於門檻的欄位一律進 `needs_human`） |
| 要不要送正式資歷評估（TRA／VETASSESS／ACS） | **顧問與求職者** |
| 履歷／佐證包要不要送出給雇主 | **求職者按下送出，否則什麼都不外流** |
| 錄用 | **雇主**。我們不參與，分數不給雇主看 |

## 6. 黃金路徑 ＋ 失敗路徑

**黃金路徑**（兩個人、一台電腦）：

```
① 顧問與求職者共桌，求職者選語言（使用者選，不自動偵測）
② 求職者用母語口述工作史與學歷 → Scribe STT → 逐字稿（每句帶時間戳）
③ 即時雙語顯示，顧問看得懂、可當場追問
④ guard() 檢查紅線 ← 在呼叫模型之前
⑤ 抽取 ＋ 對映 → 每個欄位一個 Suggestion(value, reason, confidence, sources=逐字稿第幾句)
⑥ sort_by_confidence → 高的顯示｜低的進 needs_human
⑦ 兩條輸出（地位平起平坐，2026-09-21 由 Tommy 拍板）：
     A. 佐證包：ANZSCO 代碼 ＋ VET RPL units of competency ＋ 每項要的證據
                ＋ 必須送 TRA／VETASSESS 的旗標
     B. 媒合與履歷：職缺吻合度 ＋ 依職缺需求調整的履歷
```

④⑤⑥ **已經是 `skeleton/core/pipeline.py` 現成的形狀，不必重寫。**

**三條失敗路徑（一定要演，這是 Working Prototype 15% 的關鍵）**：

1. **信心不足** → 不自動填，標示「需要顧問確認」，並附上它聽到的原句
2. **ASR 聽錯** → 顧問點該句回放原音、修正，修正後重跑該欄位
3. ⭐ **語言不支援** → 明確拒絕畫面，不靜默退回英文

## 7. 組織拿得走的一個數字

> **「N 項經歷已對映並指回逐字稿、M 項待顧問確認、K 項必須送正式評估」**

對照的基準線（EVIDENCE）：**AMES Australia FY2024-25 年報**，
Workforce Australia 服務 **17,951 名客戶 → 1,533 個 sustainable employment outcomes**，
即 **8.5% 的媒合率**。
https://www.ames.net.au/sites/default/files/2025-11/AMES%20Australia%20Annual%20Report%202024-2025.pdf

講的是**顧問每個案子省下的時間**，不是「AI 幫你找到工作」。

---

## 付費方與為什麼是現在

### ⭐ 最強的 why now：HSP 正在被 HISP 取代

- **OFFICIAL**：Home Affairs 的 **Humanitarian Integration and Settlement Program (HISP)**
  招標 **2025-03-06 截標**，結果**預計 2026 年初**。
  https://immi.homeaffairs.gov.au/settling-in-australia/settlement-policy-and-reform/refugee-and-humanitarian-settlement-sector-consultation
- 現行 HSP：年逾 **1.2 億澳幣**、年逾 **17,000 名客戶**、**5 家供應商 11 個合約區**。
  https://www.anao.gov.au/work/performance-audit/delivery-the-humanitarian-settlement-program
- **INFERENCE**：供應商此刻正在重新簽約、重設服務模式。預算與服務設計都在重畫的那一刻，
  一個能改善可申報就業成效的工具最容易進得去。

### 付費機制是現成的，不需要新預算科目

**OFFICIAL**：Workforce Australia 供應商按 **4 週／12 週／26 週成效付款**，
另有長期失業者加給，約 **75%** 的成效付款由 Services Australia 資料自動核銷。
https://www.dewr.gov.au/workforce-australia/resources/workforce-australia-employment-services-provider-payments

**INFERENCE**：提高安置率與 26 週留任率＝提高既有收入線。
賣法是**每位顧問一個席次授權**，買家角色是 Employment Services / Operations Manager。

### 買家名單（依優先序）

| 機構 | 規模（EVIDENCE） | 為什麼是他 |
|---|---|---|
| **SSI** | FY25 營收 **2.1196 億澳幣**，年服務 **67,000+ 人** | 委託了 Deloitte 的 Billion Dollar Benefit 報告，**問題敘事本來就是他家的** |
| **AMES Australia** | 17,951 Workforce Australia 客戶、6,656 HSP 客戶、**自家 13% 員工有難民背景** | VIC/SA/TAS 最大，8.5% 那個數字就是他們自己年報上的 |
| **Multicultural Australia** | QLD HSP 供應商 | 已有面向雇主的難民招募服務 |
| **SCOA**（峰層組織） | 非直接服務提供者 | **一次觸及幾乎所有供應商，最佳單一通路** |

⛔ **絕對不能說難民自己付錢。** 那會同時殺掉 Social Impact Reasoning 與 Pathway to Sustainability。

---

## 競爭態勢 —— 必讀，這裡有一條我們自己選擇承擔的風險

### 空的那一格（佐證包這條線）

**搜尋沒有找到任何同時滿足「難民」＋「澳洲」＋「AI 資歷對映」的產品。**
⚠️ 這句話的正確講法是「我們搜尋後沒有找到」，**不是「沒有人做」**。

相鄰但打不到這一格的：

| 產品 | 做什麼 | 為什麼打不到 |
|---|---|---|
| **SkillLab**（NL） | 最接近的競品。建在 **ESCO** 上（13,485 技能 → 2,942 職業），自適應訪談，**明文處理 informal learning**，已與 ILO、IRC、世銀合作部署 | **不在澳洲。** ESCO 對映搬不過來——這正是它不在澳洲的原因 |
| **Upwardly Global**（US） | 難民專用 AI 履歷與職涯助理 | **只做美國** |
| **EQPR**（歐洲理事會） | **無文件情況下評估資歷**，問卷＋45–60 分鐘真人訪談 | 歐洲，且靠真人 |
| **WES Gateway** | 無文件難民資歷評估 | **只有美加** |
| **Talent Beyond Boundaries** | Talent Catalog，15.5 萬人註冊，自動產生 CV，開源 | 做**境外技術難民簽證通道**，不是境內無文件經歷 |
| **Global Talent Pathway** | 澳洲自有，13.5 萬求職者，做資歷驗證與技能評估 | ⚠️ **最接近的澳洲對手，必須自己先講** |

**澳洲的制度是鎖死的護城河**：ANZSCO、VET RPL、ASQA、Country Education Profiles、
TRA／VETASSESS／ACS 的分工，全是澳洲專有，不能移植。

### ⚠️ 滿的那一格（媒合與履歷這條線）—— 我們明知有人做，仍選擇做

**2026-09-21 由 Tommy 拍板：佐證包與媒合兩條線地位平起平坐，都是正式功能。**
文件必須誠實記錄這個決定承擔了什麼風險。

| 競品 | 狀態 |
|---|---|
| **Jobright.ai** | 美國限定，免費層 ＋ 約 US$19.99–39.99/月。被抱怨 resume AI 會幻覺 |
| Simplify / LazyApply / AIApply / Careerflow | 全在跑，價格從免費到 US$129/年 |
| **Kickresume／AIApply 履歷翻譯** | **免費**，十秒出結果 |
| ⛔ **Home Affairs Free Translating Service** | **澳洲政府免費翻譯 10 份官方文件**，簽證核發後兩年內，**明文含教育與就業文件** |
| **JobSparrow**（AU/NZ） | 澳紐本地，AI 履歷＋模擬面試＋媒合分數，**明文鎖定 migrants**，落地才付費 |

**Sonara 已經死過一次**（2024-02 募資失敗倒閉，2026 由新東家重開）——
這一格不只滿，而且養不活。

### 被問到「已經有人做了」時，照這個順序答

評分標準**沒有新穎性這一項**，所以「有人做了」不是淘汰理由。但**不要否認競品存在**：

1. **承認它存在，而且講得比對方清楚**（我們有完整競品表）
2. **競品證明需求是真的**——有人免費做、有人收費賣得掉
3. **說出具體不一樣的那一點**：
   - 佐證包這條線：**澳洲制度鎖死，SkillLab 的 ESCO 對映搬不過來，這就是它不在澳洲的原因**
   - 媒合這條線：**老實說這一格是滿的。我們做它是因為共桌訪談已經產出結構化資料，
     再生一份履歷是零邊際成本的副產品。我們不主張在這一格贏。**
4. **標明哪些是賭注、哪些有證據**

### ⛔ 一個警訊

**澳洲唯一那家難民求職新創 Refugee Talent 已經死了。**
agent 直接 fetch `refugeetalent.com`：HTTP 200，但標題是印尼的賭博網站——網域過期後被接管。
共同創辦人現在在 Pathway Club。**空位是真的，但那是「很難養活」的證據，不是沒人想到。**

---

## 政府自己試過，而且做得不好 —— 這是打我們的棍子，要自己先拿起來

**DSS／Deloitte《Career Pathways Pilot for Humanitarian Entrants》期中評估**
（2017-03 – 2019-06，六個據點，**已結案**）
https://immi.homeaffairs.gov.au/settlement-services-subsite/files/career-pathways-pilot.pdf

- 預算 **520 萬澳幣**，服務交付實支 **450 萬澳幣**
- **只招到 784 人，是目標的 65%**。供應商達成率差距極大：SSI 88%、Navitas 48%、
  atWork 31%、Multicultural Australia 23%
- **只有 11–17% 的參與者回到抵澳前的職業**；19% 進入相關工作
- 單場成本 **181–622 澳幣**，CatholicCare 單人投入**超過 5,000 澳幣**
- 評估指出的問題：供應商間溝通不良、申報要求不清、試辦期太短、資源不足

> **照講**：*"The Government spent $4.5 million on exactly this problem and moved
> 11 to 17 per cent of people back into their own occupation. We are not claiming
> we beat that with a laptop. We are making those same caseworkers faster."*

這份報告同時是我們**斷點證據**的來源（見下節），所以它既是棍子也是武器。

---

## 可引用的證據（每一條都附 URL，上台前逐條複驗）

### 五個最強的數字

1. **人道簽證持有者領失業給付的比例是技術移民的約 12 倍——20.1% vs 1.7%**
   （ABS Migrant Settlement Outcomes，PLIDA，參考年 2022–23）
   https://www.abs.gov.au/statistics/people/people-and-communities/migrant-settlement-outcomes/latest-release
2. ⭐ **難民抵澳時就業機率低約 88 個百分點，五年後仍低超過 51 個百分點；
   同儕審查結論是主因為雇主在無法驗證海外資歷時的篩選行為**
   （Guo & Tani, BJIR 2026，n=3,757）
   https://www.unsw.edu.au/newsroom/news/2025/11/refugees-Australia-employer-discrimination
3. **44% 的移民與難民從事低於自身技能水準的工作，一年損失 90 億澳幣、約 44,000 個職位；
   報告明文指出人道入境者受影響更嚴重**
   （Deloitte Access Economics for SSI，2024-06）
   https://www.ssi.org.au/media-centre/media-releases/billion-dollar-benefit-new-report-identifies-five-ways-to-harness-untapped-skilled-workforce/
4. **政府 450 萬澳幣的 Career Pathways Pilot 只讓 11–17% 的人回到原職業，
   招募僅達目標 65%，單人成本最高逾 5,000 澳幣**（見上節 URL）
5. **AMES Australia FY2024-25：17,951 名客戶 → 1,533 個成效，8.5% 媒合率**
   https://www.ames.net.au/sites/default/files/2025-11/AMES%20Australia%20Annual%20Report%202024-2025.pdf

備用第六條：**抵澳 3–6 個月僅 6% 的人道移民有支薪工作，約 18 個月升至 16%，
約 2.5 年升至 23%**（BNLA，n=2,399）https://aifs.gov.au/building-new-life-australia

### 具體摩擦點（全部出自 Career Pathways Pilot 評估 §5.5.1，可直接引述）

- **文件拿不到**：*"retrieving hard copy documents from overseas can be challenging and time consuming"*
- **沒有澳洲推薦人**：參與者要的是短期實習，為了取得澳洲經驗**與推薦人**
- **卡在篩選階段**：部分參與者認為困難主要在**通過初篩、拿到面試**，
  因為雇主覺得人道入境者**"more risky"**
- **履歷協助是前三高需求**：**42%** 的受訪者使用過「履歷、求職申請與面試協助」
  （第三高，僅次於職涯建議 50%）
- **再認證時程被收入壓力拖垮**：某案本應六個月完成，因短期工作需求**拖成三年**
- **駕照**是具體門檻，試辦計畫的財務補助涵蓋駕照、電腦與國際無犯罪紀錄證明

### 一個可以整段講的案例（同一份報告）

阿富汗牙醫，**6 年臨床 ＋ 7 年教學**，卡住的原因是**拿不到母國一份政府文件**，
無法報考澳洲牙醫公會考試；同時又因為「沒有澳洲經驗」被牙助職缺拒絕。
最後只能在診所無薪當「見習生」。

### 資歷認證的實際成本（OFFICIAL）

- **VETASSESS 完整技能評估（申請人在澳洲境內）：1,205.60 澳幣含 GST**；
  優先處理加收 907.50 澳幣；標準處理 **8–12 週**
  https://www.vetassess.com.au/skills-assessment-for-migration/professional-occupations/skills-assessment-fees-for-professional-occupations
- **INFERENCE**：對照人道移民抵澳前五年的中位數所得 **25,183 澳幣**，
  1,206 澳幣約等於年所得的 **4.8%**。這是硬門檻，不是小麻煩。

### 一個已關閉的服務缺口（why this gap exists）

**NSW Refugee Employment Support Program (RESP) 已於 2024-06-30 結束。**
5 年 **3,450 萬澳幣**，協助逾 **10,000 人**，
**近 30% 取得持續就業**，對照全國基準「抵澳 18 個月後 17% 有支薪工作」。
結束後參與者轉入聯邦主流服務。
https://www.ssi.org.au/media-centre/media-releases/nsw-government-extends-employment-support-program-for-refugees/

**INFERENCE**：NSW 專屬的難民就業計畫現在不存在了，難民走的是主流 Workforce Australia，
而 RCOA 對該系統有長期公開批評。這是一個有名有日期、可查證的服務缺口。

---

## 語言覆蓋 —— 自己先講，不要等評審發現

**EVIDENCE，ElevenLabs 官方文件：**

| 能力 | 覆蓋 |
|---|---|
| Scribe STT（聽） | 90+ 語言。**阿拉伯語 WER 10–20%「Good」；波斯語／史瓦希里語 5–10%「High」；普什圖語 25–50%「Moderate」** |
| Agents（說） | 「All」設定為 **31 種語言** |
| ⛔ **不在清單上** | **Dari、Tigrinya、Rohingya、Hazaragi** |
| ⛔ 限制 | 語言偵測**只在通話開始時執行，無法中途切換** |

https://elevenlabs.io/docs/overview/capabilities/speech-to-text
https://elevenlabs.io/docs/help-center/product/eleven-agents/which-languages-can-i-use-with-eleven-agents

**INFERENCE**：能聽約 90 種、能說約 31 種，而**最需要的幾個語言剛好都在缺口上**。

> **照講**：*"We shipped three languages, not seven, because ElevenLabs has no Tigrinya,
> Dari, Rohingya or Hazaragi voice. We will not fake a language we cannot pronounce."*

這句話把產品缺口轉成可信度。

---

## TIS National —— 語音功能的生死線

**OFFICIAL**：TIS National 免費口譯服務只對**列舉式的機構清單**免費：
私人執業且提供 Medicare 給付服務的醫療從業者、藥局、
**沒有大額政府資助的 NGO 個案與緊急服務**、房仲、地方政府、工會、國會議員辦公室、
特定 LGA 的部分聯合健康專業人員。
**雇主、職業介紹所、就業服務供應商與個別求職者不在清單上。**
https://www.tisnational.gov.au/en/Our-services/Free-Interpreting-Service/About

**兩個推論，強度不同：**

- **INFERENCE（可用，但要標明是推論）**：HSP 供應商一年領 1.2 億澳幣，
  很可能**不符合**「沒有大額政府資助」這一條。⚠️ **上台前必須打開官網確認，不得直接宣稱。**
- **紅線（已確認）**：任何有後果的通話（Centrelink、法律、醫療、合約）
  一律導去 **TIS 131 450**。**我們不自稱口譯員。**

> **照講**：*"For any consequential conversation, we route to TIS on 131 450.
> We are not an interpreter. We are a structured intake tool for a conversation
> that is already happening, with both people at the same table."*

**我們的場景與 TIS 不衝突的理由**：我們不是取代一通電話口譯，
我們是在**同一張桌子上**把已經在發生的對話變成結構化資料。

---

## 九條倫理紅線 —— 在評審問之前自己講

| # | 紅線 | 證據 |
|---|---|---|
| 1 | **不對人評分、排名、評級** | 華盛頓大學 AAAI-AIES 2024：300 萬組測試，LLM 履歷排序器偏好白人關聯姓名達 **85%**；黑人男性姓名在近 100% 組合中被劣後 https://arxiv.org/abs/2407.20371 |
| 2 | **不改名字、不隱藏背景去騙過濾器** | ANU 實地實驗，4,000+ 份配對履歷：Anglo 姓名回電率 **35%**、中東 **22%**、華人 **21%**、原住民 26%、義大利 32% https://openresearch-repository.anu.edu.au/items/883c3559-be22-4d22-931a-16cf3e49977c |
| 3 | **不評估口音或流利度** | Koenecke et al., PNAS 2020：五套商用 ASR，黑人說話者 WER **0.35** vs 白人 **0.19** https://www.pnas.org/doi/10.1073/pnas.1915768117 。2025-03 ACLU 科羅拉多對 Intuit 與 HireVue 提出 EEOC 申訴（聾人原住民申請者被 AI 面試刷掉） |
| 4 | **AI 供應商已經在被告** | **Mobley v. Workday**：2025-05-16 聯邦法院認證全國性 ADEA 集體訴訟，原則是**AI 供應商即使沒做最終錄用決定也可能直接負責** https://www.hklaw.com/en/insights/publications/2025/05/federal-court-allows-collective-action-lawsuit-over-alleged |
| 5 | **刻意站在法規分類之外** | EU AI Act **Annex III 第 4 點**把招募／篩選／評估候選人的 AI 列為高風險，義務自 **2026-08-02** 適用 https://artificialintelligenceact.eu/annex/3/ 。NYC **Local Law 144** 要求 AEDT 年度獨立偏誤稽核、公開結果、提前 **10 個工作天**通知候選人 |
| 6 | **澳洲觀點：偏誤是反歧視法問題，不是技術問題** | AHRC ＋ Gradient Institute ＋ CSIRO Data61《Using AI to make decisions: addressing the problem of algorithmic bias》 https://humanrights.gov.au/resource-hub/by-resource-type/publications/technical-paper-addressing-algorithmic-bias ⚠️ 澳洲的強制性規範**尚未立法**，不得宣稱它是法律 |
| 7 | **會害死人的資料** | HRW 2021 羅興亞案（見本檔開頭紅線） |
| 8 | **不自稱口譯員** | TIS National（見上節） |
| 9 | **高風險決定保留人類權限** | `AI_CONTEXT.md`「Avoid」：不得自動化福利、醫療、危機或資格判定 |

**第 1 條與媒合線的關係（必須講清楚）**：
`match rate` 評的是**職缺與經歷的吻合度**，不是評人，而且沒有人因此被刷掉。
**這個分數不給雇主看。** 一旦雇主拿它篩人，就掉進第 4 條那個形狀。

---

## 評審七題的答法

| 標準 | 權重 | 怎麼拿分 | 最可能的質疑 |
|---|---|---|---|
| **Problem–Solution Fit** | **20%** | 講**具名的窄切口**：西雪梨、抵澳 1–3 年、有海外技術或照護經驗、在安置供應商案量裡的人道入境者。用 Guo & Tani 證明斷點在資訊驗證 | ⚠️ *「澳洲證據說壞的是雇主那端，你為什麼修求職者？」* —— **答案就是 Guo & Tani 那句話：雇主壞在缺可信資訊。** 這題答不好會掉 20% 並波及 Social Impact |
| **Usability** | 15% | 兩個人共桌、不用打字、開場先選語言、大觸控目標、ASR 聽錯可回放修正 | *「有沒有非英語母語者實際用過？」* 最便宜的補法：現場找 ESL 測試者跑兩三次，錄 90 秒螢幕影片 |
| **Working Prototype** | 15% | 讓評審自己動手；演**三條失敗路徑**，證明是工程不是 demo 路徑 | *「這是不是 Lovable/Base44 包一個 API 呼叫？」* → 秀 `guard()`、信心分流、source 強制。**備援影片一定要錄** |
| **Effective Use of AI** | 15% | 這一項評的是**適當性**，所以最強的動作是展示一個刻意的**「不」**：「這裡用 AI；這裡刻意不用，因為〔紅線證據〕」 | *「語音是為了贊助商獎硬加的嗎？」* → 語音必須是**主要輸入介面**，不是文字 app 上的喇叭圖示 |
| **Social Impact Reasoning** | 15% | 明確因果鏈與可測代理指標：N 次訪談 → 面試出席與 offer 轉換 → 4/12/26 週留任，對照供應商自己的基準世代。**說出什麼會證偽它** | *「你只是在訓練人去迎合一個有偏誤的系統？」* → 部分是，所以我們拒絕改名字，並把重複出現的資歷落差彙總回饋給雇主端 |
| **Problem Validation** | 10% | ⚠️ **目前是零第一手來源。** 照專案規則不得宣稱有訪談 | 正確打法：*"Zero primary interviews so far. Here is our secondary evidence, here is our recruitment plan, here is the first provider we approach."* 薄但誠實，扣分少於被戳破 |
| **Pathway to Sustainability** | 10% | HISP 重簽視窗 ＋ 4/12/26 週成效付款 ＋ 具名買家（SSI／AMES） | *「NFP 沒有軟體預算、採購週期 12 個月」* → 用成效付款的算術答，並提供在單一供應商既有案量內的免費試點 |

**分數集中處**：Usability 15% ＋ Working Prototype 15% ＋ Effective Use of AI 15% = **45%**，
全部在 24 小時內做得出來，而且指向同一個產出物。**工時壓在這裡。**

---

## demo 資料來源與誠實邊界

- ANZSCO 有上千個職業代碼。**我們手工整理 3 個**：
  建議 aged care／welding-fabrication／commercial cookery
  （難民就業高頻 ＋ 澳洲缺工）。
- **上台必須講**：「這是為 demo 手工整理的三個職業對映，不是完整 ANZSCO 圖譜。」
- 逐字稿使用**虛構的示範案例**，不得使用任何真實個案資料。
- 與方向 6 同一個作法（見 `direction-6-wise-outcomes.md`「demo 資料來源與誠實邊界」）。

---

## ⛔ 不要引用的數字 —— 這一節比正文重要

| 不要講 | 為什麼 |
|---|---|
| **ABS 的 60.4%** 說成「就業率」 | 那是 PLIDA 的「有個人所得」比例，不是就業率。**能講的是 20.1% vs 1.7% 的失業給付差距** |
| **CEDA 的 25% ／ 12.5 億澳幣** 套在難民身上 | 那份報告只涵蓋**永久技術移民**，沒有難民數字 |
| **Woolworths 雇用 150 名難民** 當成現況 | 那是 **2020 年**的數字。2026 年的總數 **NOT FOUND** |
| **IKEA／Accor／Marriott／Compass** 說成澳洲 Tent 成員 | **未驗證**。Tent 的澳洲成員名單未公開 |
| 任何**競品價格** | 多來自 SEO 比較站，**不要放簡報** |
| 人道入境者專屬的**技能錯配百分比** | Deloitte 只說「更嚴重」，**從未單獨量化**。NOT FOUND |
| 「**沒有人做這件事**」 | 只能講「我們搜尋後沒有找到」 |
| 澳洲 AI 強制性規範「**是法律**」 | 截至 2026 年中仍未立法 |
| MDA Ltd／CareSeekers／Jesuit Refugee Service 的規模 | 本輪**未驗證**，不要引用 |

### 公開資料裡本來就不存在的三個缺口（可以當論據，不得自己估數字）

1. **澳洲沒有任何官方來源可以說出「難民失業率是 X%」。**
   ABS Migrant Settlement Outcomes 只有所得與給付代理指標；
   ABS Characteristics of Recent Migrants 最新版停在 **2019-11** 且不分離人道簽證；
   BNLA 是唯一真正的就業序列，最後一波是 2023。
2. **Workforce Australia 不公布依人道簽證身分分項的成效。**
   RESP 於 2024-06-30 結束後，NSW 難民在主流系統中的表現**公開不可測**。
3. **沒有任何公開數字說明難民走完海外資歷認證的成本、時間或放棄率。**
   VETASSESS 有費用與名目時程，但沒有人公布有多少人道入境者開始、完成、
   或在文件拿不到時放棄。

> **INFERENCE，可以上台講**：管不了沒被量的東西。
> 這三個缺口本身就解釋了為什麼供應商申報的是活動量而不是成效。

---

## 現場要問提案者的三個問題

若明天現場有難民／多元文化背景的社企或 mentor：

1. 你最近一個求職者，是在**哪一步**卡住的？（聽是不是落在「篩選前」）
2. 他的經歷**有沒有文件**？沒有的話你們現在怎麼處理？
3. 你們有沒有做過 **RPL**？誰付那筆錢？

⚠️ **依 `AI_CONTEXT.md`「Interview rules」，任何對外接觸需 Tommy 當下核准。**
不得宣稱已完成訪談。
