"""Builds assets/strokes/ja_kana.json from KanjiVG SVG files.

KanjiVG (c) Ulrich Apel, CC BY-SA 3.0, http://kanjivg.tagaini.net
Download the kana files (kanji/<5-hex-digit codepoint>.svg) into a folder, then:

    python3 -I tool/gen_strokes.py <folder with the svg files>

Each stroke becomes a list of [x, y] points on KanjiVG's 109 x 109 grid, in
writing order, so the app needs no SVG path parser.
"""
import json, os, re, sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
DECKS = os.path.join(HERE, '..', 'assets', 'decks')
OUT = os.path.join(HERE, '..', 'assets', 'strokes', 'ja_kana.json')
SAMPLES = 8
TOKEN = re.compile(r'([MmLlHhVvCcSsZz])|(-?\d*\.?\d+(?:e-?\d+)?)')

def bezier(p0, p1, p2, p3):
    pts = []
    for i in range(1, SAMPLES + 1):
        t = i / SAMPLES
        u = 1 - t
        pts.append((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
                    u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
    return pts

def flatten(d):
    tokens = [(m.group(1), m.group(2)) for m in TOKEN.finditer(d)]
    i = 0
    cmd = None
    cur = (0.0, 0.0)
    last_ctrl = None
    pts = []
    def num():
        nonlocal i
        v = float(tokens[i][1]); i += 1
        return v
    while i < len(tokens):
        if tokens[i][0]:
            cmd = tokens[i][0]; i += 1
            if cmd in 'Zz':
                continue
        rel = cmd.islower()
        c = cmd.upper()
        ox, oy = cur if rel else (0.0, 0.0)
        if c == 'M':
            cur = (ox + num(), oy + num()); pts.append(cur); last_ctrl = None
            cmd = 'l' if rel else 'L'
        elif c == 'L':
            cur = (ox + num(), oy + num()); pts.append(cur); last_ctrl = None
        elif c == 'H':
            cur = ((cur[0] if rel else 0) + num(), cur[1]); pts.append(cur); last_ctrl = None
        elif c == 'V':
            cur = (cur[0], (cur[1] if rel else 0) + num()); pts.append(cur); last_ctrl = None
        elif c == 'C':
            p1 = (ox + num(), oy + num()); p2 = (ox + num(), oy + num()); p3 = (ox + num(), oy + num())
            pts += bezier(cur, p1, p2, p3); cur = p3; last_ctrl = p2
        elif c == 'S':
            p1 = (2*cur[0] - last_ctrl[0], 2*cur[1] - last_ctrl[1]) if last_ctrl else cur
            p2 = (ox + num(), oy + num()); p3 = (ox + num(), oy + num())
            pts += bezier(cur, p1, p2, p3); cur = p3; last_ctrl = p2
        else:
            raise ValueError('unsupported path command ' + cmd)
    return [[round(x, 1), round(y, 1)] for x, y in pts]

def main(folder):
    chars = []
    for deck in ('ja_hiragana', 'ja_katakana'):
        with open(os.path.join(DECKS, deck + '.json'), encoding='utf-8') as f:
            chars += [c['front'] for c in json.load(f)['cards']]
    out = {}
    for ch in chars:
        path = os.path.join(folder, '%05x.svg' % ord(ch))
        root = ET.parse(path).getroot()
        strokes = []
        for el in root.iter('{http://www.w3.org/2000/svg}path'):
            m = re.search(r'-s(\d+)$', el.get('id', ''))
            if m:
                strokes.append((int(m.group(1)), flatten(el.get('d'))))
        strokes.sort(key=lambda s: s[0])
        assert [n for n, _ in strokes] == list(range(1, len(strokes) + 1)), ch
        out[ch] = [pts for _, pts in strokes]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump({'size': 109, 'chars': out}, f, ensure_ascii=False, separators=(',', ':'))
    print(len(out), 'characters,', sum(len(v) for v in out.values()), 'strokes')

if __name__ == '__main__':
    main(sys.argv[1])
