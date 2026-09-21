# 研究交接簡報 — 2026-09-21

本檔是給**接手研究的 AI agent** 的自足簡報。讀完本檔＋`AI_CONTEXT.md` 即可開工，
不需要回溯先前的對話。

產出本檔的那一輪，共跑了 11 個研究 agent 與 2 輪 Reddit＋X 社群掃描。
原始社群資料在 `reddit-x-research/`。

---

## 1. 硬性規則（違反會讓成果作廢）

1. **不得聯絡任何人**（受訪者、主辦方、合作夥伴、機構）。全部是桌面研究。
2. **證據分級要標**：OFFICIAL FACT ／ EVIDENCE（附 URL 與日期）／ INFERENCE ／ RECOMMENDATION。
3. **不得宣稱已完成訪談、驗證或測試**，除非真的有證據。
4. **每個方向都必須做競品盤點。** 本專案已用競品檢查刪掉 3 個方向；沒做競品檢查的建議一律不採納。
5. **社會企業的定義**（Social Traders 五項）：以解決社會／環境問題為存在理由、決策上目的優先於利潤、
   自給自足的交易收入、多數盈餘再投入使命、有鎖定目的的法律結構。
   **受補助的慈善機構不是社會企業。** 服務對象搞錯，證據再硬也沒用。
6. 查不到就寫 **NOT FOUND**，不要用推論填空。

---

## 2. 賽事事實（2026-09-21 由官網重新查證）

完整內容見 `AI_CONTEXT.md`。以下是最常被記錯的幾點：

- Day 1 議程比舊紀錄**提前 15 分鐘**：09:00 introduction／09:30 intro to AI for SE／
  **09:45 Intro to Problem Validation**／**10:00 問題陳述 pitch**／10:30 組隊開工
- 評審 **4 位**：Nandeeta Maharaj（Goods 4 Good 創辦人）、Ramana Kirubagaran（MultiLit CIO）、
  James Hornitzky（Social Traders **Digital Enablement Specialist**，非主管職；
  同時是共同主辦 Moreneta Initiative 的非執行董事）、
  **Eva Sheluhina（ElevenLabs Forward Deployed Engineer）**
- 贊助／夥伴：UTS Startups、Social Impact Hub、SECNA、**ElevenLabs**、Goods 4 Good、
  **Lovable**、**Base44**、Red Bull、HackHQ、Spark Festival
- 評分為七項加權標準（2026-09-21 自官方頁面查證，取代先前記為三項的轉述）：
  **Problem–Solution Fit 20%／Usability 15%／Working Prototype 15%／Effective Use of AI 15%／
  Social Impact Reasoning 15%／Problem Validation 10%／Pathway to Sustainability 10%**
  ——**沒有新穎性這一項**

### 機構事實修正（曾經搞錯過，不要再錯）

- **Koorana** 不是兒少保護個案管理機構，是 **NDIS 註冊的早療與聯合健康服務商**（0–18 歲）。
- **MultiLit** 是 **MultiLit Pty Ltd 商業公司**（ABN 37 118 315 816），源自麥考瑞大學研究計畫，
  **不在 ACNC 慈善登記**，也未以社會企業自居。Kirubagaran 的視角是「商業教育公司 CIO」。
- **Goods 4 Good** 是**線上市集**，策展銷售其他 60+ 家認證社企的 500+ 品項，做 B2C 與企業送禮。
  創辦人自述願景是「社會企業界的 Amazon」。
- **Made for Change**（同一創辦人）是印度醃菜／調味料品牌，**利潤 50% 捐給支持家暴受害婦女的機構**。
  「為重建人生的女性創造就業」是**未來計畫，非現況**，目前不是 WISE。
- **SECNA** 官網原話（可引用）：社會企業「sit between traditional business and charity, many fall
  through the gaps… **They do the job of both without the enablers of either.**」
  並明確指出 **NSW 政府目前沒有任何優先採購社企的機制**。
- Social Traders 認證是**免費**的（依州別由政府與慈善資助方部分補助）。
  ⚠️ 不要與**會員**混為一談：Connections 會員每年 750 澳幣＋GST，是另一件事。
  搜尋結果常把兩者混講成「認證要 700 澳幣」，那是錯的。詳見 §5 方向 3 末的 FACT GUARD。

---

## 3. 已排除的方向 — 不要重查

| 方向 | 刪除理由 |
|---|---|
| **家暴 App（面向倖存者）** | ①空間飽和：Daisy（1800RESPECT）、Penda、Arc App、SafeSteps、i-DECIDE 全為政府或 peak body 出資免費發行 ②WESNET 查出這類 App 本身有安全漏洞、反使當事人更危險；36 個 DV 聊天機器人中 16 個無隱私政策 ③1800RESPECT 2024–25 的 33.5 萬次接觸中 **77% 是電話**、僅 18% 網頁聊天 ④48 小時內拿不到任何真實床位／轉介資料（SHIP 僅限登入工作者、Link2home 純電話、Infoxchange 與 healthdirect API 皆需正式協議） |
| **家暴風險分流排序** | 違反本專案禁止「自動化福利、醫療、危機或資格判定」的規則 |
| **識字／朗讀流暢度評估** | ①**Microsoft Reading Progress / Reading Coach 免費**且內建 Teams Education，Google Read Along 亦免費；付費端有 Amira、SoapBox（已併入 Lexia）、Literably（已被 Heggerty 併購） ②兒童語音 ASR 錯誤率為成人 **2–5 倍**，4–7 歲最差 ③OAIC 兒童線上隱私規範（2026-03-31 草案）＋隱私法 APP 要求監護人同意，兩天團隊做不到 |
| **買方端 RFQ→社企供應商媒合** | Social Traders 政府買方入口網站標語已是「Connect with the right social enterprises, identify opportunities, **track outcomes and produce reports**」—— 正是這一整包 |
| **「把訓練教材變成 AI 語音」** | **ElevenLabs 自己就在賣**（Learning and Development Conversational Agents） |
| **志工排班** | Rosterfy、Deputy 慈善版、Vollie 已佔據市場 |
| **補助核銷（慈善機構版）** | 證據最厚（生產力委員會 2024-05-10 終報、聯邦補助架構 2024-10-01 修訂、ANAO 2025–26、Justice Connect：46% 機構年收 <25 萬），**但服務對象是受補助慈善機構，不是社會企業** —— 主題不符。僅在現場明顯以慈善機構為主時作為備案 |

---

## 4. 方法教訓（影響怎麼做下一輪研究）

### 4.1 社群平台的可見性規律

兩輪 Reddit＋X 掃描（共 1,100 篇熱門貼文）得出：

> **「個人 vs 機構」的問題 → 社群聲量巨大。**
> **「小組織後台」的問題 → 社群完全靜音。**

社會採購、影響力衡量、社企認證在 Reddit 與 X 上**各自都是零**。
不是痛點不存在（報告都寫了），而是受苦的是機構員工，他們不在公開平台談工作。

**含意**：社群平台不是「哪個題目更真實」的裁判，是「哪個題目有人替你作證」的裁判。
對後台型題目，不要再浪費時間搜 Reddit／X，改查報告、公會文件、職缺廣告。

### 4.2 兩個平台可能立場相反

同樣講 NDIS：Reddit 的 r/NDIS 主流是「參與者被砍經費」，
X 的主流是「經費失控、詐騙猖獗」（互動量高一個量級）。
**只看一邊會對公共意見分布產生嚴重誤判。**

### 4.3 已被否證的推論（不要再用）

- ❌「AI slop 反彈是全澳跨領域共識」→ 只在 Reddit 成立，X 不支持。應收窄為「Reddit 社群文化態度」。
- ❌「44% 澳洲成人低於 Level 3 識字 → 可推及 WISE 員工」→ 找不到任何 WISE／ADE 專屬識字統計。
- ❌「碎片化 = 所有成效資料都要重講很多遍」→ **不對稱**。投資人／資助方那側是真的碎
  （IRIS+ 對映 50+ 框架，GIIN 與 SROI Network 有對照文件）；
  **採購那側不碎** —— 維州社會採購框架直接認 Social Traders 認證，認證機構本身就是翻譯層。

### 4.4 不要引用的數字

- 「9 成社區組織說缺經費是衡量成效的主要障礙」—— 找不到原始出處
- NDS 2024 職場普查的「50% 流動率、每名新進 2,130–3,320 澳幣」—— 那是**支薪支持人員**，
  不是 WISE 的受支持員工，別混用
- PlanMind 官網自述的「觸及 160,000 名參與者」「平均為計畫爭取到 5,000 澳幣」——
  純行銷自述，無第三方佐證，**不得引用**
- Reddit 分數（Arctic Shift 多在貼文早期擷取，系統性低估）。
  例：r/nonprofit《Grant writing is just rewriting the same information 40 different ways》
  年度排名第 4，但抓取顯示 score=1 且已被版主移除。**引用排名，不要引用分數。**

### 4.5 需人工開啟驗證的 PDF（自動抓取皆 403 或無法解析）

- Social Traders Full Guidance Notes：`https://assets.socialtraders.com.au/downloads/Full-Guidance-Notes.pdf`
- CSI《State of the Social Economy in Australia》完整 PDF 的百分比細分
- 維州社會採購框架買方指引 FAQ／Big Build 申報頁
- Inclusion Australia／CSI《ADE Snapshot》
- ~~**《Understanding the Impact Costs of Work Integration Social Enterprises》**~~
  —— **2026-09-21 已開啟全文並讀完（52 頁）**，不必再找人工開。
  直接下載網址（登陸頁不給，是從頁面連結挖出來的）：
  `https://drive.google.com/uc?export=download&id=1kLHcP0FE5XFXILzchlA-Q0aQzvjGT5Jt`
  內容摘要與可引用數字寫在第 5 節方向 6 的「量化證據缺口」段，**不要重抓**。
- DSS Commonwealth Outcomes Fund 頁（2026-09-21 自動抓取逾時）：
  `https://www.dss.gov.au/social-impact-investing/commonwealth-outcomes-fund`
- NDIA 官方 I-CAN 公告（2026-09-21 自動抓取回 HTTP 403）：
  `https://www.ndis.gov.au/news/10927-new-tool-deliver-simpler-pathway-disability-supports`

---

### 4.6 競品可能是死的 —— 而那把刀是雙面的（2026-09-21 新增，09-21 修訂）

這一輪競品盤點意外撞到兩具屍體：

- **Amplify Social Impact Online**（方向 3）：CSI 1,200 萬澳幣專案的一部分，**免費**、學術驗證，
  因「lower than anticipated take-up」關閉
- **Yume Food Australia**（方向 5）：自我定位社會企業，十年重新分配 1,150 萬公斤食物、
  客戶含 Mars 與 Unilever，2024 年 11 月進入自願管理並清算

**教訓**：查競品時不能只查「有沒有人在做」，必須查「做的人還活著嗎、為什麼死的」。

**而死亡證據是雙面的，兩面都要講**：
- 不利的一面：一個資源更多的前人倒了，對 viability 是不利證據，不能把它說成市場空缺。
- **有利的一面**：CSI 願意投 1,200 萬澳幣、Yume 撐了十年並拿到 Mars 與 Unilever 當客戶——
  這證明**問題是真的**，而且嚴肅的機構驗證過。而他們的死因（CSI 自述：需求分歧、資助方要求不一、
  中小型組織資源不足、技術門檻、既有平台競爭）是一份現成的設計指引。

誠實的用法是兩面都端上桌，然後回答「你憑什麼不一樣」——不是只講其中一面。
⚠️ 2026-09-21 修訂：本節初稿只寫了不利的一面，並據此降級了方向 3、淘汰了方向 5，那是過度推論。

---

## 5. 六個要研究的方向

依優先序。每個都**必須**做競品盤點與付費方分析。
**2026-09-21 更新 —— 六個方向的競品盤點全部完成，六個方向也全部保留。**

⚠️ **先前寫在本檔的「淘汰／降級／通過」判決已於 2026-09-21 撤回。**
撤回理由：評分的七項加權標準裡**沒有新穎性這一項**（清單見 `AI_CONTEXT.md`〈Official event facts〉）。
先前用「已經有人做了」當作淘汰理由，是加了一把評審沒有的尺。
競品存在通常代表需求被驗證過，對 viability 是**有利**證據，同時是一個必須正面回答的問題。

**證據全部保留，判決全部移除。** 每個方向末尾的競品區塊現在讀作
「競爭態勢與我們必須回答的問題」，不是死刑判決書。
方向 6 與方向 3 的重疊問題維持原判定：**不合併**，理由見方向 6 節末。
各方向可直接套用的框架在 `docs/frameworks/`。

