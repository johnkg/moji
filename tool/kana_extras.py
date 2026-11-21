"""Tables for the kana extras: voiced sounds, combined sounds, small tsu, long mark.

Shared by gen_decks.py and gen_lessons.py so decks and lessons cannot drift apart.
Hiragana is the source; katakana is the same characters shifted by 0x60.
"""

def to_kata(text):
    return ''.join(chr(ord(c) + 0x60) if 'ぁ' <= c <= 'ゖ' else c for c in text)

# Unit id -> (hiragana, romaji) in teaching order. The rare ぢ and づ are left out.
VOICED = [
 ("g", [("が", "ga"), ("ぎ", "gi"), ("ぐ", "gu"), ("げ", "ge"), ("ご", "go")]),
 ("z", [("ざ", "za"), ("じ", "ji"), ("ず", "zu"), ("ぜ", "ze"), ("ぞ", "zo")]),
 ("d", [("だ", "da"), ("で", "de"), ("ど", "do")]),
 ("b", [("ば", "ba"), ("び", "bi"), ("ぶ", "bu"), ("べ", "be"), ("ぼ", "bo")]),
 ("p", [("ぱ", "pa"), ("ぴ", "pi"), ("ぷ", "pu"), ("ぺ", "pe"), ("ぽ", "po")]),
]

# Combined sounds: a character plus a small や, ゆ or よ.
SMALL = [("ゃ", "a"), ("ゅ", "u"), ("ょ", "o")]
COMBO_UNITS = [
 ("c1", [("き", "ky"), ("ぎ", "gy")]),
 ("c2", [("し", "sh"), ("じ", "j")]),
 ("c3", [("ち", "ch"), ("に", "ny")]),
 ("c4", [("ひ", "hy"), ("み", "my")]),
 ("c5", [("り", "ry"), ("び", "by")]),
 ("c6", [("ぴ", "py")]),
]

def combo_rows(pairs):
    return [(base + small, stem + vowel) for base, stem in pairs for small, vowel in SMALL]

SMALL_TSU = ("っ", "xtsu", "small tsu", "a short pause: the next consonant is doubled")
LONG_MARK = ("ー", "choon", "long mark", "stretches the vowel before it")

def all_voiced():
    return [row for _, rows in VOICED for row in rows]

def all_combos():
    return [row for _, pairs in COMBO_UNITS for row in combo_rows(pairs)]
