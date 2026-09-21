# 框架 — 方向 1：NDIS 既有證據的編排

競品盤點：**已完成**（2026-09-21）。原本記在 `docs/research-brief-2026-09-21.md` 第 5 節方向 1 的
「清掉」判定**已撤回**——該判定的依據是「已有免費或成熟產品」，但本賽事的七項加權評分標準裡
**沒有新穎性**（清單見 `AI_CONTEXT.md`〈Official event facts〉）。競品的存在因此不是死刑，
而是兩件事：**需求為真的證據**，以及**我們必須當場回答的問題**（見〈競爭態勢〉一節）。
所有競品證據原封保留，只換擺放位置，不換內容。

本檔填的是 `docs/superpowers/specs/2026-09-21-direction-frameworks-design.md` 的七格模板。
標記規則：**EVIDENCE**（附來源／日期）／**INFERENCE**（推論）／**RECOMMENDATION**（建議）。
未標記者一律視為推論。本專案**未做過任何訪談、驗證或測試**，本檔任何一句都不得被讀成做過。

---

## 0. 倫理紅線（先寫，因為它決定後面每一格）

**可以做**：把使用者**已經持有**的文件裡**既有的**段落找出來、定位到頁碼、對上他自己寫的主張。

**不可以做**：
- 生成主張、生成症狀或功能限制的描述、改寫或「加強」醫療意見
- 撰寫法律論點、判斷勝算、任何構成**法律意見**的輸出
- 代替使用者送出任何東西給 NDIA 或 ART

這條線不是加分項，是這個方向能不能存在的前提。它同時對應 brief 方向 1 自列的第 4 個風險
（「協助編排既有證據 vs 生成主張；是否構成提供法律意見」）。第 4 格與第 6 格的失敗路徑
就是這條線在程式與 UI 上的具體形狀。

**政治風險（EVIDENCE）**：X 上主流敘事是 NDIS 詐騙猖獗——@bhavdip143「the biggest rort in
Australia」1336 likes，已驗證（brief §5 方向 1）。「幫參與者贏申訴」會被一部分聽眾讀成
「幫人鑽漏洞」。我們的答案就是上面這條紅線：**我們不產生任何新主張，只把你已有的證據找回來**。
被問到時直接這樣講，不要迴避。

---

## 1. 一位使用者、一個時刻、一個被卡住的結果

**使用者（RECOMMENDATION）**：一位**倡議者或 support coordinator**，正在替某位參與者準備
內部覆議／申訴文件——不是參與者本人，也不是律師。

選這個人而不是參與者本人的理由（**EVIDENCE**，r/NDIS，brief §5 方向 1）：
- ↑12「many people dont have capacity to approach tribunal this way」
- ↑6「A lot of us are too disabled, ill or fatigued to do all this」
- ↑7「severe lack of advocacy services and competent legal services in the NDIS tribunal space」
- 一位自稱 SSC 的留言者：「I desperately need an advocate for 2 of my participants」

**INFERENCE**：需求最密集的地方是「一個人同時扛多個案件」，而不是「一個人一生一次」。
這同時也是付費方比較站得住的一側。若現場的真實提案者是參與者自助組織，這一格改寫成參與者本人，
其餘六格不變——但要重算第 7 格的數字歸屬。

**時刻**：截止日前，桌上（或雲端資料夾裡）攤著這位參與者的整套既有文件——
治療師報告、評估、既往計畫、來往信件——要開始逐頁找「哪一段話支持哪一個點」。

**被卡住的結果**：一份**帶頁碼、逐條對上主張的證據索引**。它做得出來，只是要花掉一個人好幾天。

---

## 2. 斷點：最高成本的那一步

**把散落在數百頁既有文件裡的句子，一條一條對上這次要證明的點，並記下頁碼。**

**EVIDENCE**（r/NDIS 年度熱門榜，brief §5 方向 1 已附連結與票數）：
- 《18 Months, 900 Pages of T-Docs and 1,000+ Emails - I WON》↑46
  https://www.reddit.com/comments/1vz9slx
  致勝戰術原話：「I added an 'evidence index'… referenced quotes from documents already in the
  T-Docs **with page numbers**」
- 《Asked for more supports. Backed up with reports from 5 specialists…》↑63
  https://www.reddit.com/comments/1tk1uoa ——「**ignored 50 pages of evidence** compiled by five
  qualified specialists」
- 《Supports Needs Assessment not fit for purpose》↑47 https://www.reddit.com/comments/1pbx6m5
  ——「**The SNA cannot be appealed.** Only the plan can be appealed and that is driven by the SNA.」

