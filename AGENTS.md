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

## 分工

手上同時有兩個以上任務時，先評估能不能平行做，再開始動手：

```
python3 ~/.claude/skills/orca-flow/scripts/worktrees.py overlap <檔案或目錄> ...
```

檔案不重疊就提議開 worker（`orca-flow` 技能），一人一個 worktree，不要一條龍自己做完。
重疊的任務併成一包或排先後。切法看動到的檔案，不是看功能。

主 checkout 停在 base branch，改動一律在 worktree 裡做。`main_checkout_guard.py` 這個
PreToolUse hook 會擋掉主 checkout 的 Edit／Write，被擋就把工作搬進 worktree，
不要改用 Bash（`sed -i`、heredoc）繞過去。

## 版本控制

`work/` 下的 PNG／PDF 是 docx 排版流程的校稿輸出，已由 `.gitignore` 排除，
可由 `work/*.py` 與 `work/*.swift` 重新產生。
