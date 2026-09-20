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
- Social Traders 認證是**免費**的。

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
- Reddit 分數（Arctic Shift 多在貼文早期擷取，系統性低估）。
  例：r/nonprofit《Grant writing is just rewriting the same information 40 different ways》
  年度排名第 4，但抓取顯示 score=1 且已被版主移除。**引用排名，不要引用分數。**

### 4.5 需人工開啟驗證的 PDF（自動抓取皆 403 或無法解析）

- Social Traders Full Guidance Notes：`https://assets.socialtraders.com.au/downloads/Full-Guidance-Notes.pdf`
- CSI《State of the Social Economy in Australia》完整 PDF 的百分比細分
- 維州社會採購框架買方指引 FAQ／Big Build 申報頁
- Inclusion Australia／CSI《ADE Snapshot》

---

## 5. 五個要研究的方向

依優先序。每個都**必須**做競品盤點與付費方分析。

### 方向 1 — NDIS 文件編排 ⭐ 最高優先

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

---

### 方向 2 — 二手店捐贈物「路由」 ⭐

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
- 競爭壓力（訊號弱，僅 16 views，需再查）：X @bigbatnews 2026-09-03
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

---

### 方向 3 — 社企的「證據層」⭐

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

---

### 方向 4 — 租屋權益

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

---

### 方向 5 — 食品詐標／食物系統

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
