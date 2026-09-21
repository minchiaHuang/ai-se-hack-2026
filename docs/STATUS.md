# STATUS

單行狀態：2026-09-21 Day 1 傍晚。**題目改為方向 7：難民就業（口述經歷 → 佐證包 ＋ 媒合）。**
方向 6（WISE 就業成效申報）**正式放棄**，研究與證據原封保留為備案。
方向 7 的一輪研究已完成（三個 agent 平行），框架、交接文件第 8 節、spec 皆已落檔。
**現場優先原則仍凌駕一切。**

最後驗證：2026-09-21（`bash bin/verify.sh` → GREEN，含 25 個骨架測試）

## 進行中

- ⭐ **題目：方向 7 —— 難民就業**，2026-09-21 傍晚由 Tommy 決定。
  - 框架：`docs/frameworks/direction-7-refugee-employment.md`
  - 研究原始紀錄：`docs/research-brief-2026-09-21.md` **第 8 節**
  - 實作 spec：`docs/superpowers/specs/2026-09-21-direction-7-design.md`

- **產品形狀**：兩個人共桌、一台電腦放中間。難民用母語口述工作史 →
  ElevenLabs Scribe 轉逐字稿 → 即時雙語顯示給 NGO 顧問看 → 抽取與對映 →
  **兩條平起平坐的輸出**：
  - **A. 佐證包**：ANZSCO 代碼 ＋ VET RPL units of competency ＋ 每項要補的證據
    ＋ 必須送 TRA／VETASSESS 的旗標
  - **B. 媒合與履歷**：職缺吻合度 ＋ 依職缺需求調整的履歷（Jobright 形狀）

- ⭐ **最強的一張牌**：Guo & Tani, _British Journal of Industrial Relations_, 2026（UNSW），
  n=3,757。難民抵澳時就業機率低約 **88 個百分點**，五年後仍低超過 **51 個百分點**，
  同儕審查結論是**主因為雇主在無法驗證海外資歷時的篩選行為**。
  這句話同時證明問題真實、證明它是軟體打得到的資訊問題、
  並預先擋掉「你在修沒壞的那一端」這個最危險的質疑。

- ⚠️ **明知承擔的風險（Tommy 2026-09-21 拍板）**：B 線所在的車道是滿的——
  Jobright、Simplify、LazyApply、Careerflow；Kickresume／AIApply **免費**翻履歷；
  **澳洲政府自己免費翻 10 份官方文件**；JobSparrow 在澳紐已鎖定 migrants。
  決定仍做兩條線。差異化主張**只放在 A 線**（澳洲制度鎖死，SkillLab 的 ESCO 對映搬不過來）。
  答法照 spec §3。

- **語音的位置是輸入端**，不是朗讀、不是口譯。理由：求職者沒有文件、也打不出英文，
  **口述是唯一可能的輸入方式**，所以語音是必要的而非裝飾的。
  ⛔ 不做 AI 口譯通話：TIS National 有免費真人口譯，踩下去就死。

- **語言覆蓋是跛的，要自己先講**：ElevenLabs Scribe 能聽約 90 種、Agents 能說約 31 種，
  但 **Dari／Tigrinya／Rohingya／Hazaragi 不在清單上**，普什圖語 WER 25–50%。
  demo 只上阿拉伯語／波斯語／史瓦希里語三種，其餘走明確拒絕畫面。

- **待實作**：`skeleton/directions/d7_credentials.py`（唯一要新增的檔案）。
  `pipeline.py` 與 `schema.py` **不改**，既有形狀完全吐合。

## 已知問題

- ⚠️ **方向 7 的研究只有一輪，且未經人工逐條複驗。** 方向 1–6 都跑過二到四輪。
  上台前要念的每個數字必須自己打開原始 URL 確認。
  **「不要引用的數字」清單見交接文件 §8.5 與框架檔末，那一節比正文重要。**
- ⚠️ **Problem Validation（10%）目前是零第一手來源。** 沒有訪談、沒有現場提案者、
  沒有親身經驗。題目來源是「團隊覺得這個題目好」。
  依專案規則**不得宣稱有訪談**。正確打法是上台直接承認並給出次級證據與接觸計畫。
