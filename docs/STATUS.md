# STATUS

單行狀態：2026-09-21 開賽日。賽事事實已重新查證；**六個方向的競品盤點全部完成**。
淘汰 3 個（1 NDIS 文件編排、4 租屋權益、5 食物系統）、降級 1 個（3 社企證據層）、
通過 2 個：**方向 2 二手店進貨端分流**與**方向 6 WISE 成效申報**。兩者擇一在賽事當天決定。

最後驗證：2026-09-21（`bash bin/verify.sh` → GREEN）

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

- 技術堆疊未定，`bin/verify.sh` 目前只做骨架層級檢查（shell 語法、STATUS 存在、無超大追蹤檔）。

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

## 背景

完整專案脈絡見 `AI_CONTEXT.md`（官方賽事事實、評審、研究過的問題領域、策略方向、角色分工）。
