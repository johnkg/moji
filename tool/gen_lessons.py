"""Regenerates assets/lessons/*.json. Content is hand-written (no third-party data).

Items are looked up in assets/decks/ by card id, so lesson text always matches
the flashcard it feeds. Run tool/gen_decks.py first if decks changed.
"""
import json, os
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, '..', 'assets', 'lessons')
DECKS = os.path.join(HERE, '..', 'assets', 'decks')

def deck_cards(deck):
    with open(os.path.join(DECKS, deck + '.json'), encoding='utf-8') as f:
        return {c['id']: c for c in json.load(f)['cards']}

def items(deck, rows):
    """rows: (card id, hint) or (card id, hint, listen)."""
    cards = deck_cards(deck)
    out = []
    for row in rows:
        cid, hint = row[0], row[1]
        c = cards[cid]
        item = {"id": cid, "front": c["front"], "reading": c["reading"], "meaning": c["meaning"],
                "hint": hint, "card": f"{deck}:{cid}"}
        if len(row) > 2 and row[2] is False:
            item["listen"] = False
        out.append(item)
    return out

def words(rows):
    return [{"text": t, "reading": r, "meaning": m} for t, r, m in rows]

def unit(uid, title, intro, its, wds=()):
    return {"id": uid, "title": title, "intro": intro, "items": its, "words": words(wds)}

