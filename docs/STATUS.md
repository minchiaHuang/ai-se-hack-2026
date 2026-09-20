# STATUS

單行狀態：2026-09-21 開賽日。**六個方向的競品盤點全部完成**（淘汰 3、降級 1、通過 2），
且方向 2／3／6 的框架文件與共用技術骨架已建好，骨架可離線跑完黃金路徑與兩條失敗路徑。
題目未定，等 10:00 現場挑戰陳述——現場優先原則凌駕一切。

最後驗證：2026-09-21（`bash bin/verify.sh` → GREEN，含 23 個骨架測試，已故意弄紅驗證過）

## 進行中

- 題目選定：累計刪除 10 個方向。**倖存 2 個**：
  - **方向 2 — 二手店捐贈物進貨端分流**：上架／訂價被 Thriftify（無澳洲客戶）佔住、
    消費者棄置端被免費的 Recycle Mate 佔住、工業纖維分選是 Matoha／Fibersort 硬體層；
    **進貨端跨分支分流沒有人做**。付費方：Seamless 徵費基金、州政府傾倒紓困、社企自身處理成本。
  - **方向 6 — WISE 就業成效申報**：付費方證據最硬（**1 億澳幣** Commonwealth Outcomes Fund 依成效
    直接付給社企；**SEDI** 每家最高 12 萬澳幣的補助明文可用於購買影響力衡量服務）。
    判定**不併入方向 3**。
  - 兩者的碰撞風險分別是 Recycle Mate 與 Social Enterprise Australia 的 shared data system，
    都已寫在交接文件對應章節，pitch 前必須能一句話講清差異。

  **交接文件：`docs/research-brief-2026-09-21.md`** —— 給接手研究的 agent，自足可讀。
- 社群研究原始資料在 `reddit-x-research/`（兩輪 Reddit＋X 掃描，共 1,100 篇熱門貼文）。

## 已知問題

- 真實模型 API 尚未接。骨架的 `skeleton/core/model.py` 目前是 stub，
  介面已備妥，當天確定方向後才接——安裝任何相依套件需先取得核准。
- 方向 3 卡在前置閘門：必須先能回答「Amplify 免費且有學術背書仍關閉，你憑什麼不一樣」。

## 更名紀錄（2026-09-21）

- GitHub repo：`AI_Social_Enterprise_Hackathon_2026` → `ai-se-hack-2026`
  （https://github.com/minchiaHuang/ai-se-hack-2026，PRIVATE）
- 本地資料夾同步更名為 `ai-se-hack-2026`。
- GitHub 會 redirect 舊 URL，但隊友若已 clone 應改用新 URL。
- `.claude/orca-flow.json` 的 `"project"` 仍是賽事全名，那是顯示字串不是路徑，刻意不動。

## 下一步

1. ~~對方向 1 做競品盤點~~ —— **2026-09-21 完成，結果為淘汰**。免費端（PlanMind、Novida、
   PWdWA 工具包）與付費端（MagMindLab $89）皆已佔據，申訴階段另有聯邦免費倡議者與法律代理。
   完整競品表寫在 `docs/research-brief-2026-09-21.md` 第 5 節方向 1 末，不要重查。
2. ~~方向 2 競品盤點~~ —— **2026-09-21 完成，結果為通過**。上架／訂價分支被 Thriftify（Oxfam GB，
   無澳洲客戶）與 Thriftly 佔住，消費者棄置分支被免費的 Recycle Mate 佔住，工業纖維分選是
   Matoha／Fibersort 的硬體層——**進貨端跨分支分流決策沒有人做，澳洲尤其空**。
   付費方也找到了（Seamless 徵費基金、州政府傾倒紓困、社企自身處理成本）。
3. ~~方向 3–6 競品盤點~~ —— **2026-09-21 全部完成**。方向 3 降級（免費且有學術背書的 Amplify
   已因無人採用而關閉，是 viability 的不利證據）、方向 4 淘汰（Dear Landlord 逾 10 萬使用者，
   且 NSW 租客工會公開警告 AI 租務建議）、方向 5 淘汰（詐標端 ACCC 已接手、救助端在位者佔 80%+、
   同型社企 Yume Food 已清算）。逐條理由見交接文件第 5 節各方向末與第 3 節排除表。
4. **在方向 2 與方向 6 之間擇一**，或等 10:00 現場真實提案者出現（現場優先）。
5. 人工開啟該檔第 4.5 節列出的文件（自動抓取皆 403 或逾時），確認要引用的數字。
   **最優先是《Understanding the Impact Costs of WISE》**，它可能直接補上方向 6 的量化缺口。
6. 確認賽前技術預備：AI 助手登入、prototyping 工具或 API 存取。
7. 開賽後確定題目與堆疊，於 `bin/verify.sh` 的標記區段補上真正的測試。
8. 通知設計與資料科學隊友新的 repo URL。

**現場優先**：10:00 現場出現的真實問題，一律優先於上述任何方向（判準見交接文件第 7 節）。
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
