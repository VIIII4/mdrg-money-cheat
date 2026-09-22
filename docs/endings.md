# MDRG 结局大全（v0.97.11）

> 数据来源：`Story_en`/`Other_en`/`UI_en` 本地化表。游戏内置结局画廊 UI 文案：
> *"You have seen {0} out of {1} main endings."* / *"...good main endings."* / *"...bad main endings."* / *"...church storyline endings."*
> 结局名单直接取自 `Other_en` 表的画廊条目（原文照录）。

## 结局体系总览

```
├── 主线结局 Main Endings（画廊分 Good / Bad 两组）
│   ├── Good ×3 —— Paradisium 岛屿结局三变体
│   └── Bad  ×10+ —— 各种死亡/被抓/坏旅行
├── 教堂支线结局 Church Endings ×5（官方明确标注）
└── Melissa 结局 ×4（画廊占位名 "Melissa ending 1-4"）
```

---

## 一、主线 Good Endings：Paradisium 三变体

**触发路径**：主线后期（Stage3）攒够钱后萌生退意 → `Outside/IslandPrologue1~4`（准备篇：办假身份/机场/告别，含 M/F bot 变体）→ `Ending/Island_*`（155 行：起飞、俯瞰城市、向家人坦白 bot 身份、落地）。

Anon 带着(bot)用"hard earned money"买的新身份飞往 **Paradisium**（世外桃源岛）。终章原文以自白收束：

> "It all began when a military truck was speeding down the street next to Mr. Landlord's apartment complex…"
> **"You've reached one of the good ends."**

三个变体（= 随行/送行的人不同）：

| 画廊名 | 内容 |
|--------|------|
| `Paradisium... with Annalie` | 服装店 Annalie 一起走（`Ending/AnnalieESL9`：她答应 "Yes. Let's go to Paradisium."）|
| `Paradisium... with Landlord` | 房东同行（`Ending/LandlordESL7`：受伤的他豁达告别 "It's time for us to leave."）|
| `Paradisium... with Everyone` | 大团圆版（跑道上还有 cameo 成就：landlord / Shanice / fisher 逐个现身）|

**遗憾线**：无论哪版，Melissa 相关的结局文本只有一句——
> "I wish Melissa was with us, but it was not to be. I wasn't able to help her…"

**结局后**：`Ending/AfterGoodEndingContinue` 是打破第四面墙的收尾：
> "Anon's story might not be over yet, but that's all that's to be seen in this path, in this game."

玩家可选择 "pretend this was a dream" 进入官方明说的 **endless mode**（游戏自己承认剧情会不一致）。

---

## 二、主线 Bad Endings（死亡/失败画廊）

| 画廊名 | 推断内容 |
|--------|----------|
| `Revenge of the homeless` | 流浪汉复仇·登机前夜：`Ending/RevengeOfTheHobos` 全场景——钓鱼决斗羞辱过的 hobo 破门行凶，Anon 失血而死，bot 哭喊 "Anon?! Stay with me, please!" |
| `Revenge of the homeless before the flight` | 同上·机场版（逃跑当天被堵）|
| `Unlucky encounter with lead` | 吃铅弹（枪杀）|
| `Victim of a revolution` | 死于城市暴动 |
| `Absolutely Butchered` | 被剁（街头暴力）|
| `Got caught...` | bot 被当局查获（sexbot 非法世界观）|
| `I'm not crazy...` | 精神值崩溃线（对应存档 `_mentalHealth`）|
| `Wall-kun` | 彩蛋结局（名字致敬"君"式命名梗）|
| `Imaginary Sea` | 官方描述：**"The sea you visit when you smoke the fish joint."** —— 抽了 Fisher 那根"鱼卷"后的幻觉结局 |
| `Very bad trip` | 坏旅行 |
| `Bad trip saved by Melissa` | 坏旅行·Melissa 救场版 |

死亡卡片通用文案（`Other_en`）：
> "It wasn't supposed to end like this…"
> "At least, to the end, we were friends…"

**机制提示**（UI 原文）：`"Warning! You're reaching max capacity! Going overboard will cause a bad ending!"` —— 存档 `_maxCum` 溢出也会进坏结局。

---

## 三、教堂支线结局 ×5（官方标注 "Ending no. X out of 5"）

| # | 官方名 | 一句话 |
|---|--------|--------|
| 1 | The not good enough ending | 蓝屏后再没回去，遗憾告别 |
| 2 | The happy ending | 救活 Priestbot（bot +10）|
| 3 | The true ending | Priestbot 坦然接受教会报废令，Anon 目送 |
| 4 | The worst ending | Shanice 遇害（念珠珠子+漂白剂+血）|
| 5 | The oblivious ending | 浑然不觉地离开 |

重置提示（UI 原文）：*"Church storyline has been reset! Go to church and explore all the endings!"*

详见 `docs/church-storyline.md`。

---

## 四、Melissa 结局 ×4

画廊占位名 `Melissa ending 1`~`4`（开发者尚未命名），对应 Melissa（超市收银员 bot）支线的四种终局；与 `Shop/Melissa4Rejection` 等场景和主线 Paradisium 的 "I wasn't able to help her" 遗憾文本呼应。

---

## 附：数据定位备忘

- 结局画廊名单：`Other_en` 表条目 [360]-[404] 区段（成就与结局名混排）
- 教堂结局标记：`Story_en` 中 "Church side story. Ending no. X out of 5"（共 5 条 + 孤儿副本 5 条）
- 岛屿结局正文：`Ending/Island_*`（14 个子场景）+ `Outside/IslandPrologue1~4`
- UI 计数文案：`UI_en`（Main/Good/Bad/Church 四种进度句式）
- 彩蛋：`Other_en` [375]-[380] 的 Jun001 原型机报告 = bot 身世伏笔（"The prototype did something today. Something that would exclude me and it from society forever…"）
