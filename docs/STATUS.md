# STATUS

單行狀態：2026-09-21 開賽日。賽事事實已重新查證，專案更名為 `ai-se-hack-2026`。

最後驗證：2026-09-21（`bash bin/verify.sh` → GREEN）

## 進行中

- 開賽日收尾：分支 `docs/update-event-facts-2026-09-21` 待推送。

## 已知問題

- 技術堆疊未定，`bin/verify.sh` 目前只做骨架層級檢查（shell 語法、STATUS 存在、無超大追蹤檔）。

## 更名紀錄（2026-09-21）

- GitHub repo：`AI_Social_Enterprise_Hackathon_2026` → `ai-se-hack-2026`
  （https://github.com/minchiaHuang/ai-se-hack-2026，PRIVATE）
- 本地資料夾同步更名為 `ai-se-hack-2026`。
- GitHub 會 redirect 舊 URL，但隊友若已 clone 應改用新 URL。
- `.claude/orca-flow.json` 的 `"project"` 仍是賽事全名，那是顯示字串不是路徑，刻意不動。

## 下一步

1. 確認賽前技術預備：AI 助手登入、prototyping 工具或 API 存取。
2. 開賽後確定題目與堆疊，於 `bin/verify.sh` 的標記區段補上真正的測試。
3. 通知設計與資料科學隊友新的 repo URL。

## 背景

完整專案脈絡見 `AI_CONTEXT.md`（官方賽事事實、評審、研究過的問題領域、策略方向、角色分工）。
