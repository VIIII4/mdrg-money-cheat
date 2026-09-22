#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-
"""MDRG 音乐提取器：bundle → FSB5 → ogg/wav"""
import UnityPy, os, sys
import fsb5

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLES = os.path.join(HERE, 'apk', 'assets', 'aa', 'Android')
OUT = os.path.join(HERE, 'music')
os.makedirs(OUT, exist_ok=True)

def bundle_infos():
    import glob
    for p in sorted(glob.glob(os.path.join(BUNDLES, '*.bundle'))):
        try:
            env = UnityPy.load(p)
        except Exception:
            continue
        name, res = None, None
        for o in env.objects:
            if o.type.name == 'AudioClip':
                raw = bytes(o.get_raw_data())
                if len(raw) > 8:
                    nlen = int.from_bytes(raw[0:4], 'little')
                    if 0 < nlen < 128:
                        try:
                            name = raw[4:4+nlen].decode('utf-8')
                        except UnicodeDecodeError:
                            pass
        if name is None:
            continue
        for fn, fobj in env.file.files.items():
            if fn.endswith('.resource'):
                res = fobj
        if res is not None:
            yield name, bytes(res.bytes)

def safe(n):
    return n.replace('/', '_').replace('\\', '_')

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    ok = fail = 0
    for name, fsb in bundle_infos():
        if only and only.lower() not in name.lower():
            continue
        if not fsb.startswith(b'FSB5'):
            print(f'[skip] {name}: 不是FSB5 ({fsb[:4]!r})')
            continue
        try:
            f = fsb5.load(fsb)
            mode = f.header.mode
            if mode == fsb5.SoundFormat.VORBIS:
                ext = 'ogg'
            elif mode == fsb5.SoundFormat.MPEG:
                ext = 'mp3'
            elif mode.is_pcm:
                ext = 'wav'
            else:
                ext = 'raw'
            for sample in f.samples:
                rebuilt = f.rebuild_sample(sample)
                out = os.path.join(OUT, safe(name) + '.' + ext)
                with open(out, 'wb') as fh:
                    fh.write(rebuilt)
                print(f'[ok] {name} -> {os.path.basename(out)} ({len(rebuilt):,}B, {mode.name})')
                ok += 1
                break  # 每首单轨，取第一个
        except Exception as e:
            print(f'[FAIL] {name}: {e}')
            fail += 1
    print(f'\n完成: ok={ok} fail={fail} -> {OUT}')

if __name__ == '__main__':
    main()