### 方向 1 — NDIS 文件編排（競品已盤點，見本節末）

**問題形狀**：身障者必須自己蒐集、編排、辯護證據，對抗削減其經費的機構。

**已有證據**
- Reddit r/NDIS 年度熱門榜幾乎整張都是這件事。代表串：
  《18 Months, 900 Pages of T-Docs and 1,000+ Emails - I WON》↑46
  https://www.reddit.com/comments/1vz9slx
  致勝戰術是自製**證據索引**：「I added an 'evidence index'… referenced quotes from documents
  already in the T-Docs **with page numbers**」
  留言：↑12「many people dont have capacity to approach tribunal this way」／
  ↑7「**severe lack of advocacy services** and competent legal services in the NDIS tribunal space」／
  ↑6「A lot of us are too disabled, ill or fatigued to do all this」
- 《Asked for more supports. Backed up with reports from 5 specialists…》↑63
  https://www.reddit.com/comments/1tk1uoa ——「**ignored 50 pages of evidence** compiled by five
  qualified specialists」
- 《Supports Needs Assessment not fit for purpose》↑47 https://www.reddit.com/comments/1pbx6m5
  ——「**The SNA cannot be appealed.** Only the plan can be appealed and that is driven by the SNA.」
- **跨平台唯一確認點**：NDIS 決策自動化／Palantir／「Robodebt 2.0」
  X：@criprights（Sam Connor，2026-08-15）422 likes／256 reposts／**104 bookmarks**，已 oEmbed 驗證
  https://x.com/criprights/status/2088493752822444511
  Reddit：《Help put a stop to AI-Generated NDIS Plans》↑43 ——「**A machine cannot be held
  accountable, therefore a machine should not make a management decision.**」
- 相關性：RISE 報告指 **44% 的認證社企以身障者為主要受益族群**；評審 Kirubagaran 透過 Koorana
  （NDIS 註冊服務商）連到此領域

**要研究什麼**
1. **競品盤點（最重要）** —— 本專案已用競品檢查刪掉 3 個方向，**唯獨這個方向還沒做過**。
   查：NDIS 申訴／覆議輔助工具、證據整理工具、倡議服務的數位化程度、
   法律科技裡的 tribunal 文件編排工具、以及 Disability Advocacy Network Australia 等組織現用什麼。
   ⚠️ **這裡原本寫「如果已有成熟或免費的產品，這條線當場清掉」——該判準已於 2026-09-21 撤回。**
   競品存在不是淘汰理由（評分標準沒有新穎性這一項），而是一個必須回答的問題。
2. 誰付錢？參與者現金吃緊。候選：support coordinator
   （留言中一位自稱 SSC 者說「I **desperately need an advocate** for 2 of my participants」）、
   plan manager、倡議組織、allied health 提供者、法律扶助。
3. 這算社會企業嗎（交易收入）還是慈善服務？
4. 倫理與法律邊界：協助編排**既有**證據 vs 生成主張；是否構成提供法律意見。
5. **政治風險**：X 上主流敘事是「NDIS 詐騙猖獗」（@bhavdip143「the biggest rort in Australia」
   1336 likes，已驗證）。「幫參與者贏申訴」會被部分人讀成「幫人鑽漏洞」。要準備答案。

**社群搜尋設計**：r/NDIS 改用 `sort=new`（找工具討論而非情緒宣洩）、r/AusLegal、r/disability；
X 追 @criprights 等倡議帳號在推薦什麼工具。

**競爭態勢（2026-09-21 盤點完成）—— 這不是判決，是必須回答的問題**

規則 4 的競品檢查已執行（純桌面研究，未聯絡任何人）。這個問題空間同時被
**免費產品**、**已上市的付費產品**、以及**政府免費申訴代理**三層佔據。

**這代表什麼**：需求被三方獨立驗證過（有人免費做、有人收費賣得掉、政府願意撥款），
對 Social Impact Reasoning 與 Pathway to Sustainability 都是有利證據。代價是我們必須能回答
「$89 的 MagMindLab 與免費的 PlanMind 都在了，你做的哪裡不一樣」。
答不出來就不要選它；答得出來它就是六個方向裡社群痛感最具體的一個。

**EVIDENCE — 直接競品（皆於 2026-09-21 查證）**

| 產品 | 做什麼 | 價格 | 與本構想重疊 |
|---|---|---|---|
| **PlanMind** https://planmind.com.au/ | ReAssess（產出 Reassessment Brief PDF＋會議提問＋書面陳述）、Plan Decoder、Goal Planner、Support Letter Generator、Budget Calculator、Jargon Buster | 官網原話：「**No signup required · No plan data stored · Free to start**」，計算機與辭典「always free」 | 極高。ReAssess 自述「**aligned to the new I-CAN v6 framework**」，連制度轉換都已覆蓋 |
| **MagMindLab** https://magmindlab.com/ | 上傳既有醫療／評估報告 → 約 25 頁 Support Needs Evidence Report、**I-CANv6 草擬評分**、六大 impairment 類別對映、Reasonable and Necessary 結構化報告、**Evidence Gap Checklist**、給治療師的草擬信 | 「**$89 inc. GST**」（自述原價 $109 的促銷價） | **幾乎等同**。「證據索引＋缺口檢查」正是本構想的核心，已經有人做完並在賣 |
| **Novida** https://www.novida.com.au/resources | NDIS 表單白話解釋、信件與陳述範本、逐步檢核表、辭典、資格檢查器 | 官網原話：「**everything here is free**」／「The letters and statements are **free to copy, adapt and use**」 | 中高（範本層） |
| **PWdWA + Legal Aid WA《WA Advocates Internal Review Toolkit》** https://pwdwa.org/how-we-help/ndis/ | 內部覆議工具包＋申請範例＋定期線上說明會 | 免費 | 中（覆議階段的流程指引） |
| **NDIS Appeals Program**（聯邦 Department of Health, Disability and Ageing） https://www.health.gov.au/our-work/ndis-appeals-program | ART 申訴階段配置**受訓身障倡議者**作為支持人，必要時提供**法律代理** | 官方原話：supports are **free of charge**。National Legal Aid：2026–27 起兩年 **1,470 萬澳幣** 續撥 https://nationallegalaid.org.au/news/fed-budget-202627-ndis | 高。這是申訴階段的免費在位者，且剛加碼 |
| **NexLaw ChronoVault** https://www.nexlaw.ai/au/products/chronovault/ | AI 案件時序表／證據編排，產出 court-ready chronology | 商業付費 | 中，但**面向律師**，不是參與者 |

**EVIDENCE — 制度層面的結構性打擊**

自 2026 年中起，NDIA 改以受訓評估者執行 **I-CAN v6** 半結構式訪談（最長約三小時），
由**電腦程式**依評估資料計算預算，取代規劃師裁量。
多個第三方解讀指出，獨立醫療證據**不再是必須被納入考量的項目**，重心轉向功能性描述。
→ 若屬實，「把醫療報告編排得更好以贏得經費」這個前提本身正在被制度拆掉；
而即使轉向功能性紀錄，PlanMind 與 MagMindLab 都已宣稱對齊 I-CAN v6。

**NEEDS MANUAL VERIFICATION**：NDIA 官方頁 https://www.ndis.gov.au/news/10927-new-tool-deliver-simpler-pathway-disability-supports
自動抓取回 **HTTP 403**。上述「獨立醫療證據不再必須被考量」目前只有第三方（plan manager／provider 部落格）
與參議員 Steele-John 提交的 APH 文件 https://www.aph.gov.au/-/media/Estimates/ca/supp2526/Health_Disability_and_Ageing/15_TabledDoc_SenatorSteeleJohn.pdf 支撐，
**尚未從官方原文確認，不得當作事實引用**。

**NOT FOUND**
- MagMindLab 的公司登記／ABN、使用者評價、實際用量（官網僅自述由一位雪梨社工建立）
- PlanMind 的營運者身分（官網僅聲明「fully independent，與 NDIA、政府、任何 NDIS 服務商無關聯」）
- DANA 或其 80 個會員倡議組織實際使用哪套軟體做申訴文件編排
  （查得的只有 NCDA 的 Disability Advocacy Portal，定位是資源庫與系統性倡議資料蒐集，不是文件編排工具）

**剩下的縫隙（評估後認為不值得在 48 小時內押注）**

嚴格說，沒有任何一家在賣「tribunal 階段、帶頁碼的跨文件證據索引」——
也就是 ↑46 那篇致勝貼文真正用的那招。但這條縫隙同時踩到三個地雷：
①申訴階段已有政府免費倡議者＋法律代理在位；②往前一步就是提供法律意見（方向 1 自列的第 4 個風險）；
③付費方問題仍未解（參與者現金吃緊，而 support coordinator 的痛點屬「小組織後台」型，
依 §4.1 的規律在社群上無法取得佐證）。

**給下一位 agent 的指示**：不要重查本方向。若現場有身障領域的真實提案者出現，
可把本表當作「已被佔據的格子」清單使用，但起點必須是對方的問題，不是這個構想。

---

### 方向 2 — 二手店捐贈物「路由」（競品已盤點，見本節末）

**問題形狀**：把每件捐贈物路由到最高價值去向（上架／維修／布料回收／轉贈／回收），
**不是**加速淘汰。

**已有證據**
- 金額：救世軍全國每年約 **600 萬澳幣**處理不可販售品；約 **7,500 公噸**棄置，
  全產業每年 **563 萬澳幣**損失
- 循環經濟規模：RISE 八年累計 **68,050 公噸**垃圾減量
- Reddit（**美國脈絡**）：r/Goodwill《Your charitable donations 😅》↑621
  ——↑201「a majority of stuff that gets donated is trash」，收過「a dead possum in a bag」
  ／↑51「soiled… broken glass… sharp pieces」，且污染會擴散
- **社群修正了產品方向**：年度最高票 ↑2398 https://www.reddit.com/comments/1s90tez
  是員工抗議**被要求丟掉可用品**：「she makes us throw away SO MUCH STUFF」；
  ↑35「So much gets thrown out because it doesn't meet their standards, even though it likely
  meets the standards of people who shop used」；↑75「They used to make us throw away perfectly
  good donations」。高票支持的是**路由**：↑40 可修的送修（城市季度 repair fair）、
  ↑26 髒污織品送動物收容所、↑83 玩具送遊民庇護所
- 安全：《Always check thrift store toys before giving them to kids》↑407（兒童玩具盒內有用過的保險套）
- 競爭壓力（原訊號弱，僅 16 views → **2026-09-21 已由 ABC 報導補強，見本節末**）：X @bigbatnews 2026-09-03
  ——營利二手零售商 Savers 在澳洲擴張至第 19 家店，慈善店擔心捐贈與顧客被抽走

**要研究什麼**
1. **所有捐贈物證據都是美國的。** 澳洲的 Vinnies／Salvos 制度不同（稅務誘因、回收商體系）。
   找澳洲本地證據與實際作業流程。
2. Savers 擴張對澳洲慈善零售的實際衝擊（X 那則太弱，需要報導或產業資料）
3. 競品盤點：澳洲有沒有現成的捐贈物分類／路由工具
4. 資料可得性：**沒有公開的「捐贈物狀態」資料集**，這是最大弱點。要想清楚 demo 怎麼做才誠實。
5. 付費方：二手零售社企（省下的處理成本即回收期）

**社群搜尋設計**：r/australia、r/melbourne、r/perth 搜 op shop；澳洲的二手／節儉相關板；
X 搜 Vinnies／Salvos／Savers。

**競爭態勢（2026-09-21 盤點完成）—— 建議收窄到「店內進貨端分流」**

規則 4 的競品檢查已執行（純桌面研究，未聯絡任何人）。與方向 1 相反：
既有玩家各自佔住**一個分支**，沒有人做**進貨端的跨分支分流決策**，而且澳洲市場尤其空。
另外，方向 2 原本最弱的兩項（澳洲本地證據、Savers 衝擊）在這一輪都補強了，付費方也浮現。

**EVIDENCE — 競品，依佔住的分支分類（皆於 2026-09-21 查證）**

