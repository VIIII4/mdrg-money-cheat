#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-
"""
MDRG 本地化全量提取器
=====================
从 APK 的 Addressables bundle 中提取全部英文文本表 + SharedData key 映射，
输出到 extracted/ 目录：
  <Table>.json          —— {key: text}（含 __orphan__<id> 未映射条目，按文件顺序）
  <Table>.md            —— 按章节/场景分组的可读版
用法: PYTHONPATH=vendor/unitypy-1.10.18:vendor/stubs python3 extract_all.py
"""
import UnityPy, json, re, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'extracted')
BUNDLES = os.path.join(HERE, 'apk', 'assets', 'aa', 'Android')
EN_BUNDLE = os.path.join(BUNDLES, 'a418819a3ad0468b3d03402b45383142.bundle')
SHARED_BUNDLE = os.path.join(BUNDLES, '46c941530c6f45cd51b8e149487c8160.bundle')
EXTRA_BUNDLES = [
    ('UI_Assets_en', os.path.join(BUNDLES, '7817a2147444d61bf2770078e2bc57e8.bundle')),
    ('Moddable_en', os.path.join(BUNDLES, 'd2157188dbf7806617ae23d2086e8b8b.bundle')),
]

def monos(bundle):
    """yield (name, raw_bytes) 所有 MonoBehaviour"""
    env = UnityPy.load(bundle)
    for o in env.objects:
        if o.type.name == 'MonoBehaviour':
            raw = bytes(o.get_raw_data())
            if len(raw) < 36:
                continue
            nlen = int.from_bytes(raw[28:32], 'little')
            if 0 < nlen < 128:
                try:
                    yield raw[32:32+nlen].decode('utf-8'), raw
                except UnicodeDecodeError:
                    pass

def parse_string_table(raw, min_chain=2):
    """解析 StringTable: 常见 [count@72] + 条目 [id8][len4][utf8][pad4][i32 meta][meta...]
    兼容 Blog 型异构头: 先在全文引导扫描一条 ≥min_chain 的合法条目链"""
    n = len(raw)
    entries, p = [], None
    # 引导: 从 44 起找第一个能连续解析 min_chain 条的位置（链步进失败时尝试 +4 间隙）
    def try_chain(start, steps):
        tp, ok = start, 0
        for _ in range(steps):
            good = False
            for tp2 in (tp, (tp + 3) & ~3, ((tp + 3) & ~3) + 4):
                if tp2 + 12 > n:
                    continue
                ln = int.from_bytes(raw[tp2+8:tp2+12], 'little')
                if 0 <= ln and tp2 + 12 + ln <= n:
                    try:
                        raw[tp2+12:tp2+12+ln].decode('utf-8')
                        tp = tp2
                        good = True
                        break
                    except UnicodeDecodeError:
                        pass
            if not good:
                break
            tp = (tp + 12 + ln + 3) & ~3
            ok += 1
        return ok

    for start in range(44, min(400, n - 12), 4):
        if try_chain(start, min_chain) == min_chain:
            p = start
            break
    if p is None:
        return []
    while p + 12 <= n:
        ln = int.from_bytes(raw[p+8:p+12], 'little')
        if 0 <= ln and p + 12 + ln <= n:
            try:
                entries.append((raw[p:p+8], raw[p+12:p+12+ln].decode('utf-8')))
                q = (p + 12 + ln + 3) & ~3
            except UnicodeDecodeError:
                q = p + 1
        else:
            q = p + 1
        np_ = None
        for cand in range(q, min(q + 4096, n - 12)):
            cln = int.from_bytes(raw[cand+8:cand+12], 'little')
            if cand + 12 + cln <= n and cln >= 0:
                try:
                    raw[cand+12:cand+12+cln].decode('utf-8')
                    np_ = cand
                    break
                except UnicodeDecodeError:
                    continue
        if np_ is None:
            break
        p = np_
    seen, out = set(), []
    for idb, t in entries:
        if idb not in seen:
            seen.add(idb)
            out.append((idb, t))
    return out

