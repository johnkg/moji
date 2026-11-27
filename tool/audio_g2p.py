"""Text to Kokoro phonemes for Mandarin and Japanese.

Mandarin: the app's own pinyin (with tone marks) is the source of truth for tones,
so polyphonic characters are always right. We then apply third-tone sandhi
(nǐ hǎo is said ní hǎo) and keep neutral tones. Japanese: misaki's kana to phoneme
step. Needs: misaki[zh,ja], pypinyin, jieba, cn2an.
"""
import re
from pypinyin import lazy_pinyin, Style
from pypinyin.contrib.tone_convert import to_tone3, to_normal
from pypinyin.pinyin_dict import pinyin_dict
from misaki import zh as _zh, ja as _ja

_HANZI = re.compile(r'[一-鿿]')
_SYLLABLES = {to_normal(s) for v in pinyin_dict.values() for s in v.split(',')}
_SYLLABLES |= {'er', 'ng', 'hm', 'm', 'n'}
_ZH = _zh.ZHG2P()
_JA = _ja.JAG2P()

def split_pinyin(token):
    """'gāoxìng' -> ['gāo', 'xìng']. Apostrophes force a split (wǎn'ān)."""
    out = []
    for chunk in token.split("'"):
        i = 0
        while i < len(chunk):
            for j in range(min(len(chunk), i + 6), i, -1):
                if to_normal(chunk[i:j]) in _SYLLABLES:
                    out.append(chunk[i:j]); i = j; break
            else:
                raise ValueError('cannot split pinyin: ' + token)
    return out

def _tone(syl):
    t = to_tone3(syl, neutral_tone_with_five=True)
    return t[:-1], int(t[-1]) if t[-1].isdigit() else 5

def zh_phonemes(text, reading, neutral='→'):
    """Phonemes for hanzi [text] said with the pinyin [reading] (tone marks)."""
    reading = reading.lower()  # proper nouns like Mǎkè
    clauses = [c for c in re.split(r'[,，、.。?？!！]', reading) if c.strip()]
    hanzi = _HANZI.findall(text)
    words = []   # list of lists of (base, tone) per clause
    for clause in clauses:
        words.append([[_tone(s) for s in split_pinyin(tok)] for tok in clause.split()])
    total = sum(len(w) for c in words for w in c)
    if total != len(hanzi):
        raise ValueError(f'{text!r}: {len(hanzi)} hanzi but {total} syllables in {reading!r}')
    out = []
    for clause in words:
        flat = [s for w in clause for s in w]
        for i in range(len(flat) - 1):          # third-tone sandhi, left to right
            if flat[i][1] == 3 and flat[i + 1][1] == 3:
                flat[i] = (flat[i][0], 2)
        k = 0
        rendered = []
        for w in clause:
            rendered.append(''.join(_ZH.py2ipa(f'{b}{t}') + (neutral if t == 5 else '') for b, t in flat[k:k + len(w)]))
            k += len(w)
        out.append(' '.join(rendered))
    # 'ɚ' (er) is heard as an English word by the model; 'ɑɻ' comes out as the Mandarin sound.
    return ' , '.join(out).replace(chr(815), '').replace('ɚ', 'ɑɻ')

def ja_phonemes(text):
    # misaki spells some u sounds with 'ɨ'; the plain Japanese u 'ɯ' was recognised more often (79 words: +3).
    # Spelling fixes, each kept only after it won on the words it touches (see tool/AUDIO_NOTES.md):
    # 'ɨ'->'ɯ' (plain u), 'ɾ'->'r' (ら行 was heard as な), 'ʦ'->'ts' (つ was heard as ず).
    return _JA(text).replace('ɨ', 'ɯ').replace('ɾ', 'r').replace('ʦ', 'ts')