| 分支 | 玩家 | 狀態 | 對我們的意義 |
|---|---|---|---|
| **上架／訂價** | **Thriftify** https://www.thriftify.com/ 照片→AI 生成標題、描述、價格、品牌尺寸年代材質等屬性，跨 eBay／Shopify／Etsy／TikTok Shop 等通路 | 成熟。16 國以上、Oxfam GB（500+ 店）。自述 Oxfam「**292% Increase in listing speed**」「99% sell-through-rate uplift」。£130–550／月，前 500 件免費 | **僅限上架**。官網功能範圍不含「該上架／該修／該回收／該退掉」的判斷。**未提及任何澳洲客戶** |
| **上架／訂價** | **Thriftly**（美國，Google public policy 專文） | 成熟。自述痛點是「25,000 家店、每店 10 個人在訂價、沒有軟體協助」 | 同上，訂價層 |
| **轉賣者個人** | ThriftAI、Underpriced AI、Thrifty 等 | 成熟但**面向淘寶客**，不是店務 | 不重疊，但會稀釋「AI 辨識二手物」的新穎性 |
| **消費者端棄置路由** | **Recycle Mate** https://recyclemate.com.au/ 拍照→AI 辨識→依地理位置給出可回收／可翻新／棄置去向；5,000 項物品、30,000 個地理定位去處，涵蓋全澳各 LGA 垃圾桶制度 | **成熟且免費**。ACOR 與 Adaptation 開發，聯邦 Environment Restoration Fund **200 萬澳幣** 資助＋NSW EPA | ⚠️ **最大碰撞風險**。互動形式幾乎一樣（拍照→這東西該去哪）。必須能明確講出差異：它是消費者丟東西前查詢，我們是店家收到貨後分流。答不出就等於重做免費品 |
| **工業纖維分選** | **Matoha**（NIR＋AI，手持 FabriTell、S-Bench 分選台、FabriBot 機器人 2026 年底試點）、**Fibersort**（英國救世軍貿易公司 SATCoL 在用） | 成熟硬體。Matoha 自述 60 國售出 900 套 | 不同層級（資本設備、纖維成分）。可當成「分流後的下游」引用，不是競品 |
| **實體路由服務（澳洲）** | **UPPAREL** https://upparel.com.au/ 自述收到的約 **60% 為全新或可穿**，轉交 Save the Children、Youth Projects、Djirra 等慈善夥伴；其餘做 UPtex 再生材料；慈善夥伴可**免費退回**用不到的物品 | 營運中 | 路由**已經以服務形式存在**，只是沒有決策工具層。潛在夥伴而非敵人 |
| **慈善紡織收運（澳洲）** | **SCRgroup** | 營運中，規模大 | 同上 |
| **店務系統（澳洲）** | **Tower Systems**（慈善店 POS，註冊慈善半價）、**Qdos**（慈善 ERP＋POS） | 成熟 | 只做銷售端，**沒有進貨端分流智能**。是整合對象也是通路 |

**NOT FOUND**
- 任何**澳洲**面向 op shop 進貨端的 AI 分流／路由工具
- 任何 Vinnies／Salvos／Brotherhood of St Laurence 公開報導過的 AI 分揀試點
  （只查到產業層級的「澳洲慈善機構對 AI 好奇但普遍無力安全導入」的泛論）

**EVIDENCE — 澳洲本地證據（補上原「所有捐贈物證據都是美國的」這個弱點）**

Charitable Reuse Australia（全國慈善再利用組織協會）https://www.charitablereuse.org.au/
- 非法傾倒與不可用捐贈品導致每年 **80,000 公噸**進垃圾掩埋場
- **76% 的澳洲慈善與社企零售商**指非法傾倒是提升社會與環境影響的**最大障礙**
- 倡議各州依 **每公噸 10 澳幣** 補償，全澳合計約 **每年 80 萬澳幣**
- 慈善回收整體：轉移超過 **100 萬公噸**垃圾、募得近 **10 億澳幣**、創造 **5,300+** 個工作

Seamless（澳洲全國服裝產品管理制度，自述為世界第一個循環型產品管理制度）
https://www.seamlessaustralia.com/ ——〈45,000 tonnes at risk〉2026-03-25
- 2024 年澳洲出口 **85,000 公噸**二手衣，**超過一半送阿聯酋分揀**；中東衝突衝擊航線，
  **45,000 公噸**可能改進澳洲本地掩埋
- 2024 年澳洲人買了 **15.1 億件**衣服（人均 55 件）；**220,000 公噸**進澳洲掩埋場；
  含家庭與商用紡織品，全國每年可能丟棄達 **800,000 公噸**

**EVIDENCE — Savers 衝擊（原本只有 16 views 的 X 貼文，現已由 ABC 報導補強）**
- ABC News 2026-07-18〈Geelong op shops worried about arrival of Savers megastore〉
  https://www.abc.net.au/news/2026-07-18/us-thrift-chain-savers-arrival-unsettles-geelong-op-shops/106926136
- ABC News 2026-09-03〈Profitable thrift store using 'smoke screen' to appear charitable, critics say〉
  https://www.abc.net.au/news/2026-09-03/savers-thrift-second-hand-profit-australia-profile/107077786
- 澳洲第 19 家店；母公司市值約 22 億美元；澳洲員工 1,250 人（NSW／VIC／SA）；
  **2025 年支付給澳洲非營利夥伴 560 萬澳幣**，買的是**未分揀的原始貨**
- 戰略含意：**未分揀貨已經有市場價格**。這是「分流值多少錢」的現成標竿，
  也是反論——慈善機構大可把問題賣掉而不是解決它。要準備答案

**付費方（原本最沒把握的一題，現在有答案）**
1. **Seamless Circular Clothing Textiles Fund** —— 每件衣服 4 分澳幣的品牌徵費（符合生態調節標準降為 3 分），
   已在資助收運、**分揀**、再利用、再製造專案，含慈善機構；獲聯邦補助，並在爭取第二期
2. **州政府傾倒紓困** —— 維州已透過 Charitable Reuse Australia 提供財務紓困
3. **零售社企自身的處理成本** —— 省下的掩埋與處理費即回收期

**仍未解決的弱點（不要在 pitch 裡假裝解決了）**
- **沒有公開的「捐贈物狀態」資料集**（原第 4 點）仍然成立。demo 必須誠實：
  用自拍素材或公開二手圖像，不得聲稱用了任何機構的真實資料
- **Recycle Mate 碰撞**：免費、政府背書、互動形式相同。差異化說法要能一句話講清楚
- 規則 5 的檢驗還沒做：二手零售社企是服務對象，但**我們自己**賣工具給他們算不算社企，要想清楚

---

### 方向 3 — 社企的「證據層」（競品已盤點，見本節末）

**問題形狀**：社企要把散落的自家證據，反覆重新表述成認證機構／買方／資助方各自規定的結構。
一個證據庫，三個出口：①Social Traders 認證／重新認證 ②投標與買方社會價值提問 ③資助方與投資人報告。

**已有證據**
- 投標指引原話：評選標準要求「structured evidence mapping」，但「tendering **is not anyone's
  full-time job**」，建議小型供應商「**build a reusable evidence library**」
- CSI《State of the Social Economy in Australia》2025-08-13（n=140）：
  「SEOs consistently reflected on the need for resources, both financial and in terms of
  frameworks, to support social impact assessment」
- GIIN 的 IRIS+ 對映 50+ 指標框架，並與 SROI Network 合出對照文件 —— 需人工 crosswalk
- 認證流程：ST 把申請者歸入影響力模型，蒐集標題影響力活動與「direct social costs」；
  交易未滿 2 年者每年重認證，滿 2 年後每 3 年
- 三個生態系玩家（Social Traders、Social Impact Hub、SECNA）全都在做「讓社企存在、證明影響力、拿到錢」
- **社群聲音為零，而且再搜也不會有**（見 4.1）

**要研究什麼**
1. **為什麼約 12,000 家社企中，RISE 資料集裡只有 636 家取得認證？認證還是免費的。**
   這是整輪研究中最有張力、也最沒答案的問題。維州社會採購框架把 ST 認證當供應商資格，
   FY25 社會採購支出達 **14 億澳幣** —— 免費的門票通往 14 億市場，九成以上的人沒去拿。為什麼？
2. 競品：**CSI 的 Amplify Social Impact（前身 Yardstick）是澳洲本地、近乎免費的直接競品**，
   必須回答「跟它差在哪」。其他：Socialsuite（9,500 澳幣/年起）、UpMetrics（1,788 澳幣/年起）、
   Sopact、Impact Cloud、Sinzer、SAMETRICA（多為投資人端）。
   另查 SECNA 的 SIM 計畫（雪梨市政府出資）評測過哪些工具、結論是什麼。
3. 付費方設計成**認證機構／買方／資助方**，不是現金吃緊的小社企
   （86% 認證社企收入來自交易，1,788–9,500 澳幣/年的 SaaS 買不起）

**demo 資料**（皆免註冊）：ST Full Guidance Notes、RISE 報告與 RISE25 data pack、
IRIS+ 完整指標目錄、ACNC 年度資訊聲明批次資料、維州 SPF 文件、
以及一份真實公開的影響力報告（Yalari Social Impact Report，2025-04-17）作為實跑案例。

**競爭態勢（2026-09-21 盤點完成）—— 付費方設計是這個方向最需要想清楚的一題**

規則 4 的競品檢查已執行。這個方向沒有「被免費競品佔住」的問題，它的問題更嚴重：
**最直接的競品已經死了，而死因正是評審三項評分標準裡的 viability。**

**EVIDENCE — Amplify Social Impact Online 已關閉（最重要的一筆）**

CSI 官方公告 https://www.csi.edu.au/amplify-social-impact/amplify-social-impact-online/
原話：「we have made the decision to close the platform **after lower than anticipated take-up**」。
CSI 執行長列出的成因：各組織需求分歧、資助方要求不一、中小型非營利資源不足、
技術門檻、以及既有問卷平台的競爭。CSI 表示正在尋找「another values-aligned provider」接手底層研究。

背景：Amplify 是 CSI **1,200 萬澳幣**專案的一部分，對澳洲社會目的部門**免費**，
使用學術驗證過的量表，當初宣稱可為部門帶來 3 億澳幣效益。

→ **這對本方向是壞消息，不是好消息。** 不是「沒人做過所以是機會」，
而是「有人用 1,200 萬澳幣、學術背書、完全免費做過，然後因為沒人用而收攤」。
評審問 viability 時，這是最相關的澳洲先例，而它指向反方向。
**不得把 Amplify 關閉說成市場空缺。**

**EVIDENCE — 三個出口分別被誰佔住**

| 出口 | 現況 | 結論 |
|---|---|---|
| ①**認證／重新認證** | Social Traders 自有流程。未查到任何第三方工具 | **NOT FOUND — 真的是空的**，但市場極小（RISE 資料集 636 家，重認證週期 1–3 年） |
| ②**投標與買方社會價值提問** | **已被佔住**。澳洲 AI 投標工具成熟：**Bidhive**（可對歷史投標文件與「company-approved content library」做自然語言檢索並生成回答）、**Doreva**（AusTender 專用，數小時產出合規矩陣與初稿）、**TenderPilot**（澳洲 SME）、**Tender Library** | 「可重複使用的證據庫」在投標這一側**已經是現成商品** |
| ③**資助方與投資人報告** | **Socialsuite 每年 9,500 澳幣起**（Capterra AU 查證）、UpMetrics、Sopact、Impact Cloud、Sinzer、SAMETRICA；免費的學術選項 Amplify **剛死** | 付費端健在但貴，免費端已陣亡 |

**EVIDENCE — SECNA 的 SIM 計畫（原本要查「評測過哪些工具、結論是什麼」）**

https://www.secna.org.au/sim ——由**雪梨市政府**資助，目標是「test and evaluate social impact
measurement tools」並「offer feedback to tool developers」，對 SECNA 會員免費。
**頁面未具名任何受測工具，也未發布任何結論或報告。**
→ 戰略含意：這個領域目前有一個由政府出資、尚未發表結論的獨立評測計畫正在進行。
兩天做出來的工具要進這個空間，等於走進一個還沒開獎的評測場。

**FACT GUARD — 差點被搜尋結果帶偏的一點**

有二手來源稱「Social Traders 認證約需 700 澳幣」。**這是把認證與會員混為一談。**
查證後：**認證本身免費**（依社企產生影響力的州別，由政府與慈善資助方部分補助）；
**Connections 會員**另計，每年 750 澳幣＋GST（另有來源稱會員自 700 澳幣/年起），
新興市場區域另有補助。第 2 節「Social Traders 認證是免費的」這項事實**成立**，不要改。
⚠️ Social Traders 官網的會員與認證權益頁在 2026-09-21 直接抓取皆回 **404**（頁面可能已搬移），
上述金額僅到搜尋摘要層級，**引用前需人工開啟確認**。

