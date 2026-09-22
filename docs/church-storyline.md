# MDRG 教堂支线（Church Storyline）分析

> 提取自 `Story_en` 本地化表 + `Story Shared Data` key 表（APK: Unity Addressables）。
> 场景名为开发者原稿（波兰语），正文全部为英文。

## 剧情主线

1. **Monolog przed kosciolem**（教堂前独白）— Anon 出于怀旧走进贫民区的旧教堂
2. **Spotyka zakonnice**（遇见修女）— 遇到假扮修女的少女 **Shanice**
3. **There is no real priest nearby?** — 教堂里并没有真神父，只有一台老式神父机器人 **Priestbot / Ecclesiasticalot FF**（官方设定"Pius 设计失败品"）
4. **Spotkanie bota core / 2 pojscie do kosciola**（第二次去教堂）— 得知 Priestbot 的数据库损坏，且教会即将对它执行"清档/报废"（John Paul 202 的指令）
5. **大分支**：`Help them!` ↔ `Fuck them!(not literally)`
   - **Fuck them**（袖手旁观）→ 短线结束，Anon 自我安慰后离开
   - **Help them**（帮忙）→ 需要用自己的性爱机器人提取源码/数据救 Priestbot
6. **Spotkanie 2B / 2C** — 修理计划；Anon 问 Priestbot"对新教皇怎么看"时机器人过载蓝屏死机
7. **She needs to face the reality / I should cheer her up** — Shanice 崩溃，Anon 安慰
8. **Revival**（复活）— 修好后计划"教育朝圣"去梵蒂冈，但 Priestbot 坦白：教会指令不可违抗，自己终究要被报废
9. **THE WORST END 线** — 深夜回教堂发现 Shanice 失踪、长椅间散落她的念珠珠子、漂白剂与血腥味……（遇害暗示）
10. **AfterStory**（后日谈，任意结局后）— Riots 暴动线（救/不救 Priestbot / 从未参与三种）、NunBack 2-5、NunInvestigation2、BigDaddy 故事线、Melissa4church、GokusMotivation（梵蒂冈机甲大战）

## 五个结局（游戏原文标记 "Ending no. X out of 5"）

| # | 名称 | 场景 | 触发/内容 |
|---|------|------|-----------|
| 1 | **the not good enough ending** | `Just go there already!_7` | 蓝屏后再没回去，连 Shanice 住哪都不知道，只能自我告别的遗憾结局 |
| 2 | **the happy ending** | `Just go there already! bot +10_6` | 成功修复/救下 Priestbot 的圆满结局（bot 好感 +10） |
| 3 | **the true ending** | `Revival` 尾声（孤儿条目区） | Priestbot 拒绝逃跑："它是教会的财产，违抗指令没有意义"。Shanice 恳求无果离开，Anon 默然目送它接受报废 —— 官方"真结局" |
| 4 | **the worst ending** | `THE WORST END_19` | Anon 自保放弃所有人后重返教堂：血迹、漂白剂、Shanice 的念珠珠子、陌生男人…… Shanice 遇害，Anon 仓皇逃跑并永远逃离这一切 |
| 5 | **the oblivious ending** | `Spotkanie 2B_9` | Anon 对一切浑然不觉地离开："这不是应该发生的，但我大概再也不会来教堂了" |

## 数据统计

- 教堂章节文本：**1821 个映射 key**（+243 条未映射续行），共 ~2000+ 行对话
- 场景数：约 90 个（含 AfterStory 后日谈 26 个）
- 变体：`NC`（默认无性别分支）、`M`/`F`（机器人性别变体）
- 后缀 `bot +10` 等场景名内嵌好感度奖励

## 提取方法（备忘）

1. APK `assets/aa/Android/*.bundle`（UnityFS，LZ4）→ UnityPy 1.10.18（vendor 源码 + stub texture2ddecoder/etcpak + pkg python-brotli + uv lz4）
2. `a418819a…bundle` → `Story_en`（2.6MB，26238 条 `[i64 id][u32 len][utf8][pad4][i32 metaCount][meta…]`）
3. `46c9415…bundle` → `Story Shared Data`（3.5MB，17524 个 key，key 后 96 字节窗口内匹配 id）
4. `Church/*` key 过滤 + 场景分组排序 + 孤儿条目按文件顺序收养

## 文件

- `church_story_en.md` — 按场景分组的英文全文（推荐阅读）
- `church_raw.json` — key → 原始文本
- `story_en.json` / `key2id.json` — 全表数据与映射
