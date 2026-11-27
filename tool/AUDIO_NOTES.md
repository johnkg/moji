# Voice tuning notes (Japanese and Mandarin audio)

Status: shipped. `assets/audio/` holds 815 clips (4.4 MB) made by `tool/gen_audio.py`, and the app plays
them through `RecordedSpeaker` (lib/services/speaker.dart), using the device voice for anything without a clip.

Regenerate after changing lessons or decks: `python3 tool/gen_audio.py --models <folder with the Kokoro files>`
(existing clips are kept; add `--force` to rebuild all). A test fails if any spoken text has no clip.

Voice: Kokoro v1.0 (Apache-2.0) through `kokoro-onnx`, voices `jf_alpha` (Japanese, model speed 1.1)
and `zm_yunxi` (Mandarin, model speed 1.0 then slowed 10% by time-stretching). Text goes through `tool/audio_g2p.py`, then the model is run with
`is_phonemes=True`.

## Measuring

The voice was judged by transcribing generated clips with two recognizers (sherpa-onnx:
SenseVoice, and ReazonSpeech for Japanese) and comparing the phonemes of the transcript
with the intended text. This is only a guide:

- Recognizers write correct homophones in kanji (星し for ほし) and cannot judge very short
  words (ReazonSpeech answers え or うん). Treat 2-mora words with care.
- Isolated single kana cannot be checked this way at all. A person has to listen.

## What helped (Japanese, 256 real words and sentences)

| Change | Effect |
|---|---|
| Generate at the model's own speed 1.1 instead of slowing it (0.85) | 41% to 73% exact. Slowing the model made words worse. |
| Spell the u sound as ɯ instead of ɨ | +3 words on the 79 it touches |
| Spell ら行 with r instead of the tap ɾ | +3 on 49 words (ライス was heard as ナイス) |
| Spell つ as ts instead of ʦ | +1 on 6 words (なつ heard as なぜ) |

Combined: SenseVoice 74% to 76% exact; 80% heard right by at least one recognizer.

## What did not help

Trailing punctuation or spaces, trimming settings, longer clip tails, ʃ/ʧ/ʤ spellings, plain n
or lengthened ん, doubled consonant for っ, l or d for ら行, doubled long vowels, a glottal
stop before initial vowels (this one was very bad: 39 words down to 8).

## Open problems

Words ending in ん or ー sometimes lose the last sound (ごはん, メロン, シャワー). Combined sounds
(ジャズ, シャツ, ちょっと) are the weakest group. Mandarin: tones come from the app's own
pinyin with third-tone sandhi, neutral tones flat, and er spelled as `ɑɻ`.

## Mandarin

Tone sandhi and neutral tones raised exact matches from 16% to about 90%. Speed 0.92 to 1.0
works best; slow audio is made by stretching the finished clip, not by slowing the model.