**原本最有張力的那一題，答案往壞的方向靠**

「約 12,000 家社企、RISE 資料集僅 636 家認證、認證免費、維州 FY25 社會採購支出 14 億澳幣——
為什麼九成以上沒去拿？」這一輪沒有找到直接研究回答此問題（**NOT FOUND**），
但 Amplify 的死因清單（需求分歧、資助方要求不一、資源不足、技術門檻）是目前**最接近的證據**，
而它暗示的答案是：**不是工具不存在，是這個族群不採用工具。**
若這個推論成立，本方向做什麼工具都會撞到同一堵牆。標為 INFERENCE，未經證實。

**要活下來必須成立的條件（缺一不可）**
1. 付費方**不是社企本身**——必須是認證機構、買方或基金管理方（原第 3 點的設計方向是對的）
2. 不能碰出口②（投標），那裡已有成熟商品
3. 必須能回答「Amplify 免費且有學術背書都收攤了，你憑什麼不一樣」

**給下一位 agent**：本方向優先序**降到方向 2 之後**。若要繼續，先回答上面第 3 個條件，答不出就不要投入。

---

### 方向 4 — 租屋權益（競品已盤點，見本節末）

**問題形狀**：租客面對仲介／房東時，需要知道並援引法條才能守住權利。

**已有證據**
- Reddit r/shitrentals 整板都是租屋不公。代表：《CALL THEIR BLUFF: Real Estate told me I couldn't
  leave. **I quoted the law.** They doubled down.》↑980 https://www.reddit.com/comments/1vxv3b3
- r/AusLegal 充滿「我的權利是什麼」的具體個案
- AIHW：FY24–25 有 126 萬低收入家戶處於住房財務壓力
- r/australia 與 r/shitrentals **獨立出現同一則**：「Australia spends more on tax breaks for
  landlords than social housing, homelessness and rent assistance combined」
- ⚠️ X 上此議題與**移民政治**深度綑綁（@jordanhknight_ 3101 likes、@DeanMcCrae1 2457 likes，
  皆已驗證）。**這是政治第三軌，不要碰**，但要知道它存在。

**要研究什麼**
1. 這算社會企業嗎？付費方是誰？租客付不起。
2. 競品：各州租客工會（Tenants' Union NSW 等）已提供什麼？是否已數位化？
3. 法律邊界：提供法條資訊 vs 提供法律意見
4. 為什麼這比方向 1、2、3 低優先：**不是社企形狀**，且政治風險高

**競爭態勢（2026-09-21 盤點完成）—— 最強的反對意見是「對象不符」，不是競品**

規則 4 的競品檢查已執行。這是四個方向裡被佔得最滿的一個：
免費、成熟、法定經費支撐，而且**租客工會自己已公開對「AI 做租務建議」提出警告**。

**EVIDENCE — 直接競品（皆於 2026-09-21 查證）**

| 產品 | 做什麼 | 狀態 |
|---|---|---|
| **Dear Landlord**（Justice Connect Homeless Law） https://apps.justiceconnect.org.au/dear-landlord/ | 免費線上自助工具：協助維州租客了解權利、**草擬給房東的信**（協商分期或減租）、**準備 VCAT 或申請覆審**、找財務與法律協助 | **2020 年上線至今超過 10 萬名租客使用**，由法律慈善機構營運 |
| **Tenants' Union of NSW《Rent Increase Negotiation Kit》** https://www.tenants.org.au/resource/rink | **Letter Generator**：查詢所在區域租金行情，產出個人化信件與郵遞區號資料摘要，「可用於協商**或作為仲裁庭的佐證**」。資料來自 NSW Fair Trading | 免費，peak body 營運 |
| **Rent AI** https://www.fluidic.io/rent-ai | 澳洲 iOS＋Android 上架，白話拆解租約、標示風險，**與本地律師事務所合作** | 商業產品，已上線 |
| **Renters Rights AI** https://www.rentersrights.ai/ | 選州別後就租金調漲、維修、通知、押金對話；自述資料存放澳洲、不用於訓練公開模型 | 商業產品，有免費層 |
| **TAAS 體系** | NSW 有 15 個綜合型租客建議與倡議服務、4 個原住民專責服務；南澳 RentRight SA 由州政府 4 年 **140 萬澳幣** 支應 | **對租客免費** |

**付費方問題無解（原第 1 題的答案）**

NSW Tenants' Union 的主要經費來自 **NSW Fair Trading 管理的租賃押金委員會利息帳戶**與
物業服務法定利息帳戶，加上 Legal Aid NSW 的社區法律中心計畫。
→ 這個領域的付費方**已經是法定基金，而且它買的是「對租客免費」**。
沒有空間插進一個要收費的產品，而要做免費的就得先解決「誰出錢」——答案已經被佔走了。

**⚠️ 最刺的一筆：peak body 已公開警告 AI 做租務建議**

Tenants' Union of NSW 部落格〈AI & tenancy advice: Helpful tool or hidden risk?〉
https://www.tenants.org.au/blog/ai-and-tenancy-advice-helpful-tool-or-hidden-risk
原話大意：LLM 取材自不同來源與時期，回應快，但可能產出**過時、不完整或根本錯誤**的資訊；
租務案件的結果往往取決於脈絡、證據與親身經歷。
→ 在一個有社會部門評審的場子提「AI 租客權益助手」，等於直接對上該領域 peak body 的公開立場。
這不是可以靠 demo 做得好就繞過的風險。

**加上文件原本就記錄的兩點**
- **不是社企形狀**（原第 4 點）：服務對象是個人租客，不是社會企業
- **政治第三軌**：X 上此議題與移民政治深度綑綁（已驗證，見上方證據）

**給下一位 agent**：本方向仍在檯面上，但「對象是否為社會企業」必須先解決。框架見 `docs/frameworks/direction-4-renter-rights.md`。

---

### 方向 5 — 食品詐標／食物系統（競品已盤點，見本節末）

**問題形狀**：待定。目前只有議題熱度，沒有可操作的營運問題。

**已有證據**
- **整份掃描分數最高的單篇**：r/AskAnAustralian ↑2244、394 則留言
  https://www.reddit.com/comments/1vatpop —— Four Corners 揭露 40% 食品標示不實、
  牛絞肉驗出馬肉、Leggos 番茄醬標示澳洲產但約 60% 為中國產；↑532 補充香料含鉛
- ⚠️ 最高票留言是 **↑512「Because we're all tired」** —— 憤怒疲勞
- 食物救助面：Foodbank 2025 飢餓報告（2025-11-05）三分之一家戶糧食不安全（350 萬人）、
  20% 嚴重（年增 1pp）；**僅 0.2% 剩餘食物被捐出**，救援「集中在零售端且主要在大都會區」
- 競品：**OzHarvest 已有成熟且免費的 Food App** 做捐贈者↔機構媒合，並用 Rosterfy 管志工
- X 上幾乎無食品詐標討論（單平台訊號）

**要研究什麼**
1. 供應鏈驗證在兩天內不可能做。**要找的是這個議題裡有沒有一個小的、營運層面的、社企形狀的問題。**
2. 若走食物救助：真正瓶頸是**供給**（0.2% 捐出率）不是資訊，
   一張需求熱點地圖回答不了「所以問題解決了嗎」。要想清楚。
3. 為什麼排最後：熱度最高但可行性最低

**競爭態勢（2026-09-21 盤點完成）—— 兩條支線要分開看，可行性差很多**

規則 4 的競品檢查已執行。兩條支線分開檢查，結論都是不要做。

**支線 A：食品詐標 —— 缺口是實驗室與執法權，不是軟體**

- ABC Four Corners 2026-07-27〈Food fraud investigation reveals the disturbing truth behind the labels〉
  https://www.abc.net.au/news/2026-07-27/food-fraud-investigation-reveals-truth-behind-labels/106960116
  委託 **Source Certain** 實驗室做鑑識檢測：**超過 80%** 受測 Leggo's 番茄糊的化學特徵與**中國產**番茄一致；
  三個薑黃品牌驗出**鉻酸鉛與氧化鐵**；另涉及「籠外蛋」與澳洲海鮮標示
- **關鍵原話**：食品體系「largely built to protect consumers from **unsafe** food… **not fraud**」；
  前 NSW 食品局執法人員表示澳洲**不例行檢查食品詐標**
- **ACCC 已於 2026-08-07 啟動初步調查**，對象包括 Aldi、Coles、Leggo，FSANZ 表態支持
  https://www.accc.gov.au/about-us/news/media-updates/accc-looking-into-four-corners-food-claims

→ 判定：產地驗證靠的是**同位素與微量元素鑑識**（Source Certain 做的事），不是資訊工具能補的缺口。
而且**監理機關已經接手**。公民端的空缺在兩個月內被填掉了。
兩天做一個「揭露標示不實」的軟體，既無法驗證任何事，也會與已在進行的法定調查重疊。
（呼應原文件已記錄的 ↑512「**Because we're all tired**」——憤怒疲勞加上監理已動作，這題的公民動能只會更低。）

**支線 B：食物救助 —— 在位者佔八成，而瓶頸是供給、物流與稅制**

| 玩家 | 規模 | 狀態 |
|---|---|---|
| **OzHarvest** | 自 **2,000+** 家商業據點收運，**免費**直送 **1,500+** 家慈善機構；自有 Food App | 成熟且免費 |
| **Foodbank ＋ OzHarvest ＋ SecondBite** | 三家合計提供澳洲 **超過 80%** 的食物救助 | 高度集中 |

- **OzHarvest Frontline Report 2026**：每月**超過 74,000 人**被食物支援拒於門外；
  約三分之一的慈善機構表示需要更多食物；70% 表示過去 12 個月求助人數增加；
  **若沒有 OzHarvest 的免費配送，43% 的慈善機構必須縮減服務，超過一半將完全無法取貨**
- **稅制才是槓桿**：目前澳洲**沒有**全國性的捐贈剩食誘因，捐贈與丟棄在稅務上待遇相同，
  實質上在勸退捐贈
- 成本衝擊：燃料、柴油、肥料成本飆升與荷莫茲海峽封鎖造成的供應限制，使需求再增 **31%**

→ 判定：證實原文件第 2 點的擔憂。瓶頸是**供給、冷鏈物流經費與稅制**，不是媒合資訊。
一張需求熱點地圖回答不了「所以問題解決了嗎」，而媒合這一層已由免費且規模化的在位者佔住。

**⚠️ 決定性的一筆：這個領域最像我們的那家澳洲社企已經倒了**

**Yume Food Australia**（2014 年由 Katy Barfield OAM 創辦）——B2B 剩食交易平台，
**自我定位為社會企業**，企業客戶包括 Mars、Unilever、Kellanova、General Mills，
曾募得 **200 萬澳幣**。十年成績：重新分配 **1,150 萬公斤**食物、為製造商回收 **3,000 萬澳幣**。
**2024 年 11 月進入自願管理，其後清算並尋求出售**，媒體記述為「在艱困市場中資金耗盡」。
https://www.smartcompany.com.au/startupsmart/yume-food-collapses-into-liquidation-decade-of-fighting-food-waste/

→ 與方向 3 的 Amplify 同一個形狀：**不是沒人做過，是做過的人做到這個規模仍然倒了。**
評審問 viability 時，這是本領域最相關的澳洲先例。

**給下一位 agent**：本方向仍在檯面上，支線 B（食物救助）比支線 A（詐標）可行得多。框架見 `docs/frameworks/direction-5-food-system.md`。

### 方向 6 — WISE 就業成效申報與 Outcomes Fund（競品已盤點，見本節末）

**問題形狀**：WISE（工作整合型社會企業）營運主管，要把僱用受就業障礙者所產生的成效，
彙整成資助方或 Outcomes Fund 要求的格式。

**⚠️ 與方向 3 的關係（研究時先解決這題）**
方向 3 的三個出口之一就是「資助方與投資人報告」，因此本方向與其**部分重疊**。
差別在於：本方向的使用者、資料與付費方都不同 —— 使用者是 WISE 營運主管而非認證負責人，
資料是**就業成效**（安置、留任、時數）而非影響力敘述，付費方可能是 Outcomes Fund 管理方而非認證機構。
**研究的第一件事就是判斷：這該併入方向 3，還是獨立成題。** 別假設答案。

**已有證據**
- CSI《State of the Social Economy in Australia》（2025-08-13）指出
  **WISE 是澳洲與國際上最大的社會企業類別**