- ⚠️ **TIS 的 HSP 供應商資格是推論，未驗證。** 推論 HSP 供應商因年領 1.2 億澳幣
  而不符「無大額政府資助」這一條，**上台前必須打開官網確認，不得直接宣稱**。
- 真實模型 API 尚未接。`skeleton/core/model.py` 仍是 stub，介面已備妥。
  **安裝任何相依套件需先取得核准。**

## 備案：方向 1–6

**全部原封保留，一個字都沒刪。** 方向 6 的兩輪深度研究（Impact Costs 報告全文、
White Box Enterprises 與 Seedkit 的答案、SEDI 付費論證、Social Traders 認證格式）
仍在 `docs/frameworks/direction-6-wise-outcomes.md` 與交接文件第 5 節。
明天現場若聽到社企講 WISE 申報，那仍是手上唯一有兩輪證據支撐的彈藥。

## 更名紀錄（2026-09-21）

- GitHub repo：`AI_Social_Enterprise_Hackathon_2026` → `ai-se-hack-2026`
  （https://github.com/minchiaHuang/ai-se-hack-2026，PRIVATE）
- 本地資料夾同步更名為 `ai-se-hack-2026`。
- GitHub 會 redirect 舊 URL，但隊友若已 clone 應改用新 URL。
- `.claude/orca-flow.json` 的 `"project"` 仍是賽事全名，那是顯示字串不是路徑，刻意不動。

## 下一步

1. **實作 `skeleton/directions/d7_credentials.py`** —— guard() 四條紅線 ＋ prepare ＋
   target_fields ＋ metric。詳見 spec §4。
2. **整理三個職業的 ANZSCO／RPL 對映資料**（aged care／welding-fabrication／
   commercial cookery）。沒有它佐證包是空的。
3. **共桌雙語逐字稿畫面**（Usability 15% 的主場）。
4. **三條失敗路徑**：低信心扣住值、ASR 聽錯可回放修正、語言不支援明確拒絕
   （Working Prototype 15% 的主場）。
5. ⭐ **錄製 demo 備援影片。** 場地網路與現場噪音是 prototype 的標準死法。
6. **B 線（媒合與履歷）** —— 用同一份結構化資料生成，技術風險低。
7. **上台前逐條複驗要念的 5–6 個數字**，打開原始 URL 確認。
8. 確認要不要接真實模型 API；若要，先列出套件名稱與理由取得核准。

**現場優先**：現場出現的真實問題，一律優先於上述任何方向（判準見交接文件第 7 節）。
現場那張要拿在手上的是 **`docs/frameworks/onsite-matching-sheet.md`**。

## 框架與骨架（2026-09-21 新增，分支 `feat/direction-frameworks`）

- 設計規格：`docs/superpowers/specs/2026-09-21-direction-frameworks-design.md`
- 三份框架（同一個七格模板的三個實例）：`docs/frameworks/direction-{2,3,6}-*.md`
- **現場提案者辨識表**：`docs/frameworks/onsite-matching-sheet.md`
- 技術骨架：`skeleton/`，跑法 `python3 skeleton/app.py` → http://127.0.0.1:8000
  （`python3 -m skeleton.app` 也可；`--check` 為離線煙霧測試，不起伺服器）
  - 一個殼、三個可插拔方向模組、一條共用管線
  - **零外部套件、單次模型呼叫、不做 RAG／agent／vector DB**（`AI_CONTEXT.md`「Avoid」）
  - stub 模型使黃金路徑可離線跑完，這同時就是 demo 備援
  - 兩條寫進程式而非只寫在文件的保證：無來源的建議會被拒絕；低於信心門檻就扣住值改問人
  - 方向 6 的倫理紅線在模型呼叫**之前**強制：個人層級欄位與小於 5 人的群體一律拒絕輸出
  - demo 場景含兩條失敗路徑：低信心（扣住值）與群體過小（拒絕輸出）

## 背景

完整專案脈絡見 `AI_CONTEXT.md`（官方賽事事實、評審、研究過的問題領域、策略方向、角色分工）。