**INFERENCE**：贏的那一篇與被忽略的那一篇，差別不在證據的量（50 頁 vs 900 頁都算多），
而在**證據有沒有被編排成可被逐條查核的形式**。這就是斷點所在——不是取得證據，是編排既有證據。

**代價不對稱**：漏掉一段既有支持段落 → 這個點看起來沒有證據；
編排得太積極、開始替文件「補話」 → 踩到上面的倫理紅線，且一旦被發現，整份文件包失去可信度。

---

## 3. 理想的人類工作流（AI 之前）—— 閘門格

沒有 AI 也應該這樣做，而且這是我們真正要賣的東西：

1. 先寫下**這次要證明的主張清單**——每一條是一個需要被支持的點，用對方的框架寫
   （功能性需求、reasonable and necessary 等），一條一句
2. 把手上**既有文件**做成清冊：文件名、作者、日期、頁數。不新增、不索取
3. 逐條主張回既有文件裡找支持段落，記下**文件 ＋ 頁碼 ＋ 原句**
4. 標出**沒有任何既有文件支持的主張**——這一步的產出不是「把它寫出來」，
   而是「去取得新的專業證據，或把這條拿掉」
5. 人審過全部條目後，才輸出成一份帶頁碼的索引並遞交

**AI 進來之前，第 1 步與第 4 步就已經是改善。** 第 1 步逼人先講清楚要證明什麼，
第 4 步逼人承認哪裡沒有證據——而這正是最容易被「生成」補掉的洞。
如果現場提案者連主張清單都沒有，那才是第一個交付物：先做清單，AI 之後再說。

---

## 4. AI 的受限任務

**抽取**，僅此一項（模板的六選一：分類／檢索／抽取／摘要／建議／警告）。

**輸入**：使用者已持有的文件 ＋ 使用者自己寫的主張清單（第 3 格第 1、2 步的產出）。

**輸出**：每條主張底下列出候選段落，每個候選段落必附
**文件名 ＋ 頁碼 ＋ 一字不改的原句引文 ＋ 信心值**。

**明確不做**：不生成主張、不改寫或潤飾引文、不摘要成自己的話、不寫申請信或陳述書、
不評估勝算、不給法律意見、不連 NDIA 或 ART 的任何系統、不儲存參與者文件。

**INFERENCE**：「不摘要、只定位」看起來比競品做得少，這是刻意的——見〈競爭態勢〉。
輸出不是一份文件，是一張**可被逐條翻回原文查核的對照表**。

---

## 5. 人類保留決定權的節點

1. **每一條「這段話支持這個主張」都由人確認。** AI 的輸出是候選，不是結論。
2. **沒有支持段落的主張，由人決定怎麼辦**（取得新證據／改寫主張／放棄）。
   系統在這裡**不提供任何文字**——這是第 6 格失敗路徑的內容。
3. **遞交永遠是人做的動作。** 系統不產生可直接送出的成品。

理由不只是安全：跨平台唯一確認的社群共識就是這件事——
**EVIDENCE**：@criprights（Sam Connor，2026-08-15）422 likes／256 reposts／104 bookmarks，已 oEmbed 驗證
https://x.com/criprights/status/2088493752822444511 ；
r/NDIS《Help put a stop to AI-Generated NDIS Plans》↑43 ——
「**A machine cannot be held accountable, therefore a machine should not make a management decision.**」

一個會替身障者生成主張的系統，正好是這群人正在公開反對的東西。

---

## 6. 黃金路徑 ＋ 失敗路徑

**黃金路徑**：載入使用者的既有文件 → 貼上主張清單 → 對第 3 條主張
「夜間需要二人協助轉位」列出 2 個候選段落：
《OT Functional Assessment, 2025-03-11, p.7》「requires two-person assist for overnight transfers」
（信心 0.88）／《GP letter, 2024-11-02, p.2》（信心 0.41）
→ 人逐條確認 → 產出帶頁碼的證據索引。

**失敗路徑（必須 demo，且比黃金路徑更重要）**：第 5 條主張在既有文件中找不到任何支持段落。
系統顯示「**在你提供的文件中找不到支持這條主張的段落**」，並**拒絕產生任何文字**，
只提示「這條需要新的專業證據，或由你決定移除」。

這條路徑就是倫理紅線在畫面上的樣子。它也是與競品最清楚的分界：
**別人在這個格子裡會幫你寫出來，我們在這個格子裡停住。**
Demo 一定要走到這裡，否則整個方向在評審眼中與 $89 的產品沒有區別。

---

## 7. 組織拿得走的一個數字

**編排一個案件的證據索引所花的工時（從一疊文件到帶頁碼的對照表）。**