H = "ja_hiragana"
hiragana = {
 "id": "ja_hiragana_course", "lang": "ja", "mode": "reading", "title": "Read: hiragana, step by step",
 "description": "Learn to read Japanese sounds, a few characters at a time.",
 "units": [
  unit("vowels", "The five vowels", [
    "Japanese is written with three scripts mixed together. Hiragana is the one to learn first. It has 46 characters.",
    "Each hiragana character is one sound. Unlike English letters, a character is always read the same way.",
    "Japanese has only five vowel sounds: a, i, u, e, o. Always in that order. Every other character is a consonant plus one of these five.",
    "How they sound: a = 'ah' as in father. i = 'ee' as in see. u = 'oo' as in food. e = 'eh' as in bed. o = 'oh' as in go. Keep each one short.",
    "The text under each character (like 'a') is romaji: Japanese sounds spelled with English letters. It is only a helper.",
   ], items(H, [
    ("a", "Sounds like 'ah'. Look for a capital A hiding in the middle: crossing strokes over a loop."),
    ("i", "Sounds like 'ee'. Two strokes side by side, like two eels swimming together."),
    ("u", "Sounds like 'oo'. A dash above a bent line, like someone hit in the belly going 'oof'."),
    ("e", "Sounds like 'eh'. A runner full of energy: a dash for the head, legs stretched out."),
    ("o", "Sounds like 'oh'. Close to あ, but with an extra dot on the right: 'oh, a dot!'"),
   ]), [("あい", "ai", "love"), ("いえ", "ie", "house"), ("うえ", "ue", "above"),
        ("あおい", "aoi", "blue"), ("いいえ", "iie", "no")]),
  unit("k_row", "The K row", [
    "Now put a k sound in front of each vowel: ka, ki, ku, ke, ko.",
    "Same vowel order as before: a, i, u, e, o. Every row in the hiragana chart follows it.",
    "After this unit you can read real words made of vowels and K sounds.",
   ], items(H, [
    ("ka", "A blade swinging down with a spark flying off: 'ka!' like a karate chop."),
    ("ki", "Looks like an old key with two teeth on top."),
    ("ku", "An open bird beak calling 'coo, coo'."),
    ("ke", "A post on the left and a gate on the right. 'ke' as in 'kept': the gate is kept shut."),
    ("ko", "Two short curved lines, like two koi fish swimming."),
   ]), [("かお", "kao", "face"), ("あか", "aka", "red"), ("えき", "eki", "station"),
        ("いけ", "ike", "pond"), ("ここ", "koko", "here"), ("きく", "kiku", "to listen")]),
  unit("s_row", "The S row", [
    "The S row: sa, shi, su, se, so.",
    "One surprise: the second one is 'shi', not 'si'. Japanese has no 'si' sound.",
    "さ looks a lot like き from the last unit. さ has one bar, き has two.",
   ], items(H, [
    ("sa", "Like き with only one bar. Picture a salmon jumping up a stream."),
    ("shi", "A fishing hook. She is fishing: 'shi'."),
    ("su", "A line with a loop, like a curly straw. Sip some soup: 'su'."),
    ("se", "Looks like a seat with a back. 'se' as in 'set'."),
    ("so", "One zigzag stroke, like thread when you sew: 'so'."),
   ]), [("すし", "sushi", "sushi"), ("あさ", "asa", "morning"), ("かさ", "kasa", "umbrella"),
        ("せかい", "sekai", "world"), ("いす", "isu", "chair"), ("うそ", "uso", "a lie")]),
  unit("t_row", "The T row", [
    "The T row: ta, chi, tsu, te, to.",
    "Two surprises this time. The second is 'chi', not 'ti'. The third is 'tsu', not 'tu'.",
    "'tsu' is the sound at the end of 'cats', then 'oo'. It is one beat, not two.",
   ], items(H, [
    ("ta", "Looks like a small t and a small a squeezed together: 'ta'."),
    ("chi", "Like the number 5 with a bar on top. 'chi' as in 'cheese'."),
    ("tsu", "One sweeping curve, like a big wave: tsunami."),
    ("te", "A bar on top with a curved tail, like a capital T bending over. 'te' as in 'ten'."),
    ("to", "A short stick poking into a curve, like a thorn stuck in a toe: 'to'."),
   ]), [("たこ", "tako", "octopus"), ("つくえ", "tsukue", "desk"), ("とけい", "tokei", "clock"),
        ("そと", "soto", "outside"), ("あした", "ashita", "tomorrow"), ("くつ", "kutsu", "shoes")]),
  unit("n_row", "The N row", [
    "The N row: na, ni, nu, ne, no. No surprises here.",
    "Careful with ぬ and ね. They look alike. ぬ has two loops tangled together. ね has a straight post on the left.",
   ], items(H, [
    ("na", "A cross, a dash, and a loop at the bottom like a knot in a rope. 'na' as in 'nacho'."),
    ("ni", "A post on the left and two short lines on the right. 'ni' sounds like 'knee'."),
    ("nu", "Tangled loops, like noodles. 'nu' as in 'noodle'."),
    ("ne", "A post on the left and a curled tail on the right, like a cat's tail. 'neko' means cat."),
    ("no", "One swirl drawn without lifting the pen: 'no'."),
   ]), [("ねこ", "neko", "cat"), ("いぬ", "inu", "dog"), ("なに", "nani", "what"),
        ("にく", "niku", "meat"), ("きのこ", "kinoko", "mushroom"), ("なつ", "natsu", "summer")]),
  unit("h_row", "The H row", [
    "The H row: ha, hi, fu, he, ho.",
    "The third one is 'fu', not 'hu'. It is a soft f: blow air between your lips without biting your lower lip.",
    "Later you will see は read as 'wa' when it works as a grammar marker. For now it is 'ha'.",
   ], items(H, [
    ("ha", "A post on the left, then a cross with a loop at the bottom. 'ha' as in 'ha ha'."),
    ("hi", "A wide smile: 'hee hee'."),
    ("fu", "A curvy middle with small strokes around it, like a mountain with clouds: Mount Fuji."),
    ("he", "One bent line, like a small hill. 'he' as in 'hen'."),
    ("ho", "Like は with one more bar on top, as if it put on a hat: 'ho ho'."),
   ]), [("はな", "hana", "flower"), ("ひと", "hito", "person"), ("ふね", "fune", "boat"),
        ("ほし", "hoshi", "star"), ("はこ", "hako", "box"), ("ほね", "hone", "bone")]),
  unit("m_row", "The M row", [
    "The M row: ma, mi, mu, me, mo. No surprises in the sounds.",
    "め looks like ぬ from the N row. め ends in a plain curve. ぬ ends in an extra loop.",
   ], items(H, [
    ("ma", "Two bars across a pole, with a loop at the foot. 'ma' as in 'mama'."),
    ("mi", "A loop with a long tail and a stroke crossing it, like a music note falling over: do, re, 'mi'."),
    ("mu", "A loop on the left, a hook and a dot on the right. A cow says 'moo': 'mu'."),
    ("me", "Like ぬ without the last loop. 'me' is also the Japanese word for eye."),
    ("mo", "A fishing hook with two bars across it: catch 'mo'-re fish."),
   ]), [("みみ", "mimi", "ear"), ("くも", "kumo", "cloud"), ("むし", "mushi", "insect"),
        ("あめ", "ame", "rain"), ("もも", "momo", "peach"), ("なまえ", "namae", "name")]),
  unit("y_row", "The Y row", [
    "The Y row has only three characters: ya, yu, yo. There is no 'yi' or 'ye' in modern Japanese.",
    "'yu' sounds like the English word 'you'.",
   ], items(H, [
    ("ya", "A curve with two strokes through it, like the horned head of a yak: 'ya'."),
    ("yu", "A loop with a line through the middle, like a fish. 'yu' sounds like 'you'."),
    ("yo", "A post with a small arm and a loop at the bottom, like a yo-yo on its string."),
   ]), [("やま", "yama", "mountain"), ("ゆき", "yuki", "snow"), ("へや", "heya", "room"),
        ("ふゆ", "fuyu", "winter"), ("やさい", "yasai", "vegetables"), ("つよい", "tsuyoi", "strong")]),
  unit("r_row", "The R row", [
    "The R row: ra, ri, ru, re, ro.",
    "The Japanese r is not the English r. Tap the tip of your tongue once just behind your top teeth. It lands between an English r, l and d.",
    "Three look-alikes: る ends in a loop, ろ does not. れ looks like ね, but its tail kicks outward instead of curling.",
   ], items(H, [
    ("ra", "A dash floating above a curve, like a rabbit's ear above its back: 'ra'."),
    ("ri", "Two strokes, the right one longer, like reeds by a river. 'ri' sounds like 'ree'."),
    ("ru", "A zigzag that ends in a loop: the route loops at the end, 'ru'."),
    ("re", "A post on the left and a tail that kicks out to the right. 're' as in 'red'."),
    ("ro", "Like る with no loop: the road just ends, 'ro'."),
   ]), [("さくら", "sakura", "cherry blossom"), ("とり", "tori", "bird"), ("くるま", "kuruma", "car"),
        ("これ", "kore", "this"), ("いろ", "iro", "color"), ("よる", "yoru", "night")]),
  unit("w_n", "The last three", [
    "Three characters left: wa, wo and n. After this you can read all 46 basic hiragana.",
    "を is written 'wo' in romaji but said 'o', the same as お. It is only used as a grammar marker, never inside a word.",
    "ん is the only character with no vowel. It is a plain 'n' sound and never starts a word.",
   ], items(H, [
    ("wa", "A post on the left and one big round curve on the right, like a round belly: 'wa'."),
    ("wo", "Said 'o'. Marks the thing an action is done to. You will meet it in sentences later.", False),
    ("n", "Looks like a handwritten lowercase n: 'n'."),
   ]), [("わたし", "watashi", "I / me"), ("ほん", "hon", "book"), ("にほん", "nihon", "Japan"),
        ("せんせい", "sensei", "teacher"), ("かわ", "kawa", "river"), ("みんな", "minna", "everyone")]),
 ]}

