# STATUS

單行狀態：2026-09-21 開賽日。**已選定方向 6（WISE 就業成效申報）**，並完成第二輪深度研究：
Impact Costs 報告全文已讀（量化缺口部分補上）、第二輪競品掃描找到 White Box Enterprises
與 Seedkit 兩個必須正面回應的對象。六個方向的框架仍全數保留備用。
共用技術骨架已建好，可離線跑完黃金路徑與兩條失敗路徑。**現場優先原則仍凌駕一切。**

最後驗證：2026-09-21（`bash bin/verify.sh` → GREEN，含 23 個骨架測試，已故意弄紅驗證過）

## 進行中

- **題目選定：方向 6（WISE 就業成效申報）**，2026-09-21 下午決定。第二輪研究成果寫在
  `docs/frameworks/direction-6-wise-outcomes.md`（上場前必讀「第二輪競品」一節）與
  `docs/research-brief-2026-09-21.md` 第 5 節方向 6。三件會改變說法的事：
  1. **量化缺口部分補上**：Impact Costs 報告全文已讀。可引用督導工時（主管時間 2–3 倍、
     L&D 3.5% vs 25% 工時）、缺勤（30%→15% vs 一般 10%）、員工成本佔 Impact Cost 54–86%。
     ⚠️ 報告**明文拒絕揭露** Impact Cost 百分比，那個數字仍不存在，不得估算。
  2. ⛔ **White Box Enterprises 已在做這件事，只是用人做的**（PBO3 17 家、WorkFoundations 8 家）。
     CSI 評估原話：聚合者模式讓社企覺得申報是 **BAU**——「WISE 被申報壓垮」對這批不成立。
     定位改為「White Box 是客戶或夥伴，不是要打倒的競品」，問題改為「人扛的協調怎麼擴到幾百家」。
  3. **Seedkit**（免費、維州政府 100 萬澳幣、墨大託管，2023-11 上線）與 Amplify 同模式。
     差異仍成立但很薄：Seedkit 無任何資助方格式範本／匯出。
  - demo 目標格式改用 **Social Traders 認證（200+ 資料點、週期性、格式穩定）**，
    不要用參數還在共同設計的 Outcomes Fund。可觸及規模用 **294 家／14,013 名受支持員工**（Pace 2023），
    不要用 SECNA 的「almost 7,000 家」。
- 其餘五個方向的框架保留備用：**六個方向全部仍在檯面上**。2026-09-21 撤回先前寫死的「淘汰／降級／通過」判決——
  評分標準只有 quality／impact reasoning／viability，**沒有新穎性這一項**，
  用「已經有人做了」淘汰方向是加了一把評審沒有的尺。證據全部保留，判決全部移除。
  - 每個方向一份框架，同一套七格模板：`docs/frameworks/direction-{1,2,3,4,5,6}-*.md`
  - 現場那張要拿在手上的：`docs/frameworks/onsite-matching-sheet.md`
  - 唯二與競品無關的保留意見：**方向 4** 的使用者是個人租客不是社企（對象問題）；
    **方向 5 支線 A（食品詐標）** 需要同位素鑑識，48 小時做不到（能力問題）。
    兩者都寫在各自框架裡，不是淘汰。

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
4. ~~在方向 2 與方向 6 之間擇一~~ —— **2026-09-21 下午選定方向 6**。現場優先原則不變。
5. ~~人工開啟《Understanding the Impact Costs of WISE》~~ —— **2026-09-21 已讀完全文**，
   直接下載網址記在交接文件 §4.5，**不要重抓**。§4.5 其餘文件仍待人工開啟。
5b. **方向 6 剩下的未解問題**（上場前若有時間）：
   (a) PBO3 於 2026-03 結束後的後續／是否擴大，官方尚無公開結論；
   (b) 「為什麼不是 ReadyTech 順手做」仍無已驗證答案；
   (c) Impact Costs 報告提到的「開發中工具」遍尋不著，屬 NOT FOUND 而非確定沒做。
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
