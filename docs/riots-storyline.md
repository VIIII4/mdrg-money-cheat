# MDRG 剧情调研：Riots（城市暴动）事件全解

> 数据来源：APK Addressables `Story_en` 本地化表 + `Story Shared Data` key 表（v0.97.11）。
> 本文只收录结构与少量短引用用于说明；完整原文提取在本地 `church_story_en.md` / `story_en.json`（版权原因不入库）。

## 一句话概括

**Riots 是主线中后期爆发的全城暴动事件**：抗议演变成打砸抢烧，Anon 被打晕在医院躺了两天，醒来后城市面目全非。事件持续数日，波及所有可访问地点，并与教堂支线深度联动（夜间救援 Priestbot 的名场面）。暴动结束后世界永久改变，各地点进入 AfterRiots 状态。

## 事件时间线

```
RiotsStart          暴动之夜：Anon 被暴徒围殴 → 医院昏迷 2 天
   │                （醒来得知：抗议起因众说纷纭，城市已成人间炼狱）
   ▼
暴动持续期（数天，可自由外出探索，全部危险）
   ├─ Outside/WalkRiots        夜间散步（ bottles fly，反思人群之恶）
   ├─ Outside/Clothier/Riots   Annalie 的服装店被砸光，她当场痛哭
   ├─ Outside/Dispenser/Riots  面包分发机被毁——穷人断粮
   ├─ Outside/Pharmacy/Riots   药店被抢空，药瘾者堵门哀嚎
   ├─ Outside/Labour Office…   劳务所停摆/复工后时薪暴跌到 20$
   ├─ Outside/Bigdaddystoryline×Riots  Big Daddy 电话永远忙线（在处理事态）
   ├─ Church/AfterStory/Riots1 白天探望教堂：Shanice 拿扫帚守门，
   │                           Priestbot 带梵蒂冈武器出门追打暴徒
   └─ Outside/Riots/ChurchRiots2  ★夜间救援（见下）
   ▼
Riots3              第三天：Priestbot 平安；暴徒迷信"亵渎教堂不吉利"，教堂无损
RiotsGeneric        暴动尾期的日常探望
   ▼
AfterRiots*         暴动结束（官方宣布"已控制"），世界进入永久恢复期
```

## 开场：RiotsStart（140 行，Outside/RiotsStart_*）

- Anon 街头被十几个人围殴，醒来已在医院："You were quite lucky. Only a few bruises and a concussion."
- 医院人满为患，住两天就被赶（还照样收费），出门被抗议老人抓住手臂宣讲 50 年最糟通胀
- 逃亡路上目睹商店、ATM、面包机被毁，空气里全是焦糊味
- 世界观细节：**大公司有自动炮塔毫发无损，小店全遭殃；警察只保护"白金订阅"区域**

## 起因之谜（游戏刻意留白的三种说法）

| 说法 | 出处 |
|------|------|
| 通胀/政府搞砸生活，50 年最糟 | 医院抗议老人 |
| 生活成本并无剧变，是民怨积到沸点 | 家里 bot 的统计分析 |
| "预测人类行为最简单的方法就是控制它"——**可能有人策划** | bot 的暗示；Bang News 也报道"市长或多或少造成了暴动" |

## ★ 核心玩法段：夜间救援 Priestbot（Outside/Riots/ChurchRiots2_*，146 行）

教堂线在暴动期的高潮，子场景按 `_N` 顺序：

| 场景 | 内容 |
|------|------|
| `_0` (28行) | 夜间散步撞见名场面：**Priestbot 被倒插在垃圾桶里**被围殴取乐。Anon 决定救人，想到附近认识一个 hobo |
| `_2`→`_4` | 去 hobo 地盘找他（更危险的城区，藏满法外之徒） |
| `_6` (15行) | 讨价还价：hobo 不肯丢下哄抢的物资，Anon 提醒"上次谁帮的你？"并掏钱，hobo 勉强出山 |
| `_11`→`_13` | 侦察：暴徒十几人围着垃圾桶，商量"挑衅调虎离山"计划 |
| `_15` (43行) | 行动：hobo 跳脸骂"你们都是懦夫"引来追击→Anon 接应也被追→被钢管围住以为要完→**Priestbot 自行挣脱电击救人**（"ZZzapp!"） |
| `_18`/`_20` | 战后：Priestbot 表示自己"随时能启动致命武器系统，只是文件工作太多"；hobo 拿钱骂骂咧咧走人（"早知道是破机器人我就不来了"） |
| `_23` | Priestbot 感谢后急着回去守教堂，Shanice 还一个人在那 |
| `_26`→`_30` | 收尾感想；hobo 仇视 bot 的伏笔（Stage3 还有 `churchHoboBots2` 后续） |

## 暴动结束后的世界（AfterRiots）

- `Outside/AfterRiotsNotice`：政府宣布控制局势，烟散了，但"这座城市已经不是原来那座"
- `Outside/AfterRiotsWithBot`：第一次敢带 bot 出门，bot 伤感悼念"我们初识的城市消失了"
- `RE/Rent/FirstAfterRiots`：房东不仅要房租，还让 Anon 签损失报告，连帮工清洁费都赖账
- `Shop/AfterRiots`：商店陆续恢复

## 教堂线的三个暴动结局变体（Church/AfterStory/AfterRiots*）

暴动期间对教堂的参与度决定后续对话版本：

| 场景 | 条件（推断） | 内容 |
|------|--------------|------|
| `AfterRiotsSavedPriestbot` | 参与了夜间救援 | Priestbot 送自制梵蒂冈待批 T 恤答谢；Shanice 恢复修理服务 |
| `AfterRiotsDidntSavePriestbot` | 去了但没救成 | Priestbot 被暴徒涂鸦+刮花的糗事被 Shanice 大嘴巴抖出，当场社死 |
| `AfterRiotsNeverWent` | 完全没参与 | Shanice 独自挨打住院；Anon 反省"朋友就该去探望" |

## 与其他系统的关联

- **Stage3**：主线第三阶段场景包含 `churchHoboBots2`、`nunBack` —— 暴动/教堂线后续融入后期主线
- **NunInvestigation2**（教堂凶案调查，见 church_analysis.md）中 hobo 疑似前刑警的设定，与救援段结识的 hobo 呼应
- **Big Daddy**：暴动期永远"很忙"，暗示其在幕后维持秩序
- **存档字段**：save 中 `flags` 无 riot 标记（条件存于代码而非文本表）

## 数据附录

暴动相关文本分布（映射 key 计）：

| 位置 | 行数 |
|------|------|
| Outside/*（含 Riots 子章、各地点 Riots 变体） | 741 |
| Church/AfterStory/*（Riots1/3/Generic + AfterRiots 三变体） | 148 |
| Labour Office/Riots | 41 |
| RE/Rent（FirstAfterRiots） | 26 |
| Shop/Riots + AfterRiots | 15 |

关键场景全文见本地文件 `church_story_en.md`（AfterStory 分节）与 `story_en.json`。