P = "ja_phrases"
ja_speaking = {
 "id": "ja_speaking_course", "lang": "ja", "mode": "speaking", "title": "Speak: first phrases",
 "description": "Sound first. Say useful phrases before you can read them.",
 "units": [
  unit("greetings", "Hello and goodbye", [
    "You can start speaking before you can read. This path is sound first.",
    "Each phrase is shown in romaji (English letters) so you can say it. The Japanese writing is shown small underneath. Do not worry about reading it yet.",
    "Japanese is spoken in even beats. Give every syllable the same length, and do not stress one harder than the others.",
    "Tap the speaker and repeat out loud. Saying it matters more than tapping the right answer.",
   ], items(P, [
    ("1", "The daytime hello. Even beats: kon-ni-chi-wa. Hold the first n a little."),
    ("6", "'ou' is one long 'oh', not 'oh-oo': o-ha-yoh. Add 'gozaimasu' after it to be polite."),
    ("7", "The evening hello: kon-ban-wa."),
    ("8", "sa-yoh-na-ra. A real goodbye, for when you will not meet again soon. With friends, people often say 'ja ne'."),
   ])),
  unit("yes_no_thanks", "Yes, no, thank you", [
    "Five short phrases that carry most simple exchanges.",
    "The Japanese r is a quick tap of the tongue behind the top teeth, close to a soft d. You will hear it in 'arigatou'.",
   ], items(P, [
    ("4", "Sounds like the English word 'hi'. Short and crisp."),
    ("5", "A long 'ee', then 'eh': ee-eh."),
    ("2", "a-ri-ga-toh. The 'ou' at the end is one long 'oh'."),
    ("3", "su-mi-ma-sen. Use it to get attention, to apologize, or to squeeze past someone."),
    ("9", "o-ne-gai-shi-mas. The last u is almost silent. Say it when you ask for something."),
   ])),
  unit("getting_by", "Getting by", [
    "Three phrases for shops, restaurants and moments when you are lost.",
    "A 'ka' at the end of a sentence turns it into a question. Your voice does not need to rise.",
   ], items(P, [
    ("10", "wa-ka-ri-ma-sen. The '-masen' ending means 'do not'."),
    ("11", "i-ku-ra des-ka. 'desu' sounds like 'des'. The 'ka' makes it a question."),
    ("12", "o-i-shee. The double i is one long 'ee'. Say it when the food is good."),
   ])),
 ]}

