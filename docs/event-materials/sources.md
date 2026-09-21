# 活動頁資料清單（2026-09-21 抓取）

活動頁 https://hackhq.io/events/o6v6DgCLc4 的 Resources 區塊列出各提案組織的材料。
本目錄存放已取得的內容；二進位原檔在 `work/event-materials/`（`*.pdf` 已被 `.gitignore` 排除，
xlsx 有進版控）。

| 來源 | 項目 | 狀態 | 存放位置 |
|---|---|---|---|
| Recheck | Hackathon Briefs（14 頁 PDF） | ✅ 已取得 | `recheck-brief.md`、`work/event-materials/recheck-hackathon-briefs.pdf` |
| Recheck | List of sample takers（61 列） | ✅ 已取得 | `recheck-sample-takers.md`、`work/event-materials/sample-takers.xlsx` |
| Social Ventures Australia | Detailed briefs（`SVA Hackathon Proposal_UPDATED.pdf`） | ❌ **需登入** | 見下 |
| Social Ventures Australia | Problems pitch videos | ❌ **需登入**，且為影片 | 見下 |
| ElevenLabs | Voice AI Guide | ✅ 已讀，見下方摘要 | 本檔 |
| — | Spark Festival 2026 Opening Celebration | 活動報名連結 | https://events.humanitix.com/spark-2026-opening |
| — | UTS Startups Tour | 活動報名連結 | https://luma.com/utss-6wgk |

## 取不到的兩份（需要人工）

Social Ventures Australia 的兩份材料放在該組織的 OneDrive/SharePoint
（`svaltd-my.sharepoint.com`），直接抓回來的是 Microsoft 登入頁的 HTML，不是檔案。
這兩份要由人在瀏覽器裡開啟後下載，放進 `work/event-materials/`，我再抽文字。

- Detailed briefs（PDF）：`SVA Hackathon Proposal_UPDATED.pdf`
- Problems pitch videos：影片，即使下載到也需要有人看或轉逐字稿

**這代表現在手上只有 Recheck 一家的題目。** SVA 那邊的題目內容目前是未知，
不要假設它與 Recheck 相似，也不要在還沒看過之前就排除它。

## ElevenLabs Voice AI Guide（摘要）

https://eleven-hackathon-sydney-guide.lovable.app/#access

- 兌換流程：`#coupon-codes` 頻道 → Start Redemption → 選活動 → 填報名 email → bot 發專屬兌換碼。
  **頁面沒有寫額度數字或期限**，不要對額度做任何假設。
- Text-to-Speech 模型：`eleven_v3_conversational`（即時代理，約 280ms）、
  `eleven_v3`（品質優先，5,000 字元上限）、`eleven_flash_v2_5`（低延遲，約 75ms）、
  `eleven_multilingual_v2`（長文，10,000 字元）
- Speech-to-Text 模型：`scribe_v2`（批次，90+ 語言）、`scribe_v2_realtime`（串流，約 150ms）、
  `scribe_v2_medical`
- 頁面未載明賽道規則、獎項條件或截止時間。

語音只是可選工具，不是必須。本專案骨架的「零外部套件、單次模型呼叫」約束（見 `AI_CONTEXT.md`）
仍然有效，接 ElevenLabs 等於引入相依套件與第二個服務，要先取得核准。