def parse_shared_data(raw):
    """解析 SharedTableData: [u32 len][key ascii]（不强制含'/'，兼容 Items/UI 等命名风格）"""
    m2 = len(raw)
    keys = []
    i = 0
    while i < m2 - 8:
        ln = int.from_bytes(raw[i:i+4], 'little')
        if 3 <= ln <= 400 and i + 4 + ln + 24 < m2:
            s = raw[i+4:i+4+ln]
            if all(32 <= c < 127 for c in s):
                keys.append((i, i + 4 + ln, s.decode()))
                i += 4 + ln
                continue
        i += 1
    return keys

def build_key_map(shared_raw, idset):
    """key -> id（在 key 前后 128 字节窗口内找属于 idset 的 8 字节;
    兼容 [len][key][id]（Story）与 [id][len][key]（UI）两种布局）"""
    keys = parse_shared_data(shared_raw)
    key2id = {}
    m2 = len(shared_raw)
    for j, (pos, kend, key) in enumerate(keys):
        nxt = keys[j+1][0] if j + 1 < len(keys) else m2
        prv = keys[j-1][1] if j > 0 else 0
        seg_before = shared_raw[max(prv, pos - 128):pos]
        seg_after = shared_raw[kend:min(nxt, kend + 128)]
        for seg in (seg_after, seg_before):
            hit = None
            for k in range(0, max(0, len(seg) - 7)):
                w = seg[k:k+8]
                if w in idset:
                    hit = w.hex()
                    break
            if hit:
                key2id[key] = hit
                break
    return key2id

def natkey(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]

def table_md(name, key2text):
    """按章节/场景分组的 markdown"""
    out = [f'# {name} 全文（按章节/场景）\n', f'> 共 {len(key2text)} 条\n']
    groups = collections.defaultdict(list)
    orphan = []
    for k, t in key2text.items():
        if k.startswith('__orphan__'):
            orphan.append((k, t))
        else:
            groups['/'.join(k.split('/')[:-1]) if '/' in k else '(顶层)'].append((k, t))
    for g in sorted(groups, key=natkey):
        out.append(f'\n## {g}\n')
        for k, t in sorted(groups[g], key=lambda x: natkey(x[0])):
            scene = k.split('/')[-1]
            for seg in t.split('\n'):
                seg = seg.strip()
                if seg:
                    out.append(f'- **{scene}** {seg}' if len(groups[g]) > 1 else f'- {seg}')
        out.append('')
    if orphan:
        out.append(f'\n## 未映射条目（{len(orphan)} 条，游戏引用但无 key）\n')
        for k, t in orphan:
            for seg in t.split('\n'):
                seg = seg.strip()
                if seg:
                    out.append(f'- {seg}')
    return '\n'.join(out)

def main():
    os.makedirs(OUT, exist_ok=True)
    # 预载 SharedData bundle 的所有 shared 表
    shared = {}
    for nm, raw in monos(SHARED_BUNDLE):
        if nm.endswith('Shared Data'):
            shared[nm[:-12]] = raw
    # 主英文表
    tables = {nm: raw for nm, raw in monos(EN_BUNDLE) if nm.endswith('_en')}
    for nm, b in EXTRA_BUNDLES:
        for n2, raw in monos(b):
            if n2.endswith('_en'):
                tables[n2] = raw
    print(f'英文表 {len(tables)} 个, SharedData {len(shared)} 个')
    summary = []
    for name in sorted(tables):
        base = name[:-3]
        entries = parse_string_table(tables[name])
        idset = {e[0] for e in entries}
        id2text = {e[0].hex(): e[1] for e in entries}
        key2text = {}
        if base in shared:
            key2id = build_key_map(shared[base], idset)
            used = set()
            for key, idh in key2id.items():
                key2text[key] = id2text[idh]
                used.add(idh)
            for idh, t in id2text.items():
                if idh not in used:
                    key2text[f'__orphan__{idh}'] = t
            mapped = len(key2id)
        else:
            for idh, t in id2text.items():
                key2text[f'__orphan__{idh}'] = t
            mapped = 0
        json.dump(key2text, open(os.path.join(OUT, f'{name}.json'), 'w'),
                  ensure_ascii=False, indent=1)
        open(os.path.join(OUT, f'{name}.md'), 'w').write(table_md(name, key2text))
        summary.append((name, len(entries), mapped))
        print(f'  {name:18} 条目 {len(entries):6}  key映射 {mapped:6}')
    print('\n输出目录:', OUT)

if __name__ == '__main__':
    main()
