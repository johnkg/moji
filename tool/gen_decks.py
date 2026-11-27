"""Regenerates assets/decks/*.json. Content is hand-written (no third-party data)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kana_extras as X
import sentences as S
import zh_extra as ZX
import read_sentences as RS
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'decks')
ROMAJI = ("a i u e o ka ki ku ke ko sa shi su se so ta chi tsu te to na ni nu ne no "
          "ha hi fu he ho ma mi mu me mo ya yu yo ra ri ru re ro wa wo n").split()
HIRA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
KATA = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
assert len(ROMAJI) == len(HIRA) == len(KATA) == 46

def kana(chars):
    return [{"id": r, "front": c, "reading": r, "meaning": ""} for c, r in zip(chars, ROMAJI)]

def rows(items):
    return [{"id": str(i + 1), "front": f, "reading": r, "meaning": m} for i, (f, r, m) in enumerate(items)]

def extras(katakana):
    conv = X.to_kata if katakana else (lambda t: t)
    cards = [{"id": r, "front": conv(c), "reading": r, "meaning": ""} for c, r in X.all_voiced() + X.all_combos()]
    t = X.SMALL_TSU
    cards.append({"id": t[1], "front": conv(t[0]), "reading": t[2], "meaning": t[3]})
    if katakana:
        m = X.LONG_MARK
        cards.append({"id": m[1], "front": m[0], "reading": m[2], "meaning": m[3]})
    return cards

decks = [
 {"id": "ja_hiragana", "lang": "ja", "title": "Hiragana", "description": "The 46 basic hiragana.", "cards": kana(HIRA)},
 {"id": "ja_katakana", "lang": "ja", "title": "Katakana", "description": "The 46 basic katakana.", "cards": kana(KATA)},
 {"id": "ja_hiragana_extra", "lang": "ja", "title": "Hiragana extras", "description": "Voiced sounds, combined sounds and small っ.", "cards": extras(False)},
 {"id": "ja_katakana_extra", "lang": "ja", "title": "Katakana extras", "description": "Voiced sounds, combined sounds, small ッ and the long mark.", "cards": extras(True)},
 {"id": "ja_phrases", "lang": "ja", "title": "First phrases", "description": "Survival phrases.", "cards": rows([
  ("こんにちは", "konnichiwa", "hello"), ("ありがとう", "arigatou", "thank you"),
  ("すみません", "sumimasen", "excuse me / sorry"), ("はい", "hai", "yes"), ("いいえ", "iie", "no"),
  ("おはよう", "ohayou", "good morning"), ("こんばんは", "konbanwa", "good evening"),
  ("さようなら", "sayounara", "goodbye"), ("おねがいします", "onegaishimasu", "please"),
  ("わかりません", "wakarimasen", "I don't understand"), ("いくらですか", "ikura desu ka", "how much is it?"),
  ("おいしい", "oishii", "delicious")])},
 {"id": "ja_sentences", "lang": "ja", "title": "Everyday sentences", "description": "Introductions, questions, ordering, directions.", "cards": [
  {"id": i, "front": t, "reading": r, "meaning": m} for i, t, r, m, _, _ in S.flat(S.JA)]},
 {"id": "zh_sentences", "lang": "zh", "title": "Everyday sentences", "description": "Introductions, questions, ordering, directions.", "cards": [
  {"id": i, "front": t, "reading": r, "meaning": m} for i, t, r, m, _, _ in S.flat(S.ZH)]},
 {"id": "ja_read_sentences", "lang": "ja", "title": "Reading sentences", "description": "Sentences read in kana: particles, questions, verbs.", "cards": [
  {"id": i, "front": t, "reading": r, "meaning": m} for i, t, r, m, _, _, _, _ in RS.flat(RS.JA)]},
 {"id": "zh_read_sentences", "lang": "zh", "title": "Reading sentences", "description": "Sentences read in hanzi: 是, 吗, 不, 很, 的.", "cards": [
  {"id": i, "front": t, "reading": r, "meaning": m} for i, t, r, m, _, _, _, _ in RS.flat(RS.ZH)]},
 {"id": "zh_tones", "lang": "zh", "title": "Tones", "description": "The four tones plus neutral, on the syllable ma.", "cards": rows([
  ("妈", "mā", "mother (1st tone: high and flat)"), ("麻", "má", "hemp (2nd tone: rising)"),
  ("马", "mǎ", "horse (3rd tone: dips low, then rises)"), ("骂", "mà", "to scold (4th tone: sharp fall)"),
  ("吗", "ma", "question particle (neutral tone: light, short)")])},
 {"id": "zh_hanzi", "lang": "zh", "title": "First hanzi", "description": "Common characters with pinyin.", "cards": rows([
  ("一", "yī", "one"), ("二", "èr", "two"), ("三", "sān", "three"), ("四", "sì", "four"), ("五", "wǔ", "five"),
  ("六", "liù", "six"), ("七", "qī", "seven"), ("八", "bā", "eight"), ("九", "jiǔ", "nine"), ("十", "shí", "ten"),
  ("人", "rén", "person"), ("大", "dà", "big"), ("小", "xiǎo", "small"), ("我", "wǒ", "I / me"), ("你", "nǐ", "you"),
  ("他", "tā", "he / him"), ("她", "tā", "she / her"), ("好", "hǎo", "good"), ("是", "shì", "to be"), ("不", "bù", "not"),
  ("有", "yǒu", "to have"), ("水", "shuǐ", "water"), ("火", "huǒ", "fire"), ("山", "shān", "mountain"),
  ("日", "rì", "sun / day"), ("月", "yuè", "moon / month"), ("中", "zhōng", "middle"), ("国", "guó", "country"),
  ("吃", "chī", "to eat"), ("喝", "hē", "to drink")] + [(h, p, m) for _, h, p, m, _, _ in ZX.flat()])},
 {"id": "zh_phrases", "lang": "zh", "title": "First phrases", "description": "Survival phrases.", "cards": rows([
  ("你好", "nǐ hǎo", "hello"), ("谢谢", "xièxie", "thank you"), ("不客气", "bú kèqi", "you're welcome"),
  ("对不起", "duìbuqǐ", "sorry"), ("没关系", "méi guānxi", "it's okay"), ("再见", "zàijiàn", "goodbye"),
  ("早上好", "zǎoshang hǎo", "good morning"), ("请", "qǐng", "please"), ("我不懂", "wǒ bù dǒng", "I don't understand"),
  ("多少钱", "duōshao qián", "how much is it?"), ("是", "shì", "yes / it is"), ("不是", "bú shì", "no / it is not")])},
]
os.makedirs(OUT, exist_ok=True)
for d in decks:
    ids = [c["id"] for c in d["cards"]]
    assert len(ids) == len(set(ids)), d["id"]
    with open(os.path.join(OUT, d["id"] + ".json"), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print(d["id"], len(d["cards"]))
