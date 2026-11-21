"""Regenerates assets/lessons/*.json. Content is hand-written (no third-party data).

Items are looked up in assets/decks/ by card id, so lesson text always matches
the flashcard it feeds. Run tool/gen_decks.py first if decks changed.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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

K = "ja_katakana"
katakana = {
 "id": "ja_katakana_course", "lang": "ja", "mode": "reading", "title": "Read: katakana, step by step",
 "description": "The second script. Mostly used for foreign words like ice cream and hotel.",
 "units": [
  unit("k_vowels", "The five vowels", [
    "Katakana is the second Japanese script. It has the same 46 sounds as hiragana, just written with sharper, straighter shapes.",
    "It is mostly used for words borrowed from other languages: hotel, coffee, America. Names of foreign people and places are written in it too.",
    "So you already know every sound. This path is about learning a new set of shapes for them. Start with the five vowels: a, i, u, e, o.",
    "Katakana is drawn with straight strokes and sharp corners. Hiragana is curvy. That is the quickest way to tell them apart.",
   ], items(K, [
    ("a", "Looks like an axe: 'ah!' as it hits the log."),
    ("i", "Two strokes, a short slash and a post, like an eel on a stick. 'ee'."),
    ("u", "Two dashes on a cap with a hook below, like a surprised face going 'ooh'."),
    ("e", "Like a capital I: an elevator shaft, 'eh'."),
    ("o", "A cross bar with a slash through it, like a person with open arms going 'oh!'."),
   ])),
  unit("k_k_row", "The K row", [
    "The K row in katakana: ka, ki, ku, ke, ko.",
    "Careful with ク and ケ. ク has no vertical post. ケ has one. Also compare ク with タ from a later unit: タ has an extra stroke.",
    "ケ and コ both look square and tidy. コ is just two lines forming a corner.",
   ], items(K, [
    ("ka", "Like the hiragana か without its extra dot: a blade and a hook, 'ka'."),
    ("ki", "A key with three teeth: 'ki' for key."),
    ("ku", "Like an open-mouthed bird beak, angled. 'ku' as in 'cool'."),
    ("ke", "Looks like a capital K made of straight lines, with a post. 'ke' as in 'kept'."),
    ("ko", "A corner, like the letter L turned over. Two lines, 'ko'."),
   ]), [("ココア", "kokoa", "cocoa"), ("エコ", "eko", "eco")]),
  unit("k_s_row", "The S row", [
    "The S row in katakana: sa, shi, su, se, so.",
    "Same surprise as hiragana: the second one is 'shi', not 'si'.",
    "Big trap coming: シ (shi) and ソ (so) look nearly the same, and so do ツ (tsu) and ン (n) later. The difference is the angle. シ has two short dashes and a long sweep that goes up. ソ has one dash and a long stroke that goes down.",
   ], items(K, [
    ("sa", "Three strokes, like a sail on a boat. 'sa'."),
    ("shi", "Three strokes, two dots on the left lying flat and a sweep rising: 'she smiles', lying on her side."),
    ("su", "A horizontal bar with a hook that bends: a snake on a rock. 'su' as in 'sue'."),
    ("se", "Looks like a seat with a back, a bit like it fell over. 'se' as in 'set'."),
    ("so", "A dash and a long stroke going down, like a stitch of sewing thread: 'so'."),
   ]), [("スイス", "suisu", "Switzerland"), ("アイス", "aisu", "ice"), ("キス", "kisu", "kiss"),
        ("サイ", "sai", "rhino")]),
  unit("k_t_row", "The T row", [
    "The T row in katakana: ta, chi, tsu, te, to.",
    "Remember the surprises: the second one is 'chi' and the third is 'tsu'.",
    "ツ (tsu) and シ (shi) are twins. ツ has its two dashes on top, pointing down. シ has them on the left, lying flat. Tsu stands tall, shi lies down.",
   ], items(K, [
    ("ta", "Like ク with one more stroke through it, like a 'ta'-ble with a leg: 'ta'."),
    ("chi", "Three strokes: a short bar, a cross-bar, and a long hook, like a chair. 'chi' as in 'cheese'."),
    ("tsu", "Three strokes, two dashes on top and a sweep: tsunami waves coming down."),
    ("te", "A telephone pole with two cross-bars. 'te' as in 'ten'."),
    ("to", "A post with a small stick leaning on it, like a toe. 'to'."),
   ]), [("テスト", "tesuto", "test"), ("テキスト", "tekisuto", "text"), ("コスト", "kosuto", "cost")]),
  unit("k_n_row", "The N row", [
    "The N row in katakana: na, ni, nu, ne, no.",
    "ノ (no) is just one slanted stroke, the simplest katakana of all. It is part of many others, like メ and ア.",
    "ヌ (nu) and ス (su) look alike. ヌ has an extra stroke crossing the hook.",
   ], items(K, [
    ("na", "A cross with a slash through it, like a knife: 'na' as in 'nacho'. Careful: メ (me) has no bar on top."),
    ("ni", "Two lines, one above the other, like the number 2. 'ni' sounds like 'knee', and ni also means 'two' in Japanese."),
    ("nu", "Like ス with an extra stroke across the hook, like noodles being pulled. 'nu' as in 'noodle'."),
    ("ne", "A dash on top of a hooked post with a small tail, like a fishing net on a pole: 'ne'."),
    ("no", "One slash from top right to bottom left. 'no'."),
   ]), [("テニス", "tenisu", "tennis"), ("ナイス", "naisu", "nice"), ("ネクタイ", "nekutai", "necktie")]),
  unit("k_h_row", "The H row", [
    "The H row in katakana: ha, hi, fu, he, ho.",
    "Again 'fu' is a soft f: blow air between your lips, no biting.",
    "ヘ (he) is almost the same as the hiragana へ. Learn them as one shape. ホ (ho) looks like a tree with a cross-bar.",
   ], items(K, [
    ("ha", "Like the roof of a house with a left and a right slope: 'ha'."),
    ("hi", "Like a hook on a post, as if hoisting a flag: 'hi'."),
    ("fu", "A flat roof over a hook, like a fur hood. 'fu'."),
    ("he", "The same shape as hiragana へ: one little hill. 'he' as in 'hen'."),
    ("ho", "A tree with a cross-bar and two small leaves, like 'ho ho ho', Santa's tree."),
   ]), [("ハイ", "hai", "yes / high"), ("ヘア", "hea", "hair"), ("ハイテク", "haiteku", "high-tech"), ("ホスト", "hosuto", "host")]),
  unit("k_m_row", "The M row", [
    "The M row in katakana: ma, mi, mu, me, mo.",
    "メ (me) looks like ノ crossed by another line, a bit like an X. Do not mix it up with ナ (na): ナ has a horizontal bar on top.",
   ], items(K, [
    ("ma", "A triangle with a stroke inside, like a map of mountains: 'ma'."),
    ("mi", "Three slanted lines, like three fingers held up: 'mi' for 'me, me, me'."),
    ("mu", "A small triangle with a tail, like a cow's head saying 'moo': 'mu'."),
    ("me", "Two strokes crossing like an X: the eye of a needle, 'me' for eye."),
    ("mo", "Like the hiragana も made of straight lines: two bars and a hooked post, 'mo'."),
   ]), [("アニメ", "anime", "anime"), ("メモ", "memo", "memo"), ("ミス", "misu", "mistake"),
        ("マスク", "masuku", "mask"), ("タイム", "taimu", "time")]),
  unit("k_y_row", "The Y row", [
    "The Y row in katakana has only three: ya, yu, yo.",
    "ユ (yu) looks like a corner with an extra line. Careful: コ (ko) is just a corner, ユ has a long tail.",
   ], items(K, [
    ("ya", "A cross with a drooping arm, like a yak with its head down: 'ya'."),
    ("yu", "A corner shape that looks like a U with a flat bottom: 'you'."),
    ("yo", "Three horizontal lines hanging off a post, like a yo-yo string: 'yo'."),
   ]), [("メキシコ", "mekishiko", "Mexico")]),
  unit("k_r_row", "The R row", [
    "The R row in katakana: ra, ri, ru, re, ro.",
    "Same soft Japanese r as before, a quick tap of the tongue, between r, l, and d.",
    "ロ (ro) is a plain square. ル (ru) has two legs, and the right one has a hook.",
   ], items(K, [
    ("ra", "A dash on top of a hooked line, like a rack with a hat. 'ra'."),
    ("ri", "Two vertical lines, the right one hooked. 'ri' like 'ree'."),
    ("ru", "A post with a hook on the right and a long leg on the left, like a person walking: 'ru'."),
    ("re", "A single hook on a post, like the letter L slanted: 're' as in 'red'."),
    ("ro", "A plain square, like a road sign: 'ro'."),
   ]), [("アメリカ", "amerika", "America"), ("イタリア", "itaria", "Italy"), ("ロシア", "roshia", "Russia"),
        ("ホテル", "hoteru", "hotel"), ("ライス", "raisu", "rice"), ("コアラ", "koara", "koala")]),
  unit("k_w_n", "The last three", [
    "Three characters left: wa, wo and n. After this you can read all 46 basic katakana.",
    "ヲ (wo) is said 'o'. It is hardly used in katakana, so we skip its listening test.",
    "ン (n) and ソ (so) look alike. ン is nearly horizontal on its left: the dash points down and to the right in a flat angle. ソ looks like it is falling.",
    "ワ (wa) looks like ウ (u) without the top dash.",
   ], items(K, [
    ("wa", "Like ウ without the dash on top: a wide mouth, 'wa'."),
    ("wo", "Said 'o'. Almost never used in katakana. Just recognize it.", False),
    ("n", "Two strokes: a dash and a sweep that lies flat, like a person lying on their side saying 'n'."),
   ]), [("ワイン", "wain", "wine"), ("ランチ", "ranchi", "lunch"), ("カメラ", "kamera", "camera"),
        ("ライオン", "raion", "lion"), ("アンテナ", "antena", "antenna"), ("メロン", "meron", "melon")]),
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

# ---- Kana extras: voiced sounds, combined sounds, small tsu, long mark ----
import kana_extras as X

def _conv(text, katakana):
    return X.to_kata(text) if katakana else text

# Short intro and word lists per unit. Words use only kana taught up to that unit
# (plus all the basic kana of the same script).
H_INTRO = {
 "g": ["Two small marks, called dakuten, turn a sound into its voiced partner. Put them on the K row and you get the G row: ga, gi, gu, ge, go.",
       "The character keeps its shape. Only the two marks are new: か becomes が, き becomes ぎ.",
       "The g is always hard, as in 'go', never soft as in 'giraffe'."],
 "z": ["The same two marks on the S row give the Z row: za, ji, zu, ze, zo.",
       "Two surprises: し becomes じ (ji, as in 'jeep') and す becomes ず (zu).",
       "ぢ and づ sound exactly like じ and ず. They are rare, so we skip them and write じ and ず."],
 "d": ["The T row with dakuten gives the D row. Only three are common: da, de, do.",
       "ち and つ also have voiced forms (ぢ and づ), but they sound like じ and ず and appear in only a few words, so we skip them."],
 "b": ["The H row with dakuten gives the B row: ba, bi, bu, be, bo.",
       "The two marks sit at the top right, the same as on every other voiced character."],
 "p": ["The H row can also take a small circle, called handakuten. That gives the P row: pa, pi, pu, pe, po.",
       "Two marks means B. A circle means P. Check which one before you read."],
 "c1": ["A small や, ゆ or よ after a character in the 'i' column blends the two into one sound. き and ゃ make きゃ (kya).",
        "The small character is about half the size and sits low and to the right. It does not get its own beat: kya is one sound, not ki-ya.",
        "Compare きや (ki-ya, two beats) with きゃ (kya, one beat)."],
 "c2": ["With し and じ the i drops away completely: しゃ is sha, not shi-ya. じゃ is ja.",
        "So the pattern is sha, shu, sho and ja, ju, jo."],
 "c3": ["ち and に also combine: ちゃ is cha, にゃ is nya.",
        "Same rule: the small や, ゆ or よ is half size and joins the sound before it."],
 "c4": ["ひ and み combine the same way: ひゃ is hya, みゃ is mya.",
        "These are less common than the earlier ones, but they turn up in numbers like 100."],
 "c5": ["り and び also combine: りゃ is rya, びゃ is bya.",
        "Remember that Japanese r is a quick tongue tap."],
 "c6": ["The last combined sounds: ぴゃ, ぴゅ, ぴょ (pya, pyu, pyo).",
        "These are rare. You will see them mostly in sound words like ぴょんぴょん (boing, boing)."],
}
H_WORDS = {
 "g": [("かぎ", "kagi", "key"), ("ごはん", "gohan", "rice, a meal"), ("ぎんこう", "ginkou", "bank"),
       ("たまご", "tamago", "egg"), ("えいが", "eiga", "movie"), ("げんき", "genki", "healthy, well")],
 "z": [("かぞく", "kazoku", "family"), ("じかん", "jikan", "time"), ("みず", "mizu", "water"),
       ("すずしい", "suzushii", "cool"), ("かぜ", "kaze", "wind, a cold"), ("ぞう", "zou", "elephant")],
 "d": [("だれ", "dare", "who"), ("でんわ", "denwa", "telephone"), ("どこ", "doko", "where"),
       ("ともだち", "tomodachi", "friend"), ("どうぞ", "douzo", "please, go ahead"), ("おでん", "oden", "oden (a hot-pot dish)")],
 "b": [("かばん", "kaban", "bag"), ("そば", "soba", "buckwheat noodles"), ("ぼく", "boku", "I (a boy or man)"),
       ("たべる", "taberu", "to eat"), ("さびしい", "sabishii", "lonely"), ("ぶた", "buta", "pig")],
 "p": [("ぱん", "pan", "bread"), ("えんぴつ", "enpitsu", "pencil"), ("てんぷら", "tenpura", "tempura"),
       ("さんぽ", "sanpo", "a walk")],
 "c1": [("きょう", "kyou", "today"), ("きゅうり", "kyuuri", "cucumber"), ("ぎゅうにく", "gyuuniku", "beef"),
        ("おきゃく", "okyaku", "guest, customer")],
 "c2": [("しゃしん", "shashin", "photograph"), ("しゅみ", "shumi", "hobby"), ("じしょ", "jisho", "dictionary"),
        ("しょくじ", "shokuji", "meal"), ("じゅう", "juu", "ten")],
 "c3": [("おちゃ", "ocha", "tea"), ("ぎゅうにゅう", "gyuunyuu", "milk"), ("こんにゃく", "konnyaku", "konnyaku (a jelly food)"),
        ("ちゅうごく", "chuugoku", "China")],
 "c4": [("ひゃく", "hyaku", "one hundred"), ("みゃく", "myaku", "pulse")],
 "c5": [("りょこう", "ryokou", "trip"), ("りゅう", "ryuu", "dragon"), ("びょういん", "byouin", "hospital"),
        ("さんびゃく", "sanbyaku", "three hundred")],
 "c6": [("ぴょんぴょん", "pyonpyon", "boing boing (hopping)")],
}
K_INTRO = {
 "g": ["Katakana takes the same two marks (dakuten) as hiragana. Put them on the K row for the G row: ga, gi, gu, ge, go.",
       "The shapes do not change, only the marks are added: カ becomes ガ, キ becomes ギ."],
 "z": ["Two marks on the S row give the Z row: za, ji, zu, ze, zo.",
       "Same surprises as hiragana: シ becomes ジ (ji) and ス becomes ズ (zu).",
       "ヂ and ヅ exist but are rare, so we skip them."],
 "d": ["The T row with two marks gives the D row. Only three are common: da, de, do."],
 "b": ["The H row with two marks gives the B row: ba, bi, bu, be, bo.",
       "These are very common in loanwords: bus, building, button."],
 "p": ["The H row with a small circle gives the P row: pa, pi, pu, pe, po.",
       "Two marks means B, a circle means P."],
 "c1": ["Just as in hiragana, a small ャ, ュ or ョ blends with the character before it. キ and ャ make キャ (kya).",
        "The small character is half size and sits low and to the right. kya is one beat, not two."],
 "c2": ["With シ and ジ the i drops away: シャ is sha and ジャ is ja.",
        "So the pattern is sha, shu, sho and ja, ju, jo."],
 "c3": ["チ and ニ combine too: チャ is cha, ニャ is nya.", "ニュ in ニュース (news) is one you will see often."],
 "c4": ["ヒ and ミ combine: ヒャ is hya, ミャ is mya. These are rare in loanwords."],
 "c5": ["リ and ビ combine: リャ is rya, ビャ is bya."],
 "c6": ["The last ones: ピャ, ピュ, ピョ (pya, pyu, pyo). They are rare. ピュア (pure) is one example."],
}
K_WORDS = {
 "g": [("ガス", "gasu", "gas"), ("ゴルフ", "gorufu", "golf"), ("グラス", "gurasu", "glass"),
       ("ゲスト", "gesuto", "guest"), ("ゴリラ", "gorira", "gorilla"), ("マグロ", "maguro", "tuna")],
 "z": [("ゼロ", "zero", "zero"), ("ジム", "jimu", "gym"), ("カジノ", "kajino", "casino")],
 "d": [("ドア", "doa", "door"), ("デスク", "desuku", "desk"), ("ダンス", "dansu", "dance"),
       ("デザイン", "dezain", "design"), ("メダル", "medaru", "medal")],
 "b": [("バス", "basu", "bus"), ("ビル", "biru", "building"), ("ボタン", "botan", "button"),
       ("バナナ", "banana", "banana"), ("ビザ", "biza", "visa"), ("ベスト", "besuto", "best, vest"),
       ("ズボン", "zubon", "trousers")],
 "p": [("パン", "pan", "bread"), ("ピアノ", "piano", "piano"), ("ペン", "pen", "pen"),
       ("パソコン", "pasokon", "personal computer"), ("ポスト", "posuto", "mailbox"), ("ペンギン", "pengin", "penguin")],
 "c1": [("キャンプ", "kyanpu", "camp")],
 "c2": [("ジャム", "jamu", "jam"), ("シャツ", "shatsu", "shirt"), ("ジャズ", "jazu", "jazz")],
 "c3": [("チョコ", "choko", "chocolate"), ("チャンス", "chansu", "chance")],
 "c4": [],
 "c5": [],
 "c6": [("ピュア", "pyua", "pure")],
}

def _combo_hint(char, rom, katakana):
    big, small = char[0], char[1]
    return f"{big} plus a small {small}: say '{rom}' as one sound, one beat."

def _voiced_hint2(char, rom):
    return f"Same shape as the plain character, with {'a small circle' if rom[0] == 'p' else 'two small marks'} at the top right: '{rom}'."

def build_extra(katakana):
    conv = lambda t: _conv(t, katakana)
    deck = "ja_katakana_extra" if katakana else "ja_hiragana_extra"
    prefix = "k" if katakana else "h"
    intro = K_INTRO if katakana else H_INTRO
    wordsets = K_WORDS if katakana else H_WORDS
    units = []
    for uid, rows in X.VOICED:
        title = {"g": "G sounds", "z": "Z sounds", "d": "D sounds", "b": "B sounds", "p": "P sounds"}[uid]
        units.append(unit(f"{prefix}x_{uid}", title, intro[uid],
                          items(deck, [(r, _voiced_hint2(conv(c), r)) for c, r in rows]),
                          wordsets[uid]))
    for uid, pairs in X.COMBO_UNITS:
        rows = X.combo_rows(pairs)
        title = "Combined sounds: " + ", ".join(conv(b) + conv("ゃ") for b, _ in pairs)
        units.append(unit(f"{prefix}x_{uid}", title, intro[uid],
                          items(deck, [(r, _combo_hint(conv(c), r, katakana)) for c, r in rows]),
                          wordsets[uid]))
    tsu = X.SMALL_TSU
    if katakana:
        units.append(unit("kx_small_tsu", "Small ッ", [
            "A small ッ means: pause briefly, then say the next consonant twice. カット is 'kat-to', with a held beat in the middle.",
            "You do not pronounce ッ by itself. It is silence, one beat long.",
            "It is half the size of ツ and sits low on the line."],
            items(deck, [(tsu[1], "Looks like ツ but half the size and low on the line. Say nothing: hold the next consonant a beat longer.", False)]),
            [("ベッド", "beddo", "bed"), ("カップ", "kappu", "cup"), ("コップ", "koppu", "glass, cup"),
             ("チケット", "chiketto", "ticket"), ("ロケット", "roketto", "rocket"), ("ホット", "hotto", "hot")]))
        units.append(unit("kx_long", "The long mark ー", [
            "In katakana, a long vowel is written with a bar: ー. コーヒー is ko-o-hi-i, with two beats on each long sound.",
            "The bar always points along the writing direction: it is a horizontal line in horizontal text.",
            "Do not confuse ー with the kanji 一 (one). The long mark only ever follows a katakana character."],
            items(deck, [("choon", "A plain horizontal bar after a character. Hold the vowel of the character before it for one extra beat.", False)]),
            [("コーヒー", "koohii", "coffee"), ("ケーキ", "keeki", "cake"), ("タクシー", "takushii", "taxi"),
             ("ビール", "biiru", "beer"), ("ノート", "nooto", "notebook"), ("スープ", "suupu", "soup"),
             ("メール", "meeru", "email"), ("カレー", "karee", "curry"), ("ジュース", "juusu", "juice"),
             ("ニュース", "nyuusu", "news"), ("ギター", "gitaa", "guitar"), ("サッカー", "sakkaa", "soccer"),
             ("シャワー", "shawaa", "shower")]))
    else:
        units.append(unit("hx_small_tsu", "Small っ and long vowels", [
            "A small っ means: pause briefly, then say the next consonant twice. きて is 'kite', but きって is 'kit-te', with a held beat in the middle.",
            "You do not pronounce っ by itself. It is silence, one beat long. It is half the size of つ and sits low on the line.",
            "Long vowels are written by adding another vowel kana: あ after あ-column sounds, い after い or え sounds, う after う or お sounds. おかあさん (mother) has two beats on 'aa'. とうきょう (Tokyo) is 'toh-kyoh'.",
            "Hold a long vowel for about two beats. Short and long vowels change the word: おばさん (aunt) vs おばあさん (grandmother)."],
            items(deck, [(tsu[1], "Looks like つ but half the size and low on the line. Say nothing: hold the next consonant a beat longer.", False)]),
            [("きって", "kitte", "postage stamp"), ("ざっし", "zasshi", "magazine"), ("がっこう", "gakkou", "school"),
             ("ちょっと", "chotto", "a little"), ("まって", "matte", "wait"), ("いっぱい", "ippai", "full"),
             ("おとうさん", "otousan", "father"), ("おねえさん", "oneesan", "older sister"),
             ("とうきょう", "toukyou", "Tokyo"), ("おおきい", "ookii", "big")]))
    return {"id": f"ja_{'katakana' if katakana else 'hiragana'}_extra_course", "lang": "ja", "mode": "reading",
            "title": f"Read: {'katakana' if katakana else 'hiragana'} extras",
            "description": "Voiced sounds, combined sounds and more. Learn the basic characters first.",
            "units": units}

hiragana_extra = build_extra(False)
katakana_extra = build_extra(True)

os.makedirs(OUT, exist_ok=True)
for course in (ja_speaking, hiragana, hiragana_extra, katakana, katakana_extra, zh_speaking, mandarin):
    for u in course["units"]:
        ids = [i["id"] for i in u["items"]]
        assert len(ids) == len(set(ids)), u["id"]
    assert len({u["id"] for u in course["units"]}) == len(course["units"])
    with open(os.path.join(OUT, course["id"] + ".json"), "w", encoding="utf-8") as f:
        json.dump(course, f, ensure_ascii=False, indent=1)
    print(course["id"], [(u["id"], len(u["items"]), len(u["words"])) for u in course["units"]])