Z = "zh_hanzi"
mandarin = {
 "id": "zh_basics_course", "lang": "zh", "mode": "reading", "title": "Read: tones and first characters",
 "description": "Tones first, then your first hanzi.",
 "units": [
  unit("tones", "The four tones", [
    "Mandarin is written with characters called hanzi. Each character is one syllable and has a meaning.",
    "Pinyin spells the sound of a character with Latin letters, like 'ma'. It is a helper, the same way romaji helps with Japanese.",
    "The mark above the vowel is the tone: how your voice moves while you say the syllable. A different tone makes a different word.",
    "1st tone (mā): high and flat, like holding one sung note. 2nd tone (má): rising, like asking 'what?'",
    "3rd tone (mǎ): low and dipping, like a doubtful 'well...'. 4th tone (mà): a sharp fall, like a firm 'No!'",
    "Neutral tone (ma): no mark. Short and light.",
    "In this unit the same syllable, 'ma', is five different words. Listen to each one a few times before you move on.",
   ], items("zh_tones", [
    ("1", "1st tone: high and flat. The flat line over the a is the shape of your voice."),
    ("2", "2nd tone: rising. The mark climbs upward, and so does your voice."),
    ("3", "3rd tone: dips low. The mark is a small valley: go down, then a little up."),
    ("4", "4th tone: sharp fall. The mark drops, like a scolding 'No!'"),
    ("5", "Neutral tone: light and short. Put 吗 at the end of a sentence to make it a yes/no question."),
   ])),
  unit("numbers_1_5", "Numbers 1 to 5", [
    "Numbers are a good first set of hanzi. The first three are just lines you can count.",
    "Reading pinyin: 'yī' sounds like 'ee'. 'èr' sounds like 'are'. 'sān' sounds like 'sahn'.",
    "'sì' is the tricky one: the i after s is not 'ee'. Say 's' and keep buzzing, like 'sz'. 'wǔ' sounds like 'woo'.",
    "Watch the tone marks. They tell you how to move your voice, just like in the last unit.",
   ], items(Z, [
    ("1", "One line means one. 1st tone: high and flat, like the line itself."),
    ("2", "Two lines mean two. 4th tone: falling."),
    ("3", "Three lines mean three. 1st tone: high and flat."),
    ("4", "A box with four sides, like a window with curtains. 4th tone: falling."),
    ("5", "A shape standing between a top line and a bottom line. 3rd tone: dipping."),
   ])),
  unit("numbers_6_10", "Numbers 6 to 10", [
    "Five more and you can count to ten.",
    "Reading pinyin: 'q' sounds like 'ch', so 'qī' is 'chee'. 'j' is a soft 'j', so 'jiǔ' is close to 'jyoh'.",
    "'shí' is not 'she'. The i after sh sounds like 'r': say 'shr' with a rising voice. 'liù' is close to 'lyoh', 'bā' is 'bah'.",
    "Then the fun part. Bigger numbers are built from pieces: 十一 is ten-one, which is 11. 二十 is two-ten, which is 20.",
   ], items(Z, [
    ("6", "A person with a hat, arms out and legs apart. 4th tone: falling."),
    ("7", "Like an upside-down 7 with a line through it. 1st tone: high and flat."),
    ("8", "Two strokes leaning apart. 1st tone: high and flat."),
    ("9", "Close to a cross, but with a hooked tail: nine is almost ten. 3rd tone: dipping."),
    ("10", "A cross, like a plus sign. 2nd tone: rising."),
   ]), [("十一", "shíyī", "eleven (ten + one)"), ("十五", "shíwǔ", "fifteen (ten + five)"),
        ("二十", "èrshí", "twenty (two tens)"), ("三十", "sānshí", "thirty (three tens)"),
        ("九十九", "jiǔshíjiǔ", "ninety-nine (nine tens + nine)")]),
  unit("you_and_me", "You and me", [
    "Many hanzi are built from smaller parts, and the parts give clues. Watch the left side of the characters in this unit.",
    "亻 on the left is a squeezed form of 人, person. 女 on the left means woman.",
    "Reading pinyin: 'wǒ' is close to 'waw'. 'nǐ' is 'nee'. 'tā' is 'tah'. 'hǎo' is 'how'.",
    "他 (he) and 她 (she) sound exactly the same. You can only tell them apart in writing.",
   ], items(Z, [
    ("14", "I, me. Many strokes, but you will see it so often it sticks. 3rd tone: dipping."),
    ("15", "亻 (person) on the left: the person in front of me is you. 3rd tone: dipping."),
    ("16", "亻 (person) on the left: he. 1st tone: high and flat."),
    ("17", "女 (woman) on the left: she. Same sound as 他."),
    ("18", "女 (woman) next to 子 (child): together they mean good. 3rd tone: dipping."),
   ]), [("你好", "nǐ hǎo", "hello (you + good)")]),
  unit("small_words", "Small words", [
    "Five characters that show up in almost every sentence.",
    "Reading pinyin: 'rén' starts with a buzzing r, tongue curled back. 'dà' is 'dah'. 'xiǎo' is close to 'shyow': x is a soft sh.",
    "是 is 'to be'. Mandarin uses the same word for am, is and are. No changes to memorize.",
    "不 means 'not'. It is 'bù', but in front of another falling tone it flips to rising: 不是 is 'bú shì'.",
   ], items(Z, [
    ("11", "A person walking, seen from the side: two legs. 2nd tone: rising."),
    ("12", "A person stretching both arms out wide: big. 4th tone: falling."),
    ("13", "A center stroke with two small strokes falling away from it: small. 3rd tone: dipping."),
    ("19", "To be. 日 (sun) sits on top. 'shr' with a sharp fall."),
    ("20", "Not. A line on top, like a lid holding things down. 4th tone: falling."),
   ]), [("大人", "dàren", "adult (big person)"), ("好人", "hǎorén", "good person"),
        ("不是", "bú shì", "is not"), ("不好", "bù hǎo", "not good"),
        ("我是", "wǒ shì", "I am"), ("你是", "nǐ shì", "you are")]),
  unit("nature", "Sun, moon, fire, water", [
    "Some of the oldest hanzi started as drawings. These five still look a little like what they mean.",
    "Reading pinyin: 'shuǐ' is close to 'shway'. 'huǒ' is 'hwaw'. 'shān' is 'shahn'. 'yuè' is 'yweh'.",
    "'rì' is hard: curl your tongue back and buzz, like the r in 'run' held on its own, with a falling voice.",
    "日 also means day, and 月 also means month. So 一月 is month one: January.",
   ], items(Z, [
    ("22", "A stream down the middle with splashes on both sides. 3rd tone: dipping."),
    ("23", "A fire with a spark flying off each side. 3rd tone: dipping."),
    ("24", "Three peaks: a mountain. 1st tone: high and flat."),
    ("25", "It began as a circle with a dot: the sun. Also means day. 4th tone: falling."),
    ("26", "A crescent moon standing upright. Also means month. 4th tone: falling."),
   ]), [("火山", "huǒshān", "volcano (fire mountain)"), ("山水", "shānshuǐ", "landscape (mountain and water)"),
        ("大山", "dà shān", "big mountain"), ("小山", "xiǎo shān", "hill (small mountain)"),
        ("一月", "yīyuè", "January (month one)"), ("十月", "shíyuè", "October (month ten)")]),
  unit("daily", "Have, eat, drink", [
    "Three everyday verbs and the name of the country.",
    "口 is a mouth. Both 吃 (eat) and 喝 (drink) have it on the left.",
    "Reading pinyin: 'yǒu' sounds like 'yo'. 'zhōng' is close to 'jong'. 'guó' is 'gwaw'. 'chī' is 'chr', high and flat. 'hē' is close to 'huh'.",
    "中国 is 'middle country': China. Add 人 and you get 中国人, a Chinese person.",
   ], items(Z, [
    ("21", "To have. The bottom looks like 月. Picture a hand on top holding it. 3rd tone: dipping."),
    ("27", "A line straight through the middle of a box: middle. 1st tone: high and flat."),
    ("28", "A border around something precious: country. 2nd tone: rising."),
    ("29", "口 (mouth) on the left: eat. 1st tone: high and flat."),
    ("30", "口 (mouth) on the left again: drink. 1st tone: high and flat."),
   ]), [("中国", "Zhōngguó", "China (middle country)"), ("中国人", "Zhōngguórén", "Chinese person"),
        ("喝水", "hē shuǐ", "drink water"), ("我有", "wǒ yǒu", "I have"),
        ("不吃", "bù chī", "not eat"), ("不喝", "bù hē", "not drink")]),
 ]}