算法必須當場講得出來：（人工基準工時 － 使用後工時）× 每月案件數。

⚠️ **NOT FOUND**：沒有查到任何公開的「每案證據編排工時」基準。
**不得使用我們自己編的數字。** 基準值只能由現場提案者提供（現場第 1 個問題就是問這個）。
若拿不到，demo 只顯示「本案已定位的既有證據段落數 ／ 主張數 ／ 無支持的主張數」，
並明說工時基準未取得。

**INFERENCE**：「無支持的主張數」這個副產品可能比主數字更有說服力——
它量化的是誠實，而不是產能。

---

## 付費方

參與者本人**不列為付費方**：brief §5 方向 1 已記錄「參與者現金吃緊」。候選（皆未驗證）：

1. **Support coordination 與 plan management 供應商** —— **INFERENCE**，依據是那位 SSC 留言者
   「I desperately need an advocate for 2 of my participants」。屬「小組織後台」型痛點，
   依 brief §4.1 的規律在社群上難以取得佐證，**必須現場問到才算數**
2. **倡議組織** —— **EVIDENCE**：PWdWA＋Legal Aid WA 已自製並維護免費覆議工具包
   https://pwdwa.org/how-we-help/ndis/ ，代表這類組織確實在這件事上投入人力
3. **申訴階段的公共經費** —— **EVIDENCE**：聯邦 NDIS Appeals Program 提供免費倡議者與法律代理
   https://www.health.gov.au/our-work/ndis-appeals-program ；National Legal Aid 指 2026–27 起兩年
   續撥 **1,470 萬澳幣** https://nationallegalaid.org.au/news/fed-budget-202627-ndis
   **INFERENCE**：有經費流動不等於有採購管道，這是在位者也可能是客戶，**現場必須釐清方向**
4. **願付價格的存在** —— **EVIDENCE**：MagMindLab 以 **$89 inc. GST** 販售相近產品，
   代表這個市場裡有人願意掏錢。**NOT FOUND**：其實際銷量、公司登記／ABN、使用者評價

**NOT FOUND**：DANA 或其 80 個會員倡議組織實際使用哪套軟體做申訴文件編排
（查得的只有 NCDA 的 Disability Advocacy Portal，定位是資源庫與系統性倡議資料蒐集，不是文件編排工具）。

---

## 競爭態勢與我們必須回答的問題

這個問題空間同時被**免費產品**、**已上市的付費產品**、**政府免費申訴代理**三層佔據。
在沒有新穎性評分的場子，這是**需求為真的最硬證據**——同時也是我們必須正面回答的問題。

**EVIDENCE — 直接競品（皆於 2026-09-21 查證）**

| 產品 | 做什麼 | 價格 | 與本構想重疊 |
|---|---|---|---|
| **PlanMind** https://planmind.com.au/ | ReAssess（產出 Reassessment Brief PDF＋會議提問＋書面陳述）、Plan Decoder、Goal Planner、Support Letter Generator、Budget Calculator、Jargon Buster | 官網原話：「No signup required · No plan data stored · Free to start」，計算機與辭典「always free」 | 極高。ReAssess 自述「aligned to the new I-CAN v6 framework」 |
| **MagMindLab** https://magmindlab.com/ | 上傳既有醫療／評估報告 → 約 25 頁 Support Needs Evidence Report、I-CANv6 草擬評分、六大 impairment 類別對映、Reasonable and Necessary 結構化報告、**Evidence Gap Checklist**、給治療師的草擬信 | 「$89 inc. GST」（自述原價 $109 的促銷價） | 幾乎等同。「證據索引＋缺口檢查」正是本構想的核心 |
| **Novida** https://www.novida.com.au/resources | NDIS 表單白話解釋、信件與陳述範本、逐步檢核表、辭典、資格檢查器 | 官網原話：「everything here is free」／範本「free to copy, adapt and use」 | 中高（範本層） |
| **PWdWA + Legal Aid WA《WA Advocates Internal Review Toolkit》** https://pwdwa.org/how-we-help/ndis/ | 內部覆議工具包＋申請範例＋定期線上說明會 | 免費 | 中（覆議階段的流程指引） |
| **NDIS Appeals Program**（聯邦 Department of Health, Disability and Ageing） https://www.health.gov.au/our-work/ndis-appeals-program | ART 申訴階段配置受訓身障倡議者作為支持人，必要時提供法律代理 | 官方原話：supports are **free of charge**。National Legal Aid：2026–27 起兩年 1,470 萬澳幣續撥 https://nationallegalaid.org.au/news/fed-budget-202627-ndis | 高。申訴階段的免費在位者，且剛加碼 |
| **NexLaw ChronoVault** https://www.nexlaw.ai/au/products/chronovault/ | AI 案件時序表／證據編排，產出 court-ready chronology | 商業付費 | 中，但面向律師，不是參與者 |