- 國會 Select Committee on Workforce Australia Employment Services 文件原話：
  就業基金支出「**time consuming and burdensome**」，且聯邦就業服務經費
  「largely not been available to WISEs」，限制其規模化
- 政府回應設立 **1,160 萬澳幣的 Social Enterprise Development Initiative**（2023–24 預算）
  與 **1 億澳幣的 Outcomes Fund**
- Melbourne Social Equity Institute／UQ《WISE Perspectives — Ecosystem Insights Report 2024》：
  WISE 是「people-centred, combine work and support」，而 Workforce Australia 是
  「work-first」、合規導向，兩者**結構性不相容**（完整 PDF 為 403，僅取得登陸頁框架）
- RISE 報告：全澳社企貢獻約 160 億澳幣／年，其中約 **89,000 個工作**給被就業市場排除的人；
  八年累計 13,383 個工作、100 萬小時訓練
- 規模數字有爭議：SECNA 的 WISE Hub 稱全澳「almost 7,000」家 WISE，
  **高於 RISE 自身資料集所能支持的數字** —— 當作倡議估計，不是查證過的計數
- **社群聲音為零**（Reddit 與 X 皆無），原因見 4.1

**要研究什麼**
1. 先解決上面的重疊問題
2. **競品盤點**：NDIS／身障個案管理軟體（SupportAbility、Lumary、Carelink）已覆蓋合規文件、
   排班、計費 —— 這層**已飽和，不要碰**。要查的是**成效申報**這層有沒有現成工具，
   以及 SROI 顧問服務（如 Social Ventures Australia）的實際收費與涵蓋範圍
   —— 顧問收費的存在本身證明有付費意願，這是比方向 3 更清楚的交易收入論證
3. **量化證據缺口（重要）**：找不到任何 WISE 專屬的督導工時、員工流動率或到職成本數字。
   公開紀錄裡沒有。**不要編造，要誠實說「有記載但未量化」。**
   （再次提醒：NDS 2024 職場普查的 50% 流動率是**支薪支持人員**，不是 WISE 的受支持員工）
4. **倫理紅線（硬性）**：為了向資助方申報而彙整個別受支持員工資料，
   極易滑向個人績效追蹤或工作能力的隱含判定。**只能做彙總，不得做個別員工的評分、監控或能力推論。**
5. 付費方：WISE 本身（取代付費顧問）或 Outcomes Fund 管理方

**資料可得性**：無公開的員工層級資料（本應如此，屬隱私敏感）。
Demo 只能用合成或彙總資料 —— 這是本方向最大的弱點，要先想清楚怎麼誠實呈現。

**競爭態勢（2026-09-21 盤點完成）—— 付費方證據最硬；與方向 3 維持獨立，不合併**

**先回答重疊問題（原第 1 題）：不要併。**
理由不是使用者不同（那是原本的假設），而是**付費方的性質完全不同，且只有這邊有錢**：
方向 3 的付費方要從頭說服，而本方向的付費方是**已撥款、有法定用途的政府資金**，見下。
方向 3 的工具層剛死（Amplify），本方向的工具層從來沒被填過。合併會讓好的那半被壞的那半拖下水。

**EVIDENCE — 付費方（本輪所有方向中最硬的一組）**

- **Commonwealth Outcomes Fund**：**1 億澳幣**、自 2024–25 年起、最長 10 年，由**社會服務部（DSS）**管理。
  依成效付款，**直接支付給服務提供者與社會企業**，也透過州與領地政府支付。
  三個重點領域之一正是「**people facing barriers to employment**」——就是 WISE 的定義族群。
  各投資組合的參數於 **2026 年初**進行跨轄區共同設計。
  https://www.dss.gov.au/social-impact-investing/commonwealth-outcomes-fund
- **SEDI（Social Enterprise Development Initiative）**：2023–24 至 2026–27。
  Impact Investing Australia 於 2024–2026 執行 **8 輪**競爭型撥款，
  收到 **900+ 份意向書、400+ 份申請**，選出 **56 家**社企，每家最高 **12 萬澳幣**。
  ⭐ **補助用途明文包含「evaluation and impact measurement」**——這是政府直接出錢讓社企去買影響力衡量服務。
  已延長一年，約 **260 萬澳幣**；另有 **294 萬澳幣**的第一民族專責管理方。
- **顧問市場存在＝付費意願存在**（原第 2 點的論證成立）：SVA Consulting 自 2007 年起完成
  400+ 專案、服務 200+ 組織。其 **Social Value & SROI 培訓**早鳥價 **2,095 澳幣**
  （非營利 1,569 澳幣），標準價 2,305 澳幣（非營利 1,727 澳幣）。
  ⚠️ **SROI 顧問專案本身的收費未公開（NOT FOUND）**，官網只寫「contact consulting team」。
  培訓價格只能當下限訊號，不得當作專案報價引用。

**EVIDENCE — 競品與碰撞**

| 玩家 | 做什麼 | 對我們的意義 |
|---|---|---|
| **ReadyTech《Job Ready》** https://readytech.io/what-we-do/employment-services/products/job-ready/overview | DES 與 Workforce Australia 提供者專用：集中管理成效、**成效申報預測**、**證據文件管理**、個案量管理、就業後支持 | ⚠️ 成效申報這層**在就業服務體系內已被佔住**。但文件既有證據指出聯邦就業服務經費「largely not been available to WISEs」——**WISE 基本上不在那個體系內**，所以 ReadyTech 服務不到他們。**這就是楔子，但也要準備好被問「那為什麼不是 ReadyTech 順手做」** |
| **Social Enterprise Australia 的「shared data system」** https://www.socialenterpriseaustralia.org.au/news/a-shared-data-system-for-the-sector-etcxr | 與墨爾本大學 Melbourne Social Equity Institute、Social Enterprise World Forum 合作建立部門共享資料系統；Lord Mayor's Charitable Foundation 種子資金、**Minderoo Foundation 多年期支持** | ⚠️ **最大碰撞風險**。peak body 加大學加慈善基金已在建「部門層級」資料基礎設施。差異必須講清楚：他們做**部門統計**，我們做**單一 WISE 的成效申報**。講不清楚就是重複投資 |
| **NDIS／身障個案管理軟體**（SupportAbility、Lumary、Carelink） | 合規文件、排班、計費 | 文件原本就判定已飽和，**維持不碰**。本輪未發現改變 |

**量化證據缺口：2026-09-21 下午已讀全文，缺口部分補上**

全文（52 頁）已下載並讀完。**先講不利的一面**：報告在執行摘要裡**明文拒絕揭露** Impact Cost
百分比——「this report does not disclose Impact Cost Percentages at an aggregated or individual
level for the five WISEs in the sample」，理由是樣本只有 5 家、不可一般化，要等下一階段更大樣本。
所以「WISE 多負擔幾 % 成本」這個數字**仍然不存在**，不得宣稱、不得估算。

**但可引用的東西比預期多。** 以下全部出自該報告，**性質是 5 家 WISE 的從業者自述估計，
不是統計**，引用時必須連這個限制一起講：

- **督導工時（原本完全找不到的那一格，現在有了）**
  - WISE #3：第一線團隊主管投入在受支持員工身上的時間，是一般職場的 **2–3 倍**
  - WISE #3：一般組織的 L&D 預算約為薪資的 **3.5%**，而 WISE 投入約 **25% 的工作時數**在發展性活動
  - WISE #5：領導層 **20–50%** 的時間花在支持性對話上
  - WISE #1：通才 HR 職位因社會目的而**多出 40–50%** 的時間負擔
  - 到職期（onboarding）典型 **2–12 週**，WISE #5 稱可延長至 3–9 個月
- **出勤**：WISE #3 自述缺勤率首月約 **30%**，後期回落到約 **15%**；
  其對照的一般企業約 **10%**。⚠️ 這是單一受訪者的估計，不是普查
- **工時上限**：Centrelink 可評定 DES 參與者每週僅能工作 8 小時 ——
  要湊滿 1 個 40 小時人力就得僱 **5 個人**，薪資／退休金／WorkCover 隨人頭而非工時增加
- **Impact Cost 的組成（有百分比，這部分報告有給）**：五家 WISE 一致以**員工成本**為最大宗，
  佔各自 Impact Cost 的 **54%／69%／82%／84%／86%**；其餘為房產、外部訓練與其他
- **樣本輪廓 —— 這一條對產品設計最重要**：五家 WISE 的 FTE 為 **4／4／13／19／26**，
  年總收入 **0.2／2.0／2.3／3.1／4.0 百萬澳幣**。
  **使用者是十幾人、年收入數百萬的小組織**，沒有資料團隊，也買不起企業軟體
- ⭐ **「更詳盡的影響力衡量」本身就被列為一項 Impact Cost**：
  報告把「為了管理社會目的與滿足資助方申報需求而做的、比一般組織更細的影響力衡量」
  寫進員工成本項下（WISE #1 原話：「we prioritise certain roles like impact, measuring impact
  to the degree that we do… The reporting is different」）。
  **這是目前最直接、最可引用的一句「申報工作有成本」的官方級證據。**

書目：Pullen, T., Webster, J., & Ward-Christie, L. (2023). *Understanding the Impact Costs of
Work Integration Social Enterprises.* Centre for Social Impact, Swinburne University of Technology.

**另外兩件從這份報告裡撿到的事**
1. 樣本是從 **Payment by Outcomes Trial 3（PBO3）** 的參與社企裡招募的，中介方是
   **White Box Enterprises** —— 這條線索引出本輪最重要的發現，見下一段
2. 報告結尾寫「**A tool to assist WISEs to implement this framework is now under development**」
   （2023-11）。**2026-09-21 遍尋不著該工具上線的任何跡象**，只找到同一研究網絡的 Seedkit（見下）。
   ⚠️ 這是 NOT FOUND，不是「確定沒做」

---

**第二輪競品（2026-09-21 下午新增）—— 這一段會改變方向 6 的說法，務必讀完**

**① White Box Enterprises ＝ 這個功能已經有人在做，但是用人做的**
https://whiteboxenterprises.com.au/innovate/payment-by-outcomes-trial/

- **PBO3**：DSS 與 White Box 合作，2022-07 起至 **2026-03** 結束（最終成效量測延至 2026-09-30）。
  White Box 作為**聚合者（aggregator）**，統籌 **17 家**就業型社企，
  社企在受僱者滿 6／12／18 個月時依成效收款
- 成效（Taylor Fry 精算比對 DES 公開資料）：**12 個月留任率 69%，DES 為 26%**；
  首年平均個人所得約 **17,000 澳幣**；若推廣，五年可為政府省 **2.2 億澳幣**（20% 成本節省）
- **WorkFoundations**（DEWR，2024 年預算 2,190 萬澳幣配套中的就業方案，實際投入 1,000 萬澳幣，
  **16 家**機構，撥款協議 2025-07 簽定）：White Box 同樣擔任**全國聚合者**，
  2026-03 起與 **8 家**社企合作，明文「capture key data and insights」，
  追蹤三件事：**留任、支持成本、參與者成效**

  > ⛔ **這三件事就是方向 6 原本要做的事。** 必須正面承認。

- ⚠️ **最不利的一條證據**：CSI 的 PBO3 第二年評估報告原話——聚合者模式
  「reduces transaction costs of PBOs, with some social enterprises describing Year 2 of PBO3
  as **BAU**」，並對比「traditional PBOs which are seen by service providers to come with a
  **high administrative burden**」。
  **也就是說：在 PBO3 裡，申報負擔對社企來說並不痛，因為 White Box 幫他們扛掉了。**
  原本「WISE 被申報壓垮」的問題陳述，**對這 17 家不成立**。
  https://whiteboxenterprises.com.au/wp-content/uploads/2024/11/CSI-Evaluation-of-the-Payment-by-Outcomes-Trial-3_Year-2-Report_November-2024.pdf

- **但同一段也給了有利的一面**：負擔是**真的存在**的（沒有聚合者的傳統 PBO「high administrative
  burden」），只是被一個人力中介吸收了；而這個中介一次只服務 **8–17 家**，
  且 CSI 自己把聚合者模式定位為「potential pathway for **scaling and replication**」。
  → **誠實的定位是：White Box 不是要打倒的競品，是最可能的客戶或夥伴**，
  要問的問題從「WISE 痛不痛」變成「**這個由人扛的協調功能，要怎麼從 17 家擴到幾百家**」

**② Seedkit ＝ 免費、政府出資、大學託管的影響力申報平台（與方向 3 的 Amplify 同型）**
https://seedkit.com.au/

