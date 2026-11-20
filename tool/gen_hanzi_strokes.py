"""Builds assets/strokes/zh_hanzi.json from hanzi-writer-data files.

Data: Make Me a Hanzi / hanzi-writer-data, extracted from Arphic Technology
fonts, Arphic Public License (see assets/strokes/ARPHICPL.TXT).
Download <char>.json for each character from
https://github.com/chanind/hanzi-writer-data (data/ folder) into a folder, then:

    python3 -I tool/gen_hanzi_strokes.py <folder>

Characters come from assets/decks/zh_hanzi.json and the Mandarin lessons.
We keep each stroke's median (centre line) and rescale it from the source's
1024 grid (y up, baseline at y=124 from the bottom) onto the 109 x 109 grid
used for kana, so the app treats both the same way.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')
OUT = os.path.join(ASSETS, 'strokes', 'zh_hanzi.json')
GRID = 109.0

def wanted():
    chars = []
    with open(os.path.join(ASSETS, 'decks', 'zh_hanzi.json'), encoding='utf-8') as f:
        chars += [c['front'] for c in json.load(f)['cards']]
    with open(os.path.join(ASSETS, 'lessons', 'zh_basics_course.json'), encoding='utf-8') as f:
        for unit in json.load(f)['units']:
            chars += [i['front'] for i in unit['items']]
    return sorted({c for c in chars if len(c) == 1 and ord(c) > 0x2E80})

def convert(point):
    x, y = point
    return [round(x / 1024 * GRID, 1), round((900 - y) / 1024 * GRID, 1)]

def main(folder):
    out = {}
    for ch in wanted():
        with open(os.path.join(folder, ch + '.json'), encoding='utf-8') as f:
            medians = json.load(f)['medians']
        out[ch] = [[convert(p) for p in stroke] for stroke in medians]
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump({'size': GRID, 'chars': out}, f, ensure_ascii=False, separators=(',', ':'))
    print(len(out), 'characters,', sum(len(v) for v in out.values()), 'strokes')

if __name__ == '__main__':
    main(sys.argv[1])
