# STATUS

單行狀態：2026-09-21 晚。**方向 7 共 21 個 PR 已合入 `docs/direction-7-refugee-employment`（第一波 #5 d7-core、#3 d7-match、#2 d7-live、#4 d7-intake-ui；第二波 #6 d7-wire；#7 d7-resume 職缺板與逐職缺履歷；#8 d7-docs 給評審的英文 README；#9 d7-entry 起始畫面：口述或帶履歷兩個入口；#10 d7-docs2 README 補上起始畫面；#11 d7-jobs 職缺頁：全部範例職缺、平台式版面、佐證與逐字稿分頁；#12 d7-adzuna Adzuna 雪梨職缺快照工具（30 筆、25 筆有單元、106 個單元）；#13 d7-validation-docs 問題驗證數字改用官方來源；#14 d7-flow 履歷入口一步完成、職缺板獨立成 `/jobs` 頁；#15 d7-adzuna-quotes 抓取重試與引文要指名單元；#16 d7-real-jobs 職缺板改用真實 Adzuna 廣告並附上每個單元的原文出處；#17 d7-pdf-upload 可讀取文字型 PDF 履歷（純標準函式庫）；#18 d7-quotes 同一段廣告引文最多對應兩個單元、`?mock=1` 改顯示真實 Adzuna 職缺板；#19 d7-iv-api 面試題目、翻譯與朗讀 API（新增選用環境變數 `ELEVENLABS_VOICE_ID`）；#20 d7-topcard 拿掉 demo 首張職缺卡（廣告 5870142114）較弱的食品安全引文；#21 d7-review 顧問用的履歷審閱頁 `/review` 與 `/api/resume-sections`；#22 d7-iv-page 面試頁 `/interview`：朗讀題目、錄音、原文＋英文，再交給 `/review`，合併點 `5e1fe54`），`/intake` 與三條 API 已接上。**
題目為方向 7：難民就業（口述經歷 → 佐證包 ＋ 媒合）。
方向 6（WISE 就業成效申報）**正式放棄**，研究與證據原封保留為備案。
方向 7 的一輪研究已完成（三個 agent 平行），框架、交接文件第 8 節、spec 皆已落檔。
**現場優先原則仍凌駕一切。**

最後驗證：2026-09-21（`bash bin/verify.sh` → GREEN，含 244 個骨架測試，於 `5e1fe54`）

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
  demo 用中文錄影、阿拉伯語保留為設定語言，其餘走明確拒絕畫面（見下方 Tommy 的決定）。

- ⭐ **實作計畫已完成並經審查**：`docs/superpowers/plans/2026-09-21-direction-7-implementation.md`
  九個 task、全程 TDD，**切線在 Task 6 之後**。計畫內的程式碼已原封貼進拋棄式副本實跑，
  **54 個測試全過、離線 `--check` 兩種啟動方式皆通過**。
  - 審查修掉 1 個 BLOCKER（單元代碼格式檢查漏了 7 字母前綴 `SITHCCC`／`SITXFSA`）
    與 4 個 SERIOUS（閘門被渲染成空白、來源檢查被誤稱為現行狀態查核、
    切線前 demo 的限制、紅線措辭超出實際涵蓋）。
  - 審查 agent 本身撞到帳號用量上限（HTTP 429，19:10 重置）未完成，改由主 session 實跑審查。
- **參考資料全部到齊且已驗證**（ANZSCO 2022 ＋ OSCA 2024 ＋ VET 資格與單元，三個職業）。
  兩個要記住的：**ANZSCO 已被 OSCA 取代但移民系統仍用 ANZSCO → 兩組都帶**；
  **`MEM31922` 於 2025-09-04 被 `MEM31925` 取代**。
- **技術堆疊定案**：Python 標準函式庫 ＋ 一頁 vanilla JS，**零外部套件、零建置步驟**。
  真實 API 用 `urllib.request` 直打，**因此不需要安裝核准**。