- CSI Swinburne ＋ 墨爾本大學 Melbourne Social Equity Institute 共同開發，
  維州政府 **100 萬澳幣**資助，**2023-11 上線**，目前由墨大託管、Minderoo Foundation 支持
- 定位：**免費**、自助式，給中小型澳洲社企選指標→輸入資料→產生儀表板與可下載報告
- **與我們的差異（查證後仍成立，但只剩薄薄一層）**：
  Seedkit 做的是**自選指標的追蹤與通用報告**，站上**沒有任何針對特定資助方申報格式的
  範本或匯出**。方向 6 的楔子「把營運紀錄對映到**這一份**資助方要的格式」仍未被填
- ⚠️ **兩個警訊**：(a) 網站最新消息停在 **2025-07**，2026 年無更新（不等於死，但要注意）；
  (b) 這是**和 Amplify 同一個研究網絡、同一種「免費＋學術背書」模式**，
  而 Amplify 正是因無人採用而關閉（§4.6）。**免費的東西沒人用，不代表付費的就會有人用**
- ⚠️ 同時這也修正了上表對 SEA「shared data system」的描述：那套系統的技術底座就是 Seedkit，
  所以「部門統計 vs 單一 WISE 申報」的切分**仍然成立，但邊界比原本寫的更近**

**③ 申報格式其實是多份、且有一份是穩定的**
- **Social Traders 認證**：收集**逾 200 個資料點**，含影響力活動與**對應的交付成本**，
  對齊最近一個完整財政年度；成立未滿兩年者**每年**重新認證，滿兩年者**每三年**一次
  → 這是一份**強制、週期性、格式穩定**的申報，比參數還在共同設計的 Outcomes Fund
  更適合當 demo 的目標格式
- 同一來源可用來界定可觸及規模：Social Traders 認證社企中 **53%** 以就業／訓練為主要影響模式，
  即 **294 家**，共直接僱用 **14,013 名**受支持員工（Pace 2023）。
  ⭐ **這個數字比 SECNA「almost 7,000 家 WISE」的倡議估計可靠得多，優先用這個**
- 其他同時並行的格式：PBO3 的 6／12／18 個月里程碑、WorkFoundations、
  EPRI（難民就業，2026-05 延長一年、770 萬澳幣）、SEDI 撥款核銷、各州社會採購

**④ 一條必須修正的舊證據（我們自己之前引用的）**
原文引用 2023 年國會委員會的「聯邦就業服務經費 largely not been available to WISEs」，
並以此論證「所以 ReadyTech 服務不到他們」。**這句話到 2026 年已部分過期**：
WorkFoundations 由 DEWR 直接撥款給 16 家社企（協議 2025-07），EPRI 亦然。
**仍然成立的部分**是：這些錢走的是**專案型撥款**，不是 Workforce Australia／DES 的服務提供者合約，
所以 WISE 依舊不是 ReadyTech 那套系統的使用者。**引用時要用修正後的版本，不要再照抄原句。**

---

### 第三輪研究（2026-09-21 傍晚）—— 市面產品全景、補助要填什麼、有哪些能申請

**⚠️ 本節最重要的一句話**：上一輪寫的「沒有人做資助方格式對映」**已被推翻**。
海外商業產品宣稱做了，只是沒有做澳洲的格式。詳見 A-3。

#### A. 市面產品盤點 —— 分五層，每層的佔位者都不同

**A-1 澳洲部門層（免費、政府或大學出資）**

| 產品 | 狀態 | 對我們的意義 |
|---|---|---|
| **Seedkit** https://seedkit.com.au/ | 免費，維州政府 100 萬澳幣，墨大託管，2023-11 上線；最新消息停在 2025-07 | 直接對到同一批使用者。**無資助方格式範本／匯出**（已查證） |
| ~~Amplify Social Impact Online~~ | **已關閉**（CSI 1,200 萬澳幣專案，免費，因無人採用） | 同型前例，見 §4.6 |

**A-2 商業影響力衡量 SaaS（全球，有澳洲據點）**

| 產品 | 事實 | 備註 |
|---|---|---|
| **Socialsuite** https://www.socialsuitehq.com/ | 墨爾本＋Austin＋NYC；社會影響力業務客戶 **75+ 非營利**（含 Habitat for Humanity International）；主力已轉向 ESG／永續合規 | **訂價未公開（NOT FOUND）**，只能報價洽詢 |
| **Sopact**（Impact Cloud／Sopact Sense） | 定位在資料收集的下游，接 CRM／個案系統／會計系統 | ⛔ 見 A-3 |
| **UpMetrics** | 偏資助方端的投資組合視角、標準化指標框架 | 據第三方比較文，2026 年仍不做開放式文本的 AI 分析 |
| **Makerble** | 第一線日常營運＋參與者成效放同一個工作區 | — |
| **Clear Impact Scorecard** | RBA（Results-Based Accountability）的標準工具 | 若資助方要的就是 RBA scorecard，它是直球對位 |
| **Bonterra**（原 Apricot／Social Solutions） | 大型個案管理＋成效 | 企業級，非 4–26 人組織的價位 |

⚠️ **上表多數描述來自各家自家或競品比較行銷內容，屬廠商宣稱，未經獨立驗證。**
尤其 sopact.com 的「六大工具比較」「十大平台比較」等頁面是 Sopact 自己寫的，不是中立評測。

**A-3 ⛔ 推翻我們上一輪結論的發現：資助方格式對映，海外已經有人做**

- **Sopact** 自述：「maps the same evidence to SDGs, IRIS+, a logic model, **a funder template**,
  or a custom framework, then **maps each funder's questions to that shared evidence base**」，
  且不同資助方可拿到不同側重的客製報告
- **Knack**：每個資助方的報告是底層資料的一個「saved view」（不同篩選／欄位／分組），設定好之後一鍵產出
- **LiveImpact**：AI 產生客製報告，並有導入專員協助對映欄位

→ **所以「一份資料產出多個資助方格式」這個概念不是空白格，而是海外已商品化的功能。**
（⚠️ 以上三條全是**廠商自述**，沒有獨立驗證過實際做得多好。）

**我們還剩下的差異（誠實版，只剩三條，且沒有一條是「沒人做過」）**：
1. **澳洲的格式沒有人做**：Social Traders 認證、SEDI、DSS 的 AWP／AWPR、PBO 里程碑、
   各州社會採購——這些都是澳洲本地格式，上述產品沒有一家宣稱支援
2. **目標組織太小**：Impact Costs 報告的樣本是 **4–26 FTE、年收入 0.2–4.0 百萬澳幣**。
   這個價位帶買不起 Bonterra，也不會有導入專員。Seedkit 免費但不做格式
3. **倫理紅線寫進程式**：沒有任何一家把「拒絕個人層級輸出、群體小於 5 人拒絕彙總」
   做成程式層的硬性檢查。這是我們唯一無法被「他們順手做掉」的差異

**A-4 補助流程層（申請與核銷的管道，不是成效衡量）**

- **SmartyGrants**（Our Community，墨爾本）：**澳紐使用率最高**的撥款管理系統，
  數百家政府／慈善／企業撥款方在用，已擴至英國與歐洲。
  **注意方向性**：它是**撥款方**的系統，社企是在它的表單裡填答的那一方
- **GrantConnect** grants.gov.au：聯邦補助的官方公告與文件平台
- **AI 寫補助申請書工具**（全是美國市場）：Grantable、Instrumentl、GrantCopilot、
  Grant Assistant、Grantboost。做的是**找資助方＋草擬申請文字**，
  **不是**把營運紀錄算成申報數字——和我們不同格，但評審可能會拿來問

**A-5 個案管理／就業服務層（已飽和，維持不碰）**

ReadyTech Job Ready（DES／Workforce Australia 專用）、Bonterra、CHARMS（支持性就業）、
FAMCare、SupportAbility／Lumary／Brevity／ShiftCare（NDIS）。

**A-6 人力聚合者層 —— 這層才是真正的在位者**

**White Box Enterprises**：PBO3 17 家、WorkFoundations 8 家。用人做，不是用軟體做。
詳見上一節。

#### B. 申請官方補助到底要填什麼（欄位層級，已查證）

**B-1 Social Traders 認證／重新認證（⭐ demo 首選目標格式）**
- 法人文件：章程／公司章程／股東協議／合作社章程／信託契約（依法人型態）
- 財務：**最近兩個財政年度**的損益表與資產負債表（查核財報或管理帳皆可）；
  未滿兩年者交至今財報＋營運計畫＋12 個月財務預測
- 影響力：**少量影響力指標＋社會成本（social costs）**，對齊**最近一個完整財政年度**，
  指標內容依該社企的影響力模式而定
- ABN、佐證文件（營運計畫、年報、行銷素材）
- 時程：申請到結果約 **4–5 週**；未滿兩年**每年**重新認證，滿兩年**每三年**
- 整體資料集：Social Traders 對每家社企收集**逾 200 個資料點**（人口、影響力、成本、財務）
- ⚠️ 完整指引 PDF（`assets.socialtraders.com.au/downloads/Full-Guidance-Notes.pdf`）
  **2026-09-21 再次嘗試下載，回 S3 AccessDenied**，欄位全表仍未取得。維持在 §4.5 待辦

**B-2 ACNC 年度資訊報表（AIS）—— 所有註冊慈善機構每年強制**
- 必填含**員工人數與志工人數**（志工含無給職董事與企業志工時數；不確定時用最佳估計）
- 依規模（小／中／大型）決定要附的財務報表層級
- ⚠️ 逐題清單未取得：ACNC 網站 2026-09-21 連續逾時。
  官方有「2026 AIS Hub」與逐題指引，**需人工開啟**：
  `https://www.acnc.gov.au/for-charities/annual-information-statement`

**B-3 DSS／Community Grants Hub（聯邦補助拿到之後的申報）**
- **Activity Work Plan（AWP）**：寫你打算怎麼交付、如何對齊方案成效與物有所值；
  需經授權簽署人簽名；由 Funding Arrangement Manager 協助對齊部門要求
- **Activity Work Plan Report（AWPR）**：對著 AWP 回報達成情形
- 申報項目與期限寫在撥款協議的 **Item E. Reporting**
- ⭐ **範本每個文字欄位建議 300 字以內** —— 這是一個很具體的產品設計約束
- 若不需 AWP，則依協議附表的里程碑交進度與績效報告

**B-4 SEDI（拿補助前後都要交東西）**
- 流程：**線上 EOI 問卷 → IIA 電話確認資格 → 受邀提交正式申請 → 專家小組評審**
- 資格門檻（First Nations 線已查證）：**年營收 > 5 萬澳幣、交易收入 > 3.5 萬澳幣／年**；
  交易收入定義為「以可重複的方式向不同客戶銷售商品或服務所得」；
  **補助金額不得超過年營收**
- 金額：First Nations 線 **5–12 萬澳幣**，含最多 **20%** 內部成本
- ⭐ **獲補助者須在補助期間建立「Impact Measurement Framework」與「Business Plan」**
  （若尚未具備）—— **這是一條直接的產品鉤子**
- 不可用於：一般營運費、房地產、車輛、裝修、薪資、IT 系統維護、租金、辦公用品、行政管銷

**B-5 PBO3 型的成效付款**：受僱者滿 **6／12／18 個月**觸發付款，
另有社企里程碑與轉銜里程碑之分，一名參與者最多可觸發 **5 個**里程碑。

**B-6 一家 WISE 同時面對的格式數量** —— 這就是問題陳述本身：
Social Traders 認證 ＋ ACNC AIS ＋ 各筆聯邦補助的 AWP／AWPR ＋ SEDI 核銷 ＋
PBO／WorkFoundations 里程碑 ＋ EPRI ＋ 各州社會採購申報。**每一份格式都不一樣。**
⚠️ 想找一篇量化「多少個資助方／多少小時」的澳洲研究，**沒找到**。
唯一主題吻合的學術文獻是 Misbauddin (2026)，`https://ojs.aut.ac.nz/rangahau-aranga/1/article/view/323`，
但樣本是**孟加拉 18 家社企、約 35 次訪談**，且僅取得摘要、無量化數字，
**不可當作澳洲證據引用**。

#### C. 2026-09 現在真的能申請的補助（給現場提案者的實用清單）

