# MDRG Money Cheat / 存档资金修改器

[English](#english) | [中文](#中文)

单文件 Python 脚本，用于修改 Android 版 *My Dystopian Robot Girlfriend*（MDRG）存档中主人公的资金（及赌场代币）。

## 中文

### 原理

MDRG 的存档位于：

```
/sdcard/Android/data/com.IncontinentCell.MyDystopianRobotGirlfriend/files/Saves/
```

- 存档槽为 `M1.mdrgslot`、`M2.mdrgslot`…（M=手动槽），`save.mdrg` 为全局进度
- 格式为**紧凑 JSON，无加密、无校验和**
- 资金就是顶层 `money` 字段（整数），赌场代币为 `casinoTokens`

本脚本读取/修改该 JSON，并自动处理 Android 11+ 的 scoped storage 权限问题（通过 `su` 提权后原地写入，保留文件属主/权限/SELinux 标签）。

### 环境要求

- 已 root 的 Android 设备（`su` 可用）
- [Termux](https://termux.dev) + Python 3（`pkg install python`）
- Windows / 桌面版玩家不需要本脚本：存档就是普通 JSON 文件，直接用文本编辑器改 `money` 字段即可

### 用法

```bash
# 列出所有存档槽及资金（只读）
python3 mdrg_money.py

# 把所有存档资金改为 99999
python3 mdrg_money.py 99999

# 只改 M1 槽
python3 mdrg_money.py M1 99999

# 改资金 + 赌场代币
python3 mdrg_money.py M1 99999 -t 500
```

### 特性

- ✅ 单文件、零依赖（仅 Python 标准库）
- ✅ 自动 `su` 提权（Android 11+ 无法直接访问 `/sdcard/Android/data`）
- ✅ 每次修改前自动备份到 `./backups/`
- ✅ 原地写入（in-place），不破坏文件属主/权限/SELinux 上下文

### 注意

- 修改前请把游戏**退到主菜单或完全退出**，否则游戏退出时会把内存中的旧数值写回
- 游戏目录中有官方提示：该目录存档会被游戏轮换覆盖，重要进度请在游戏内导出

---

## English

A single-file Python script to edit the protagonist's money (and casino tokens) in *My Dystopian Robot Girlfriend* saves on Android.

### How it works

Saves live in `/sdcard/Android/data/com.IncontinentCell.MyDystopianRobotGirlfriend/files/Saves/` as **plain compact JSON** — no encryption, no checksums. Money is simply the top-level `money` integer field (casino tokens: `casinoTokens`).

Since Android 11 blocks direct access to `/sdcard/Android/data`, the script elevates itself via `su` and patches the file in place, preserving ownership/permissions/SELinux context.

### Requirements

- Rooted Android with `su`
- Termux + Python 3 (`pkg install python`)
- Desktop players don't need this — just open the save in a text editor and change `money`

### Usage

```bash
python3 mdrg_money.py            # list all slots (read-only)
python3 mdrg_money.py 99999      # set money for ALL slots
python3 mdrg_money.py M1 99999   # set money for slot M1 only
python3 mdrg_money.py M1 99999 -t 500  # also set casino tokens
```

### Notes

- Quit to the main menu (or close the game) before editing, or the game will overwrite your change on exit
- Auto-backup to `./backups/` before every modification

## Disclaimer

This is an unofficial fan tool for personal save editing. Not affiliated with the game's developer. Use at your own risk.

## License

[MIT](LICENSE)
