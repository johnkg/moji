"""Regenerates assets/lessons/*.json. Content is hand-written (no third-party data).

Each item may point at a flashcard with "card": "<deck id>:<card id>", so a
finished unit feeds the review decks.
"""
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'lessons')

def items(deck, rows):
    return [{"id": cid, "front": f, "reading": r, "meaning": m, "hint": h, "card": f"{deck}:{cid}"}
            for cid, f, r, m, h in rows]

def words(rows):
    return [{"text": t, "reading": r, "meaning": m} for t, r, m in rows]

hiragana = {
 "id": "ja_hiragana_course", "lang": "ja", "title": "Hiragana, step by step",
 "description": "Learn to read Japanese sounds, five characters at a time.",
 "units": [
  {"id": "vowels", "title": "The five vowels",
   "intro": [
    "Japanese is written with three scripts mixed together. Hiragana is the one to learn first. It has 46 characters.",
    "Each hiragana character is one sound. Unlike English letters, a character is always read the same way.",
    "Japanese has only five vowel sounds: a, i, u, e, o. Always in that order. Every other character is a consonant plus one of these five.",
    "How they sound: a = 'ah' as in father. i = 'ee' as in see. u = 'oo' as in food. e = 'eh' as in bed. o = 'oh' as in go. Keep each one short.",
    "The text under each character (like 'a') is romaji: Japanese sounds spelled with English letters. It is only a helper.",
   ],
   "items": items("ja_hiragana", [
    ("a", "あ", "a", "", "Sounds like 'ah'. Look for a capital A hiding in the middle: crossing strokes over a loop."),
    ("i", "い", "i", "", "Sounds like 'ee'. Two strokes side by side, like two eels swimming together."),
    ("u", "う", "u", "", "Sounds like 'oo'. A dash above a bent line, like someone hit in the belly going 'oof'."),
    ("e", "え", "e", "", "Sounds like 'eh'. A runner full of energy: a dash for the head, legs stretched out."),
    ("o", "お", "o", "", "Sounds like 'oh'. Close to あ, but with an extra dot on the right: 'oh, a dot!'"),
   ]),
   "words": words([("あい", "ai", "love"), ("いえ", "ie", "house"), ("うえ", "ue", "above"),
                   ("あおい", "aoi", "blue"), ("いいえ", "iie", "no")])},
  {"id": "k_row", "title": "The K row",
   "intro": [
    "Now put a k sound in front of each vowel: ka, ki, ku, ke, ko.",
    "Same vowel order as before: a, i, u, e, o. Every row in the hiragana chart follows it.",
    "After this unit you can read real words made of vowels and K sounds.",
   ],
   "items": items("ja_hiragana", [
    ("ka", "か", "ka", "", "A blade swinging down with a spark flying off: 'ka!' like a karate chop."),
    ("ki", "き", "ki", "", "Looks like an old key with two teeth on top."),
    ("ku", "く", "ku", "", "An open bird beak calling 'coo, coo'."),
    ("ke", "け", "ke", "", "A post on the left and a gate on the right. 'ke' as in 'kept': the gate is kept shut."),
    ("ko", "こ", "ko", "", "Two short curved lines, like two koi fish swimming."),
   ]),
   "words": words([("かお", "kao", "face"), ("あか", "aka", "red"), ("えき", "eki", "station"),
                   ("いけ", "ike", "pond"), ("ここ", "koko", "here"), ("きく", "kiku", "to listen")])},
  {"id": "s_row", "title": "The S row",
   "intro": [
    "The S row: sa, shi, su, se, so.",
    "One surprise: the second one is 'shi', not 'si'. Japanese has no 'si' sound.",
    "さ looks a lot like き from the last unit. さ has one bar, き has two.",
   ],
   "items": items("ja_hiragana", [
    ("sa", "さ", "sa", "", "Like き with only one bar. Picture a salmon jumping up a stream."),
    ("shi", "し", "shi", "", "A fishing hook. She is fishing: 'shi'."),
    ("su", "す", "su", "", "A line with a loop, like a curly straw. Sip some soup: 'su'."),
    ("se", "せ", "se", "", "Looks like a seat with a back. 'se' as in 'set'."),
    ("so", "そ", "so", "", "One zigzag stroke, like thread when you sew: 'so'."),
   ]),
   "words": words([("すし", "sushi", "sushi"), ("あさ", "asa", "morning"), ("かさ", "kasa", "umbrella"),
                   ("せかい", "sekai", "world"), ("いす", "isu", "chair"), ("うそ", "uso", "a lie")])},
 ]}