| 補助 | 金額 | 狀態（2026-09-21 查） |
|---|---|---|
| **SEDI Capability Building Grants 2026–27** | 每家最高 **12 萬澳幣** | ⭐ **2026-05-08 開放**，IIA 管理。用途明文含 **evaluation and impact measurement** |
| **SEDI First Nations Capability Building Grants** | **5–12 萬澳幣** | ⭐ **2026-07-22 開放**，滾動審查，預計開到 **2027 初** |
| **Commonwealth Outcomes Fund 第 2、3 輪** | 總額 1 億澳幣 | 州與領地於 **2026-05～2027-02** 提案；社企非直接申請人，須經州政府 |
| **WorkFoundations**（DEWR） | 方案 1,000 萬澳幣 | 16 家機構執行中，協議 2025-07 簽定 |
| **EPRI**（難民就業） | **2026-05 延長一年、770 萬澳幣** | 執行中 |
| **Westpac Foundation Inclusive Employment Grant** | **5 萬澳幣／2 年** | 專為「為複雜就業障礙者創造工作」的社企；**下一輪 2026 年開放** |
| **QLD Social Enterprise Jobs Fund** | 成長型 5,000–25,000；部門發展型 10,000–200,000 澳幣 | 需確認當期輪次 |
| **VIC 社企設備補助**（Business Victoria） | 購置廠房／機具／設備 | 社企模式須營運滿 12 個月 |
| 地方議會（如 Melbourne、Banyule、Parramatta） | 2,000 澳幣起 | 小額、門檻低 |

⚠️ 上表的州與地方項目僅由搜尋摘要取得，**開關狀態與當期金額需點進官網確認**，不要在 pitch 直接報。

#### D. 這一輪對方向 6 的淨影響

1. **不能再說「沒有人做格式對映」** —— 海外做了（廠商自述）。改說「**澳洲的格式沒有人做**」
2. **最強的產品鉤子變成 SEDI**：政府出錢（最高 12 萬澳幣）叫社企去買影響力衡量服務，
   而且**強制獲補助者建立 Impact Measurement Framework**。付費意願不需要論證，是寫在補助條款裡的
3. **demo 目標格式用 Social Traders 認證**（強制、週期性、格式穩定、有 200+ 資料點）
4. **一個立刻可用的產品約束**：DSS 的 AWP／AWPR 範本每欄建議 **300 字以內**
5. **唯一不可被複製的差異**：倫理紅線寫進程式。其餘兩條（澳洲格式、小組織價位）都只是時間問題

---

### 第四輪研究（2026-09-21 深夜）—— 「用 AI 幫填資料」這條線，有人做了

**觸發**：團隊把目標講成「用 AI 幫填資料」。第三輪盤的是「影響力衡量平台」，
**那是另一條產品線**，會漏掉整個 AI 表單自動填寫市場。本輪補上。

**⚠️ 結論先講**：如果我們把自己定位成「AI 幫填補助表單」，
**這一格是滿的，而且澳洲已經有一個、就長在澳洲撥款方在用的那個平台家族裡。**

#### A. 直接對打的產品

| 產品 | 做什麼 | 對我們的意義 |
|---|---|---|
| ⛔ **Drafter**（The Funding Centre，SmartyGrants 的姊妹單位，同屬 Our Community） https://www.smartygrants.com.au/articles/artificial-intelligence-powers-grant-writing-tool-for-nfps | **2025-10 上線，澳洲**。輸入組織／專案／目標補助的資料，**生成符合資助方指引與字數上限的草擬回答**，且**組織與專案資訊可在未來的申請中重複使用**。內嵌在 Funding Centre 平台（訂閱制） | **最危險的一個**。澳洲、在地、already shipped，而且和澳紐使用率最高的撥款系統 SmartyGrants 同一家。**他們握有通路** |
| **Grantyd** https://www.prnewswire.com/news-releases/grantyd-launches-as-first-ever-autofill-platform-for-grant-applications-302443629.html | **contextual autofill engine（專利申請中）**：瀏覽器外掛把線上入口的申請題目抓進平台 → AI 草擬 → **一鍵填回原本的申請表**。免費層／AI 層 **US$20 月**／協作層 **US$45 月** | 「AI 幫填表單」這件事**已經被做成產品並訂價了**，而且很便宜 |
| **Grantable** | 把 RFP 變成檢查清單，**從你的內容庫與過去得標的申請書**逐段草擬 | 同型 |
| **Loopio／Responsive（原 RFPIO）** | 企業級對照組：內容庫＋AI **自動回答最多約 80%** 的題目，同一套也做 DDQ 與資安問卷 | 證明這個模式在企業市場已經成熟十年 |
| **Instafill.ai／Happycapy** | 通用 AI 表單填寫。Instafill 有**澳洲商業表單與 ATO 表單**分類；Happycapy 用真實瀏覽器登入政府入口網站**填答並送出** | 連「登入政府網站幫你填」都有人做了 |

**可引用的工時數字（⚠️ 廠商來源，不是研究）**：
「average mid-sized grant takes **25–30 hours** to complete」，Grantyd 宣稱可減少最多 **60%**。
**這是我們目前唯一的申報工時數字**，但它出自廠商新聞稿，**引用時必須講明出處性質**。
（第三輪已確認：找不到任何澳洲研究量化過這件事。）

#### B. ⭐ 唯一還站得住的區分：**文字題 vs 數字題**

上述**每一個**產品填的都是**文字**：從內容庫、過去的申請書、組織文件裡，
把散文式的回答重複利用（"describe your project"、"what outcomes will you achieve"）。

**沒有任何一個宣稱：從營運紀錄算出一個數字，並附上算式與來源。**

> 「留任率 = 第 6 個月仍在職 14 人 ÷ 安置 22 人 = 64%，來源：出勤彙總，信心 0.9」
>
> 這一句，內容庫做不出來。去年的散文裡沒有今年的分母。

**這就是方向 6 剩下的那一格**，而且它剛好對上 WISE 的實際處境：
資助方要的是**安置數、留任率、工時**——全是數字，不是文字。

⚠️ **誠實的三個限制**：
1. **Sopact** 是唯一逼近的：自述會「clean IDs、code qualitative text、standardize reporting」
   並對映到資助方範本——那是資料側，比其他家更靠近數字。**但仍未查到它宣稱做推導與算式**
2. 我們**用「AI 從專案資料算出成效指標供申報」搜尋，沒找到任何產品**。
   ⚠️ **搜尋沒找到 ≠ 不存在**，不得宣稱「沒有人做」
3. 這一格很窄，**任何一家補上「算數字」都會蓋掉我們**。
   我們不靠這個站著（本場沒有新穎性評分），只用它來說明我們在哪一格

#### C. 對定位的直接影響（會改 pitch 的措辭）

**不要說**（這樣說等於自願跳進 Drafter 與 Grantyd 的格子）：
> "We use AI to help fill in grant applications."

**要說**：
> "We do not fill in the words. Tools already do that — Drafter in Australia,
> Grantyd in the US. We compute the numbers. Placements, retention, hours —
> derived from the records the enterprise already keeps, with the formula and the
> source shown beside every figure, and a refusal when the group is too small."

**被問到 Drafter 時的答法**：
> Drafter is good and it is Australian and it ships. It reuses organisational and
> project information across applications. That is the narrative half of the form.
> The other half is the table of numbers, and that half cannot be reused —
> the denominator changes every year.

**維持不變的硬性限制**
- **倫理紅線（原第 4 點）不因本判定而放寬**：只能做彙總，不得做個別受支持員工的評分、監控或能力推論
- **無公開員工層級資料**（本應如此）：demo 只能用合成或彙總資料，且必須明說是合成的
- **Outcomes Fund 的參數 2026 年初還在共同設計**——申報要求是移動中的標靶，
  不要把產品綁死在任何一組尚未定案的指標上

**判定**：本方向是方向 2 之外唯一通過的方向，且付費方證據比方向 2 更硬。
兩者的取捨在賽事當天決定，判準見第 7 節。

---

## 6. 評審四題壓測（選定方向後逐題回答，答不出就換題）

| 評審 | 他一定會問的那題 |
|---|---|
| James Hornitzky（Social Traders；PhD 做社企財務可持續性） | 誰付錢？賽後誰維護？這能變成交易收入還是只能靠補助？ |
| Ramana Kirubagaran（MultiLit CIO，主持 AI 治理委員會、跑過 AI 試點） | AI 答錯會怎樣？小機構維運得了嗎？ |
| Nandeeta Maharaj（Goods 4 Good 創辦人，實際營運者） | 我禮拜二早上真的會打開它嗎？ |
| Eva Sheluhina（ElevenLabs FDE，前 McKinsey） | 這是真的跑起來了，還是投影片？技術選擇有道理嗎？ |

**可引用的風險論證**：臨床語音轉文字錯誤率 7.4%、其中 5.7% 具臨床顯著性，
但**人工複核後降到 0.3%**（JAMA Network Open）→ 人審是設計的一部分，不是補丁。

**可引用的 viability 對照**：Ask Izzy 年營運約 500 萬澳幣（企業夥伴＋慈善基金會＋DSS 混合）；
Good Cycles 80/20（八成以上交易收入）；Social Traders 認證社企平均 86% 收入來自交易、68% 有淨利。

**語音（若使用）**：ElevenLabs Conversational AI 約 $0.08–0.10/分鐘，免費層 15 分鐘/月；
不需即時就用 **Scribe 批次**（更便宜、更準、無併發上限）。
500 通 × 5 分鐘 ≈ 每月 200–250 澳幣，對小型 NFP 是真實預算壓力 —— 主動講出來比被問出來好。

---

## 7. 現場優先原則

賽事 Day 1 **10:00 是問題陳述 pitch、10:30 組隊**。
若現場出現的真實問題能在 15 分鐘內填滿下列五欄，**一律優先於本檔的任何方向**：

1. 一個使用者、一個時刻、一個卡住的結果（一句話，不能有「而且」）
2. 證據（來源＋日期，能當場報出來）
3. AI 做的那件受限的事（抽取／比對／檢查，不是決定）
4. Demo 的黃金路徑（評審會看到的那一個畫面）
5. 誰付錢、誰維護

填不滿就用本檔的方向。

---

## 8. 方向 7 研究 —— 難民就業（2026-09-21 傍晚，三個 agent 平行）

**背景**：2026-09-21 傍晚，隊伍決定換題到「澳洲難民就業平台」。
本倉庫在此之前對 refugee／migrant／asylum／CALD **完全沒有任何研究**（grep 為零），
因此本節是該方向的第一輪、也是唯一一輪研究。

**方法**：三個 `general-purpose` agent 平行跑 WebSearch／WebFetch，
分為證據線、競品線、語音與評分對位線。

> ### ⚠️ 本節與第 5 節的證據等級不同
>
> 第 5 節的六個方向經過二到四輪研究與人工複驗。
> **本節只有一輪，且未經人工逐條複驗。**
> 上台前要念的每個數字必須自己打開原始 URL 確認。
> 「不要引用的數字」見 8.5，那一節比正文重要。

### 8.1 核心發現 —— 三份報告互相打架，而打架處就是答案

- **競品 agent** 的結論：履歷翻譯、jobright 式媒合、模擬面試三條車道全滿，
  唯一可守的是「無文件經歷 → ANZSCO／VET RPL 對映」。
- **語音 agent** 的結論：做非評分的語音面試練習室，
  因為 Usability 15% ＋ Prototype 15% ＋ Effective AI 15% = 45% 最好拿。
- **證據 agent** 挖到的同儕審查論文判了這場架：斷點在**雇主篩選時缺乏可信資訊**，
  所以面試練習室打不到斷點，而資歷對映打得到。

**合成結論（本輪最重要的一句）**：
**語音的正確位置是輸入端（口述採集），不是輸出端（朗讀）、也不是通話端（口譯）。**
因為求職者沒有文件、也打不出英文，**口述是唯一可能的輸入方式**——
所以語音是必要的，不是裝飾的。

### 8.2 證據線（agent 1）

⭐ **最強的一張牌 —— Guo & Tani, _British Journal of Industrial Relations_, 2026（UNSW）**
n=3,757（BNLA + HILDA）。難民抵澳時就業機率比其他移民低約 **88 個百分點**，
五年後仍低超過 **51 個百分點**。作者原話：

> *"the primary driver is discrimination by employers due to how they screen candidates
> when they lack reliable information about overseas qualifications or experience."*

https://www.unsw.edu.au/newsroom/news/2025/11/refugees-Australia-employer-discrimination
DOI https://doi.org/10.1111/bjir.70016

**其餘可引用數字**（完整清單與警語見 `docs/frameworks/direction-7-refugee-employment.md`）：

