# STATUS

單行狀態：2026-09-21 開賽日。賽事事實已重新查證；題目方向第一輪收斂為 6 個，
方向 1（NDIS 文件編排）已完成競品盤點並淘汰，待研究剩 5 個。

最後驗證：2026-09-21（`bash bin/verify.sh` → GREEN）

## 進行中

- 題目選定：已刪除 8 個方向（含 2026-09-21 因競品盤點淘汰的方向 1 NDIS 文件編排），
  待深入研究剩 5 個（方向 2–6）。
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
2. 依 `docs/research-brief-2026-09-21.md` 第 5 節，研究方向 2–6，從方向 2（二手店捐贈物路由）起。
   每個方向都先做競品盤點再投入。
3. 人工開啟該檔第 4.5 節列出的文件（自動抓取皆 403），確認要引用的數字。
4. 確認賽前技術預備：AI 助手登入、prototyping 工具或 API 存取。
5. 開賽後確定題目與堆疊，於 `bin/verify.sh` 的標記區段補上真正的測試。
6. 通知設計與資料科學隊友新的 repo URL。

**現場優先**：10:00 現場出現的真實問題，一律優先於上述任何方向（判準見交接文件第 7 節）。

## 背景

完整專案脈絡見 `AI_CONTEXT.md`（官方賽事事實、評審、研究過的問題領域、策略方向、角色分工）。