mandarin = {
 "id": "zh_basics_course", "lang": "zh", "title": "Mandarin basics, step by step",
 "description": "Tones first, then your first characters.",
 "units": [
  {"id": "tones", "title": "The four tones",
   "intro": [
    "Mandarin is written with characters called hanzi. Each character is one syllable and has a meaning.",
    "Pinyin spells the sound of a character with Latin letters, like 'ma'. It is a helper, the same way romaji helps with Japanese.",
    "The mark above the vowel is the tone: how your voice moves while you say the syllable. A different tone makes a different word.",
    "1st tone (mā): high and flat, like holding one sung note. 2nd tone (má): rising, like asking 'what?'",
    "3rd tone (mǎ): low and dipping, like a doubtful 'well...'. 4th tone (mà): a sharp fall, like a firm 'No!'",
    "Neutral tone (ma): no mark. Short and light.",
    "In this unit the same syllable, 'ma', is five different words. Listen to each one a few times before you move on.",
   ],
   "items": items("zh_tones", [
    ("1", "妈", "mā", "mother", "1st tone: high and flat. The flat line over the a is the shape of your voice."),
    ("2", "麻", "má", "hemp", "2nd tone: rising. The mark climbs upward, and so does your voice."),
    ("3", "马", "mǎ", "horse", "3rd tone: dips low. The mark is a small valley: go down, then a little up."),
    ("4", "骂", "mà", "to scold", "4th tone: sharp fall. The mark drops, like a scolding 'No!'"),
    ("5", "吗", "ma", "question word", "Neutral tone: light and short. Put 吗 at the end of a sentence to make it a yes/no question."),
   ]),
   "words": []},
  {"id": "numbers_1_5", "title": "Numbers 1 to 5",
   "intro": [
    "Numbers are a good first set of hanzi. The first three are just lines you can count.",
    "Reading pinyin: 'yī' sounds like 'ee'. 'èr' sounds like 'are'. 'sān' sounds like 'sahn'.",
    "'sì' is the tricky one: the i after s is not 'ee'. Say 's' and keep buzzing, like 'sz'. 'wǔ' sounds like 'woo'.",
    "Watch the tone marks. They tell you how to move your voice, just like in the last unit.",
   ],
   "items": items("zh_hanzi", [
    ("1", "一", "yī", "one", "One line means one. 1st tone: high and flat, like the line itself."),
    ("2", "二", "èr", "two", "Two lines mean two. 4th tone: falling."),
    ("3", "三", "sān", "three", "Three lines mean three. 1st tone: high and flat."),
    ("4", "四", "sì", "four", "A box with four sides, like a window with curtains. 4th tone: falling."),
    ("5", "五", "wǔ", "five", "A shape standing between a top line and a bottom line. 3rd tone: dipping."),
   ]),
   "words": []},
  {"id": "numbers_6_10", "title": "Numbers 6 to 10",
   "intro": [
    "Five more and you can count to ten.",
    "Reading pinyin: 'q' sounds like 'ch', so 'qī' is 'chee'. 'j' is a soft 'j', so 'jiǔ' is close to 'jyoh'.",
    "'shí' is not 'she'. The i after sh sounds like 'r': say 'shr' with a rising voice. 'liù' is close to 'lyoh', 'bā' is 'bah'.",
    "Then the fun part. Bigger numbers are built from pieces: 十一 is ten-one, which is 11. 二十 is two-ten, which is 20.",
   ],
   "items": items("zh_hanzi", [
    ("6", "六", "liù", "six", "A person with a hat, arms out and legs apart. 4th tone: falling."),
    ("7", "七", "qī", "seven", "Like an upside-down 7 with a line through it. 1st tone: high and flat."),
    ("8", "八", "bā", "eight", "Two strokes leaning apart. 1st tone: high and flat."),
    ("9", "九", "jiǔ", "nine", "Close to a cross, but with a hooked tail: nine is almost ten. 3rd tone: dipping."),
    ("10", "十", "shí", "ten", "A cross, like a plus sign. 2nd tone: rising."),
   ]),
   "words": words([("十一", "shíyī", "eleven (ten + one)"), ("十五", "shíwǔ", "fifteen (ten + five)"),
                   ("二十", "èrshí", "twenty (two tens)"), ("三十", "sānshí", "thirty (three tens)"),
                   ("九十九", "jiǔshíjiǔ", "ninety-nine (nine tens + nine)")])},
 ]}

os.makedirs(OUT, exist_ok=True)
for name, course in (("ja_hiragana_course", hiragana), ("zh_basics_course", mandarin)):
    for unit in course["units"]:
        ids = [i["id"] for i in unit["items"]]
        assert len(ids) == len(set(ids)), unit["id"]
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(course, f, ensure_ascii=False, indent=1)
    print(name, [(u["id"], len(u["items"]), len(u["words"])) for u in course["units"]])