Q = "zh_phrases"
zh_speaking = {
 "id": "zh_speaking_course", "lang": "zh", "mode": "speaking", "title": "Speak: first phrases",
 "description": "Sound first. Say useful phrases before you can read them.",
 "units": [
  unit("greetings", "Hello and goodbye", [
    "This path is sound first. Phrases are shown in pinyin so you can say them. The characters are shown small underneath.",
    "Tones matter for being understood. If you have not done 'The four tones' in the reading path, do it first or right after this.",
    "Tap the speaker, listen for how the voice moves, and repeat out loud.",
   ], items(Q, [
    ("1", "Sounds like 'nee how'. Two dipping tones in a row are hard to say, so the first one rises instead."),
    ("7", "Close to 'dzow-shahng how'. z sounds like the 'ds' in 'kids'."),
    ("6", "Close to 'dzai jyen'. Both syllables fall sharply. It means 'see you again'."),
   ])),
  unit("thanks_sorry", "Thanks and sorry", [
    "Two pairs: a phrase, and the usual answer to it.",
    "In pinyin, x is a soft 'sh' and q is a soft 'ch', both made with the tongue flat behind the lower teeth.",
   ], items(Q, [
    ("2", "Close to 'shyeh-shyeh'. The first one falls, the second is light."),
    ("3", "Close to 'boo kuh-chee'. The usual answer to 谢谢."),
    ("4", "Close to 'dway-boo-chee'. For a real apology."),
    ("5", "Close to 'may gwahn-shee'. The usual answer to 'sorry': no problem."),
   ])),
  unit("getting_by", "Getting by", [
    "Phrases for shops and for moments when you are lost.",
    "Mandarin has no single word for 'yes'. You repeat the verb. 是 means 'it is', and 不是 means 'it is not'.",
   ], items(Q, [
    ("8", "Close to 'ching' with a dipping tone. Put it before a request."),
    ("11", "Close to 'shr' with a sharp fall. It means 'it is'."),
    ("12", "Close to 'boo shr'. 不 means 'not'."),
    ("9", "Close to 'waw boo dong'. 我 is I, 不 is not, 懂 is understand."),
    ("10", "Close to 'dwaw-shao chyen'. 钱 means money."),
   ])),
 ]}

os.makedirs(OUT, exist_ok=True)
for course in (ja_speaking, hiragana, zh_speaking, mandarin):
    for u in course["units"]:
        ids = [i["id"] for i in u["items"]]
        assert len(ids) == len(set(ids)), u["id"]
    assert len({u["id"] for u in course["units"]}) == len(course["units"])
    with open(os.path.join(OUT, course["id"] + ".json"), "w", encoding="utf-8") as f:
        json.dump(course, f, ensure_ascii=False, indent=1)
    print(course["id"], [(u["id"], len(u["items"]), len(u["words"])) for u in course["units"]])
