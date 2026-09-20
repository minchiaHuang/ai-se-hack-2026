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
- 評分標準只有三項：**quality／impact reasoning／viability**

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
| **食品詐標／食物系統（方向 5）** | 2026-09-21 競品盤點：詐標端的缺口是鑑識檢測與執法權（Source Certain 實驗室、**ACCC 已於 2026-08-07 啟動調查**），不是軟體；食物救助端 Foodbank／OzHarvest／SecondBite 合計佔全澳 **80%+**，OzHarvest 免費配送覆蓋 1,500+ 機構，真瓶頸是供給、冷鏈經費與捐贈稅制；且同型澳洲社企 **Yume Food 已於 2024-11 進入自願管理並清算**。詳表見 §5 方向 5 末 |
| **租屋權益（方向 4）** | 2026-09-21 競品盤點：Justice Connect《Dear Landlord》免費自助工具（2020 年起逾 **10 萬**名維州租客使用，含 VCAT 準備）、Tenants' Union NSW《Rent Increase Negotiation Kit》內建 Letter Generator（可作仲裁庭佐證）、商業端有 Rent AI 與 Renters Rights AI；付費方已是法定基金且買的是「對租客免費」；**NSW 租客工會已公開警告 AI 做租務建議的風險**。詳表見 §5 方向 4 末 |
| **NDIS 文件編排（方向 1）** | 2026-09-21 競品盤點：免費端有 PlanMind（免註冊、含 ReAssess 書面陳述產生器）、Novida 範本庫、PWdWA＋Legal Aid WA 內部覆議工具包；付費端 MagMindLab 以 **$89** 販售幾乎等同的「證據對齊＋缺口檢查＋I-CANv6 草擬評分」；申訴階段另有聯邦 **NDIS Appeals Program** 免費倡議者與法律代理（2026–27 起再撥 1,470 萬澳幣）。詳表見 §5 方向 1 末 |
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
- NDIA 官方 I-CAN 公告（2026-09-21 自動抓取回 HTTP 403）：
  `https://www.ndis.gov.au/news/10927-new-tool-deliver-simpler-pathway-disability-supports`

---

### 4.6 競品可能是死的 —— 而死的競品是不利證據（2026-09-21 新增）

這一輪競品盤點意外撞到兩具屍體：

- **Amplify Social Impact Online**（方向 3）：CSI 1,200 萬澳幣專案的一部分，**免費**、學術驗證，
  因「lower than anticipated take-up」關閉
- **Yume Food Australia**（方向 5）：自我定位社會企業，十年重新分配 1,150 萬公斤食物、
  客戶含 Mars 與 Unilever，2024 年 11 月進入自願管理並清算

**教訓**：查競品時不能只查「有沒有人在做」，必須查「做的人還活著嗎、為什麼死的」。
而且——**發現競品已死不等於發現空缺**。在只有 quality／impact reasoning／**viability**
三項評分標準的場子，一個做得更大更有資源的前人倒了，是對 viability 的直接不利證據。
要用這種發現，唯一誠實的方式是正面回答「你憑什麼不一樣」，不是把它說成市場機會。

---

## 5. 六個要研究的方向

依優先序。每個都**必須**做競品盤點與付費方分析。
**2026-09-21 更新**：方向 1 **淘汰**；方向 2 **通過**（收窄為「店內進貨端分流」，目前領先）；
方向 3 **降級**（直接競品 Amplify 已因無人採用而關閉）。方向 4–6 尚未做競品盤點。

### 方向 1 — NDIS 文件編排 ✂️ **已於 2026-09-21 競品盤點後淘汰**（理由見本節末）

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
   **如果已有成熟或免費的產品，這條線當場清掉。**
2. 誰付錢？參與者現金吃緊。候選：support coordinator
   （留言中一位自稱 SSC 者說「I **desperately need an advocate** for 2 of my participants」）、
   plan manager、倡議組織、allied health 提供者、法律扶助。
3. 這算社會企業嗎（交易收入）還是慈善服務？
4. 倫理與法律邊界：協助編排**既有**證據 vs 生成主張；是否構成提供法律意見。
5. **政治風險**：X 上主流敘事是「NDIS 詐騙猖獗」（@bhavdip143「the biggest rort in Australia」
   1336 likes，已驗證）。「幫參與者贏申訴」會被部分人讀成「幫人鑽漏洞」。要準備答案。

**社群搜尋設計**：r/NDIS 改用 `sort=new`（找工具討論而非情緒宣洩）、r/AusLegal、r/disability；
X 追 @criprights 等倡議帳號在推薦什麼工具。

**競品盤點結果（2026-09-21 完成）→ 判定：✂️ 清掉，不要在賽事當天做這條線**

規則 4 的競品檢查已執行（純桌面研究，未聯絡任何人）。結論：這個問題空間同時被
**免費產品**、**已上市的付費產品**、以及**政府免費申訴代理**三層佔據。
依本方向自訂的判準（「如果已有成熟或免費的產品，這條線當場清掉」），**本方向淘汰**。

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

### 方向 2 — 二手店捐贈物「路由」 ⭐ **2026-09-21 競品盤點通過**（判定見本節末）

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

**競品盤點結果（2026-09-21 完成）→ 判定：✅ 通過，但必須收窄到「店內進貨端分流」**

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

### 方向 3 — 社企的「證據層」⚠️ **2026-09-21 競品盤點後降級**（判定見本節末）

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

**競品盤點結果（2026-09-21 完成）→ 判定：⚠️ 降級，除非付費方改成不是社企本身**

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

### 方向 4 — 租屋權益 ✂️ **2026-09-21 競品盤點後淘汰**（判定見本節末）

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

**競品盤點結果（2026-09-21 完成）→ 判定：✂️ 清掉**

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

**給下一位 agent**：不要重查本方向。若現場有住房領域提案者，上表可當「已被佔據的格子」清單使用。

---

### 方向 5 — 食品詐標／食物系統 ✂️ **2026-09-21 競品盤點後淘汰**（判定見本節末）

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

**競品盤點結果（2026-09-21 完成）→ 判定：✂️ 清掉（兩條支線都不通）**

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

**給下一位 agent**：不要重查本方向。若現場有食物系統提案者，把支線 B 的瓶頸清單
（供給、冷鏈經費、捐贈稅制）交給對方，那是真問題——但解法是政策與資金，不是我們兩天能做的軟體。

### 方向 6 — WISE 就業成效申報與 Outcomes Fund

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