| 數字 | 來源 | 標籤 |
|---|---|---|
| 人道簽證領失業給付 **20.1%** vs 技術移民 **1.7%**（約 12 倍） | ABS Migrant Settlement Outcomes, PLIDA 2022–23 | OFFICIAL |
| 人道移民中位總所得 **$39,423**；抵澳未滿 5 年 **$25,183** | 同上 | OFFICIAL |
| 抵澳 3–6 個月 **6%** 有支薪工作 → 約 18 個月 **16%** → 約 2.5 年 **23%** | BNLA, AIFS/DSS, n=2,399 | EVIDENCE |
| BNLA 第 3 波性別差：男 **36%** vs 女 **8%**；第 10 年男 **63%** vs 女 **39%** | 同上 | EVIDENCE |
| **44%** 移民與難民從事低於技能水準的工作；年損 **90 億澳幣**、約 **44,000** 職位；**62 萬**「隱形勞動力」 | Deloitte Access Economics for SSI, 2024-06 | EVIDENCE |
| Career Pathways Pilot：**450 萬澳幣**、**784 人（目標 65%）**、**11–17%** 回到原職業、單人最高逾 **5,000 澳幣** | DSS/Deloitte 期中評估 | OFFICIAL/EVIDENCE |
| AMES FY2024-25：**17,951 客戶 → 1,533 成效 = 8.5%** | AMES 年報 | EVIDENCE |
| VETASSESS 完整評估 **$1,205.60 含 GST**，處理 **8–12 週** | VETASSESS 官網，2026-09 生效 | OFFICIAL |
| HSP：年逾 **1.2 億澳幣**、年逾 **17,000 客戶**、**5 供應商 11 合約區** | ANAO 績效稽核 | OFFICIAL |
| ⭐ **HISP 招標 2025-03-06 截標，結果預計 2026 年初** | Home Affairs | OFFICIAL |
| SETS：**205 筆補助**，2024-07-01 – 2027-06-30；**444 萬澳幣**滾存給 42 家供應商 | Home Affairs / ANAO | OFFICIAL |
| NSW RESP **已於 2024-06-30 結束**：5 年 **3,450 萬澳幣**、逾 **10,000 人**、近 **30%** 持續就業（全國基準 18 個月後 **17%**） | SSI / NSW | OFFICIAL/EVIDENCE |
| SSI FY25 營收 **2.1196 億澳幣**，年服務 **67,000+ 人** | SSI FY25 整合報告 | EVIDENCE |
| Thrive Refugee Enterprise：逾 **1,000 萬澳幣**放款給 550 家企業，年營收 **6,000 萬澳幣**；2017 年起支持 **1,500+** 名難民 | Thrive 影響報告 | EVIDENCE |

**摩擦點（Career Pathways Pilot 評估 §5.5.1，可直接引述原文）**：
文件拿不到、沒有澳洲推薦人、卡在初篩（雇主覺得 "more risky"）、
履歷協助為第三高需求（**42%**）、再認證六個月拖成三年、駕照與電腦是具體門檻。

**可整段講的案例**：阿富汗牙醫，6 年臨床 ＋ 7 年教學，
因拿不到母國一份政府文件而無法報考，同時因「沒有澳洲經驗」被牙助職缺拒絕，
最後只能無薪見習。

**雇主端阻礙**（Career Pathways Pilot ＋ Tent ＋ UNSW 三方交叉）：
初篩風險趨避、無法驗證海外資歷（Guo & Tani 指為**主因**）、
從人脈招募（難民沒有本地人脈）、本地經驗要求、小雇主職缺密度不足、
支援成本無法預估、沒有客製 onboarding 的經費。
另見 Lee, Szkudlarek, Johnson & Brewster, _Human Relations_, 2026（39 家澳洲雇主質性研究）
https://journals.sagepub.com/doi/10.1177/00187267251363341

### 8.3 競品線（agent 2）

**車道盤點結論**：

| 車道 | 狀態 | 關鍵佔位者 |
|---|---|---|
| A. 難民專用求職平台（境外技術通道） | **佔滿** | Talent Beyond Boundaries（15.5 萬人、開源、政府試辦）、Global Talent Pathway（澳洲自有、13.5 萬人、做資歷驗證）⚠️ 最接近的澳洲對手 |
| A'. 澳洲境內消費端 | **空著，但養不活** | ⛔ **Refugee Talent 已死** —— agent 直接 fetch `refugeetalent.com`，HTTP 200 但標題是印尼賭博網站，網域過期被接管 |
| B. AI 履歷翻譯／重排 | **完全佔滿，而且免費** | Kickresume、AIApply **免費**十秒翻譯；⛔ **Home Affairs Free Translating Service 免費翻 10 份官方文件**（含就業與教育文件，簽證後兩年內） |
| B'. 無文件資歷對映 | ⭐ **唯一薄的一格** | **SkillLab**（ESCO 13,485 技能→2,942 職業，明文處理 informal learning，**不在澳洲**）；**EQPR**（歐洲，靠 45–60 分鐘真人訪談）；**WES Gateway**（只有美加）；**Upwardly Global**（只有美國） |
| C. jobright 式媒合 | **佔滿且競爭激烈** | Jobright（**美國限定**，US$19.99–39.99/月，被抱怨 resume AI 幻覺）、Simplify、LazyApply、AIApply、Careerflow。**Sonara 已死過一次**（2024-02 倒閉，2026 換東家重開） |
| C'. 澳紐本地 | **有人佔住** | **JobSparrow**（AU/NZ，AI 履歷＋模擬面試＋媒合分數，**明文鎖定 migrants**，落地才付費） |
| D. AI 模擬面試／語音 | **佔滿，且地基本身是商品** | Yoodli（$8/月）、Huru（$99/年）、Final Round AI；⛔ **Google Interview Warmup 已於 2026-04 關閉**；**ElevenLabs Agents 本身就賣整套語音堆疊 $0.08–0.12/分鐘** |
| E. 澳洲安置部門就業媒合服務 | **塞滿了人** | 30+ 家政府資助機構，每州都有；**AMES 官網直接寫「free employment matching service」**；SSI、Brotherhood of St Laurence、CareerSeekers |

**⭐ Upwardly Global 的自我實測（本輪最有用的單一引用）**：
該組織公布自家 AI 工具對移民與難民申請者的辨識錯誤率——
**教育資歷 35% 被誤判、工作經歷 20% 被誤判**。其 CEO 原話大意：
AI 目前無法把一個人在外國取得的技能拆解出來、對映到本地勞動市場。
https://www.upwardlyglobal.org/news/new-report-examines-impact-of-ai-technologies-on-immigrant-and-refugee-workforce/

**這一條同時證明問題真實、且天真做法會失敗。**

**為什麼澳洲這一格搬不過來（護城河論證）**：
ANZSCO、VET RPL、ASQA、Country Education Profiles、TRA／VETASSESS／ACS 的分工
全是澳洲專有制度。SkillLab 的 ESCO 對映不能移植——**這正是 SkillLab 不在澳洲的原因**。

**誠實警語（agent 自陳）**：Workeer、Migracode、Amala、Talent Lift、Hire Immigrants、
LinkedIn Welcome Talent、Refugee Jobs Marketplace **本輪未取得現行第一手資料**，
不得宣稱其已死。Divtal 的網域無法解析，狀態未確認。

### 8.4 語音與評分對位線（agent 3）

**ElevenLabs 實際能力（EVIDENCE，官方文件）**：

| 能力 | 覆蓋 |
|---|---|
| Eleven v3 / v3 Conversational（約 280ms） | 70+ 語言 |
| Flash v2.5（約 75ms） | 32 語言 |
| Agents「All」設定 | **31 語言**；⛔ **語言偵測只在通話開始執行，無法中途切換** |
| Scribe v2 STT（90+ 語言） | 阿拉伯語 WER **10–20%**「Good」；波斯語／史瓦希里語 **5–10%**「High」；**普什圖語 25–50%**「Moderate」 |
| ⛔ **不在清單** | **Dari、Tigrinya、Rohingya、Hazaragi** |

https://elevenlabs.io/docs/overview/capabilities/speech-to-text
https://elevenlabs.io/docs/help-center/product/eleven-agents/which-languages-can-i-use-with-eleven-agents

**⭐ 承重的不對稱（INFERENCE）**：能聽約 90 種，能說約 31 種，
而**最需要的幾個語言剛好都缺**。任何以「說使用者的語言」為核心價值的功能，
對最需要它的族群結構性最弱。**自己先講。**

**TIS National 精確結論（OFFICIAL）**：免費口譯只對列舉式機構清單免費
（Medicare 私人執業醫療、藥局、**無大額政府資助的 NGO 個案／緊急服務**、房仲、
地方政府、工會、國會議員辦公室、特定 LGA 聯合健康）。
**雇主、職業介紹所、就業服務供應商與個別求職者不在清單上。**
https://www.tisnational.gov.au/en/Our-services/Free-Interpreting-Service/About

- **紅線（已確認）**：任何有後果的通話一律導去 TIS 131 450，我們不自稱口譯員。
- **INFERENCE，未驗證**：HSP 供應商年領 1.2 億澳幣，很可能不符合「無大額政府資助」。
  ⚠️ **上台前必須打開官網確認，不得直接宣稱。**

**九條倫理紅線**（含 AAAI-AIES 2024 的 85%、ANU 的 35% vs 22%、
PNAS 2020 的 WER 0.35 vs 0.19、Mobley v. Workday、EU AI Act Annex III、
NYC LL144、AHRC 技術報告、HRW 羅興亞案）：
完整表格與 URL 見 `docs/frameworks/direction-7-refugee-employment.md`「九條倫理紅線」一節。

**七項評分逐條對位**：同框架檔「評審七題的答法」一節。
最危險的一題是 **Problem–Solution Fit 20%**：
*「澳洲證據說壞的是雇主那端，你為什麼修求職者？」*
答案是 Guo & Tani 那句話——雇主壞在**缺可信資訊**。

### 8.5 ⛔ 不要引用的數字（本節最重要）

| 不要講 | 為什麼 |
|---|---|
| ABS **60.4%** 說成「就業率」 | 那是 PLIDA 的「有個人所得」比例。能講的是 **20.1% vs 1.7%** 的失業給付差距 |
| **CEDA 25% ／ 12.5 億澳幣** 套在難民身上 | 該報告只涵蓋**永久技術移民**，無難民數字 |
| **Woolworths 150 名難民** 當現況 | 那是 **2020 年**的數字；2026 年總數 NOT FOUND |
| **IKEA／Accor／Marriott／Compass** 為澳洲 Tent 成員 | **未驗證**，Tent 澳洲成員名單未公開 |
| 任何**競品價格** | 多來自 SEO 比較站，不要放簡報 |
| 人道入境者專屬**技能錯配百分比** | Deloitte 只說「更嚴重」，從未單獨量化。NOT FOUND |
| 「**沒有人做這件事**」 | 只能講「我們搜尋後沒有找到」 |
| 澳洲 AI 強制性規範「**是法律**」 | 截至 2026 年中仍未立法 |
| MDA Ltd／CareSeekers／Jesuit Refugee Service 規模 | 本輪未驗證 |
| TRA 費用 | 本輪未取得，只有 VETASSESS |

### 8.6 公開資料裡本來就不存在的三個缺口

**這三個是 NOT FOUND，不是沒查到。可以當論據用，不得自己估數字填補。**

1. **澳洲沒有任何官方來源可以說出「難民失業率是 X%」。**
   ABS Migrant Settlement Outcomes 只有所得與給付代理指標；
   ABS Characteristics of Recent Migrants 最新版停在 **2019-11** 且不分離人道簽證；
   BNLA 是唯一真正的就業序列，最後一波 2023。
2. **Workforce Australia 不公布依人道簽證身分分項的成效。**
   RESP 於 2024-06-30 結束後，NSW 難民在主流系統中的表現公開不可測。
   唯一對照點是已消失的 RESP 近 30% vs 全國 18 個月 17%。
3. **沒有公開數字說明難民走完海外資歷認證的成本、時間或放棄率。**
   VETASSESS 有費用（$1,205.60）與名目時程（8–12 週），
   但沒有人公布有多少人道入境者開始、完成、或在文件拿不到時放棄。
   現有證據全是軼事（阿富汗牙醫；六個月拖成三年的再認證）。

> **INFERENCE，可以上台講**：管不了沒被量的東西。
> 這三個缺口本身解釋了為什麼供應商申報的是活動量而不是成效。