**EVIDENCE — 制度層面的變動**：自 2026 年中起，NDIA 改以受訓評估者執行 **I-CAN v6** 半結構式訪談
（最長約三小時），由電腦程式依評估資料計算預算，取代規劃師裁量。

⚠️ **UNVERIFIED — 必須照實講**：「獨立醫療證據不再是必須被納入考量的項目」這項解讀，
目前只有第三方（plan manager／provider 部落格）與參議員 Steele-John 提交的 APH 文件
https://www.aph.gov.au/-/media/Estimates/ca/supp2526/Health_Disability_and_Ageing/15_TabledDoc_SenatorSteeleJohn.pdf
支撐。NDIA 官方頁 https://www.ndis.gov.au/news/10927-new-tool-deliver-simpler-pathway-disability-supports
自動抓取回 **HTTP 403**，**尚未從官方原文確認，不得當作事實引用**。
被問到時的正確答法：「這點我們沒能從官方原文確認，官方頁面抓取回 403。」

**剩下的縫隙（EVIDENCE 層面的事實）**：查到的產品中，**沒有任何一家在賣
「tribunal 階段、帶頁碼的跨文件證據索引」**——也就是 ↑46 那篇致勝貼文真正用的那招。

### 既然這些產品存在，我們必須在哪裡更好或不同

三點，缺一不可，而且每一點都要能在 demo 裡看見：

1. **使用者不同**：PlanMind、MagMindLab、Novida 都是**參與者自助**的形狀（單次、上傳、產出 PDF）。
   我們面向的是**一個人同時扛多個案件**的倡議者／協調者。**INFERENCE**，現場必須確認。
2. **輸出形狀不同，而且是刻意做得更少**：競品產出**生成的文字**
   （書面陳述、支持信、25 頁報告——皆為其官網自述）。我們產出的是
   **帶頁碼、可逐條翻回原文查核的對照表**，一個字都不生成。
   在一個 AI 信任度正在下降的領域，這是特性不是缺陷（見第 5 格的社群證據）。
3. **紅線可被看見**：找不到支持段落時我們停住並說「找不到」。競品在這個格子裡會幫你寫。
   這是唯一一個在 90 秒 demo 裡就能讓評審分辨出差別的動作。

### 評審／提案者一定會問的三題，以及我們的答法

1. **「$89 就買得到近似品，為什麼還需要你？」**
   → 因為那是賣給參與者的一次性報告，而它會**生成文字**。我們賣的是可查核的定位表，
   給每週處理多個案件的人。若現場問不到這種使用者，**這個方向當天就不該選**。
2. **「如果 I-CAN v6 真的讓獨立醫療證據不再必須被考量，你的前提還在嗎？」**
   → 先誠實說這點未經官方確認（403）。若屬實，主張清單改成**功能性描述**，
   第 4 格的受限任務（抽取＋頁碼定位）不變——被定位的來源從醫療報告換成功能性紀錄。
3. **「政府已經提供免費倡議者與法律代理，你是取代還是配合？」**
   → 配合。我們不進申訴程序、不代理、不給法律意見（見第 0 節）。
   我們縮短的是倡議者在拿到文件之後、寫任何東西之前的那幾天。

---

## demo 資料來源與誠實邊界

- **不得使用任何真實參與者文件。** 那是個人健康資訊，且我們沒有任何同意書。
  這條沒有例外，包含「朋友願意給」的情況
- **沒有公開的 NDIS 證據文件資料集**（**NOT FOUND**）。demo 用**我們自製的合成文件**：
  假造的 OT 評估、GP 信件、既往計畫，頁碼與段落都是編的，並在畫面上明寫是合成資料
- **不得聲稱**做過訪談、做過使用者測試、與任何倡議組織或 NDIA 接觸過、
  或本工具曾用於任何真實案件——**這些事都沒有發生**
- **不得引用** NDIA 那個 403 頁面的內容，也不得把第三方解讀講成官方說法
- Reddit 與 X 的引用僅用於說明問題形狀與社群態度，票數與原話照抄，不加工

---

## 現場要問提案者的三個問題

1. 你們現在編排一個案件的證據，是誰在做、花多久？（第 7 格的基準值只能從這裡來）
2. 你們用過 PlanMind、MagMindLab，或 PWdWA 的覆議工具包嗎？哪裡不夠用？
   （若答「都很好用」，這個方向當天就放掉，不要硬推）
3. 這筆錢從哪出——組織營運預算、某個方案經費，還是參與者自付？
