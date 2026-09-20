# AGENTS.md

專案指令。開場先讀本檔，再讀 `docs/STATUS.md`（STATUS 的時效性優先於本檔）。

## 專案

AI for Social Enterprise Hackathon 2026（2026-09-21～09-22，UTS Startups, Ultimo NSW）。
團隊 3 人：開發（Tommy）、設計、資料科學。

## 必讀脈絡

`AI_CONTEXT.md` 是本專案的長效脈絡檔：官方賽事事實、已確認評審、研究過的問題領域、
策略方向、角色分工、建構與 pitch 順序、要避開的做法。修改任何策略或研究結論前先讀它，
且只在有新證據佐證時才更新。

其中的「AI operating instructions」章節對本專案具約束力，特別是：
區分官方要求／證據／推論／建議；未經當下核准不得聯絡受訪者、主辦方或合作夥伴；
沒有證據就不得宣稱已完成訪談、驗證或測試。

## 驗證

```
bash bin/verify.sh
```

賽事期間確定技術堆疊後，在該檔標記區段補上真正的測試。

## 版本控制

`work/` 下的 PNG／PDF 是 docx 排版流程的校稿輸出，已由 `.gitignore` 排除，
可由 `work/*.py` 與 `work/*.swift` 重新產生。