- **2026-09-21 傍晚，Tommy 的決定（以此為準）**：
  - **Demo 語言（最終）：中文測試與錄影，阿拉伯語保留為設定語言**，`SUPPORTED_LANGUAGES = ("zh", "ar")`，
    其餘語言一律拒絕畫面。台詞：*"We recorded this in Mandarin because it is the language we could verify
    word for word. Arabic is configured, but we have not validated it with a native speaker, so we do not claim it."*
    ElevenLabs 對中文的準確率**未查證，不得引用數字**。（先前的「只用阿拉伯語」已被此決定取代。）
  - **今晚範圍 = 原計畫 ＋ 課程推薦**（課程推薦從 `missing` 單元推出，框為 RPL 的 gap training）。
  - **訪談只問工作與學習，不問逃亡經歷**；就算求職者自己講了也不抽取。
  - **四個 worker 平行開發**（orca-flow，疊在本分支上）：`d7-core`、`d7-live`、`d7-match`、`d7-intake-ui`；
    第一波合併後再開 `d7-wire` 接路由。推送一律由 Tommy 手動。
- **隊友的五階段設計流程**（企業入駐／通道 A＋B／SWOT＋課程／匹配投遞／手機模擬面試）：
  今晚只做與本計畫重疊的**階段二通道 A ＋ 階段四**，其餘當 pitch 的 roadmap 畫面。
  ⚠️ 兩處風險 Tommy 決定暫不處理、記錄在此：**SWOT 的「劣勢／威脅」是對人評分**（九條紅線第 1 條）；
  **企業付費＋企業自訂欄位＋一鍵投遞**會讓產品落入雇主篩選工具的法規形狀（EU AI Act Annex III、Mobley v. Workday），
  且與研究找到的付費方（安置機構）不同。roadmap 畫面若出現這兩項，評審可能追問。
- **Tommy 2026-09-21 的兩個決定**：AI 維持判斷職業與代碼（不收窄）；
  工作順序維持先語音後抽取，**切線前 demo 以錄影為準、照罐頭情境講**。

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

## 下一步 —— 新 session 從這裡接手（2026-09-21 晚）

**目標：今晚做完全部 web code，明早錄影。** 前一個 session 是 manager，因 context 滿了交接。

1. **Tommy 手動推送本分支**（hook 擋所有 Claude 的推送）。確認計畫已在遠端：
   `git cat-file -e origin/docs/direction-7-refugee-employment:docs/superpowers/plans/2026-09-21-direction-7-implementation.md`
2. **新 session 切成 bypassPermissions**，以 orca-flow manager 角色同時開第一波 4 個 worker。
   brief 已寫好，存在共用狀態目錄（所有 worktree 都看得到）：
   ```
   D=/Users/tommyhuang/Desktop/Projects/Hackathon/ai-se-hack-2026/.git/orca-flow/pending-briefs/2026-09-21-d7
   S=~/.claude/skills/orca-flow/scripts/spawn_worker.py
   for w in d7-core d7-live d7-match d7-intake-ui; do
     python3 $S --name $w --brief $D/$w.md --base origin/docs/direction-7-refugee-employment --bypass
   done
   ```
   Bash timeout 600000。`--dry-run` 已驗證通過。
   ⚠️ 帳號用量上限曾觸發（HTTP 429，19:10 重置）；若 worker 一啟動就 429，等重置再開。
3. **Worker 完成時卡片顯示 `READY:<branch> — push by hand`**，終端會印出確切的推送與
   `gh pr create --base docs/direction-7-refugee-employment` 指令。Tommy 照貼，manager 審 PR。
4. **第一波合併後開第二波 `d7-wire`**：把 `/intake`、`/api/extract`、`/api/transcribe`、`/api/match`
   接進 `skeleton/app.py`，改 `ThreadingHTTPServer`，有金鑰時 `model_for()` 回傳 `live.LiveModel`。
   brief 依第一波實際合進來的程式碼再寫；介面契約見任一份 pending brief 的 "API contract"。
5. **錄影前**：`python3 skeleton/app.py` → `http://127.0.0.1:8000/intake`；斷網再跑一次確認離線可用；
   逐條複驗要念的數字；查 ElevenLabs 音檔保留設定（查清楚前不得宣稱零保留）。
6. 提交前（Tommy 2026-09-21 決定）：開 submission 分支，git rm AGENTS.md CLAUDE.md，評審看的是這個分支；開發分支照常保留兩檔，worker 流程要靠它們。

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
