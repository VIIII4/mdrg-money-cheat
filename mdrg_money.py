#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-
"""
MDRG (My Dystopian Robot Girlfriend) 存档资金修改器
====================================================
用法（在 Termux 里运行，需要 root，脚本会自动通过 su 提权）：

  python3 mdrg_money.py                  # 列出所有存档槽及资金
  python3 mdrg_money.py 99999            # 把【所有】存档槽资金改为 99999
  python3 mdrg_money.py M1 99999         # 只改 M1 槽
  python3 mdrg_money.py M1 99999 -t 500  # 顺便把赌场代币也改成 500

说明：
  - 存档位置: /sdcard/Android/data/com.IncontinentCell.MyDystopianRobotGirlfriend/files/Saves/
  - 存档格式: 紧凑 JSON，无校验和，直接改 money 字段即可
  - 每次修改前自动备份到脚本同目录的 backups/ 下
  - 原地(in-place)写入，保留文件属主/权限/SELinux 标签
"""
import json
import os
import shutil
import sys
import time

SAVES_DIR = "/sdcard/Android/data/com.IncontinentCell.MyDystopianRobotGirlfriend/files/Saves"
PYBIN = "/data/data/com.termux/files/usr/bin/python3"
BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")


def relaunch_as_root():
    """以 root 重新执行自身（su -c 不继承 Termux PATH，用绝对路径）"""
    args = [PYBIN, os.path.abspath(__file__)] + sys.argv[1:]
    quoted = " ".join("'" + a.replace("'", "'\\''") + "'" for a in args)
    os.execvp("su", ["su", "-c", quoted])


def find_slots():
    """返回存档目录下所有 .mdrgslot 文件路径"""
    return sorted(
        os.path.join(SAVES_DIR, f)
        for f in os.listdir(SAVES_DIR)
        if f.endswith(".mdrgslot")
    )


def resolve_slot(name):
    """把 'M1' / 'M1.mdrgslot' / 完整路径 解析为实际路径"""
    if os.path.isfile(name):
        return name
    for suf in (".mdrgslot", ""):
        p = os.path.join(SAVES_DIR, name + suf)
        if os.path.isfile(p):
            return p
    sys.exit(f"[!] 找不到存档槽: {name}（可用槽: " +
             ", ".join(os.path.basename(s)[:-9] for s in find_slots()) + "）")


def show_slot(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    name = os.path.basename(path)
    print(f"  {name:18} 资金: {d.get('money', 0):>10} $   "
          f"代币: {d.get('casinoTokens', 0):>8}   "
          f"游戏时长: {d.get('time', 0):>6}s   版本: {d.get('gameVersion', '?')}")


def backup(path):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    dst = os.path.join(BACKUP_DIR, f"{os.path.basename(path)}.{ts}.bak")
    shutil.copy2(path, dst)
    # 备份文件归还给 Termux 用户，避免 root 占位
    st = os.stat(os.path.abspath(__file__))
    try:
        os.chown(dst, st.st_uid, st.st_gid)
    except PermissionError:
        pass
    return dst


def patch(path, money=None, tokens=None):
    with open(path, "rb") as f:
        raw = f.read()
    d = json.loads(raw)
    old_m, old_t = d.get("money"), d.get("casinoTokens")
    if money is not None:
        d["money"] = int(money)
    if tokens is not None:
        d["casinoTokens"] = int(tokens)
    if d.get("money") == old_m and d.get("casinoTokens") == old_t:
        print(f"[=] {os.path.basename(path)} 无变化 (money={old_m})，跳过写入")
        return
    bak = backup(path)
    # 原地写入：保留 inode → 属主/权限/SELinux 标签不变
    with open(path, "r+b") as f:
        f.write(json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        f.truncate()
    print(f"[+] {os.path.basename(path)}: 资金 {old_m} -> {d.get('money')}"
          + (f"，代币 {old_t} -> {d.get('casinoTokens')}" if tokens is not None else ""))
    print(f"    备份: {bak}")


def main():
    if os.geteuid() != 0:
        relaunch_as_root()  # 不再返回

    argv = sys.argv[1:]
    tokens = None
    if "-t" in argv or "--tokens" in argv:
        i = next(k for k in ("-t", "--tokens") if k in argv)
        idx = argv.index(i)
        tokens = argv[idx + 1]
        del argv[idx:idx + 2]

    if not argv:  # 列出所有槽
        slots = find_slots()
        if not slots:
            sys.exit(f"[!] 未找到任何 .mdrgslot 存档: {SAVES_DIR}")
        print(f"存档目录: {SAVES_DIR}")
        for s in slots:
            show_slot(s)
        return

    if argv[0].isdigit():          # 只有金额 → 改所有槽
        money, targets = argv[0], find_slots()
    else:                          # 指定槽
        if len(argv) < 2 or not argv[1].isdigit():
            sys.exit(__doc__)
        money, targets = argv[1], [resolve_slot(argv[0])]

    if not targets:
        sys.exit("[!] 没有可修改的存档")
    for t in targets:
        patch(t, money=money, tokens=tokens)


if __name__ == "__main__":
    main()
