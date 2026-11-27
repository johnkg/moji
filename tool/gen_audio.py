"""Generates the recorded voice clips in assets/audio/ and their manifest.

Voice: Kokoro v1.0 (Apache-2.0) through kokoro-onnx. Japanese: jf_alpha at the model's speed 1.1.
Mandarin: zm_yunxi at speed 1.0, then slowed 10% by time-stretching (slowing the model itself
made words worse; see tool/AUDIO_NOTES.md). Text goes through tool/audio_g2p.py.

Needs: kokoro-onnx, misaki[zh,ja], pyopenjtalk-plus, pypinyin, jieba, cn2an, soundfile, numpy, ffmpeg
and the Kokoro files kokoro-v1.0.onnx and voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx,
release model-files-v1.0).

    python3 tool/gen_audio.py --models <folder with the two Kokoro files> [--force]

Every text the app speaks gets a clip: all flashcards and all lesson words. The app looks
clips up by (language, text) in assets/audio/manifest.json and falls back to the device
voice for anything missing.
"""
import argparse, glob, hashlib, json, os, subprocess, sys, tempfile
import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ASSETS = os.path.join(HERE, '..', 'assets')
OUT = os.path.join(ASSETS, 'audio')
SR = 24000
# A lone small tsu or long mark has no sound of its own.
SKIP = {'ー', 'っ', 'ッ'}
VOICE = {'ja': ('jf_alpha', 1.1, 1.0), 'zh': ('zm_yunxi', 1.0, 0.9)}   # voice, model speed, stretch

def corpus():
    """Unique (lang, text, reading) the app speaks."""
    seen, out = set(), []
    def add(lang, text, reading):
        if (lang, text) in seen or not text.strip() or text in SKIP: return
        seen.add((lang, text)); out.append((lang, text, reading))
    for f in sorted(glob.glob(os.path.join(ASSETS, 'decks', '*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        for c in d['cards']: add(d['lang'], c['front'], c['reading'])
    for f in sorted(glob.glob(os.path.join(ASSETS, 'lessons', '*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        for u in d['units']:
            for w in u.get('words', []): add(d['lang'], w['text'], w['reading'])
            for i in u['items']: add(d['lang'], i['front'], i['reading'])
    return out

def clip_id(lang, text):
    return hashlib.md5(f'{lang}|{text}'.encode()).hexdigest()[:10]

def tidy(a):
    """Trim silence, even out loudness, add short fades and a little padding."""
    a = a.astype(np.float32)
    idx = np.where(np.abs(a) > 10 ** (-45 / 20))[0]
    if len(idx): a = a[max(0, idx[0] - int(0.03 * SR)): idx[-1] + int(0.06 * SR)]
    a = a * (10 ** (-20 / 20) / (np.sqrt(np.mean(a ** 2)) + 1e-9))
    peak = np.max(np.abs(a))
    if peak > 0.89: a = a * (0.89 / peak)
    f = int(0.01 * SR); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
    return np.concatenate([np.zeros(int(.08 * SR), np.float32), a, np.zeros(int(.12 * SR), np.float32)])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--models', required=True)
    ap.add_argument('--force', action='store_true')
    args = ap.parse_args()
    import audio_g2p as g
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(args.models, 'kokoro-v1.0.onnx'), os.path.join(args.models, 'voices-v1.0.bin'))
    items = corpus()
    manifest = {'ja': {}, 'zh': {}}
    failed, made, kept = [], 0, 0
    for lang in manifest: os.makedirs(os.path.join(OUT, lang), exist_ok=True)
    for n, (lang, text, reading) in enumerate(items):
        cid = clip_id(lang, text)
        path = os.path.join(OUT, lang, cid + '.mp3')
        if os.path.exists(path) and not args.force:
            manifest[lang][text] = cid; kept += 1; continue
        voice, speed, stretch = VOICE[lang]
        try:
            ph = g.ja_phonemes(text) if lang == 'ja' else g.zh_phonemes(text, reading)
            audio = tidy(k.create(ph, voice=voice, speed=speed, lang='ja', is_phonemes=True)[0])
            with tempfile.NamedTemporaryFile(suffix='.wav') as tmp:
                sf.write(tmp.name, audio, SR)
                cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-i', tmp.name]
                if stretch != 1.0: cmd += ['-filter:a', f'atempo={stretch}']
                subprocess.run(cmd + ['-ac', '1', '-codec:a', 'libmp3lame', '-b:a', '48k', path], check=True)
            manifest[lang][text] = cid; made += 1
        except Exception as e:   # leave it out: the app falls back to the device voice
            failed.append((lang, text, f'{type(e).__name__}: {e}'))
        if n % 100 == 0: print(f'{n}/{len(items)}', flush=True)
    with open(os.path.join(OUT, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump({'version': 1, 'clips': manifest}, f, ensure_ascii=False, sort_keys=True, indent=0)
    size = sum(os.path.getsize(p) for p in glob.glob(os.path.join(OUT, '*', '*.mp3')))
    print(f'made {made}, kept {kept}, failed {len(failed)}; ja {len(manifest["ja"])}, zh {len(manifest["zh"])}; {size / 1e6:.1f} MB')
    for lang, text, err in failed: print('FAILED', lang, text, err)

if __name__ == '__main__':
    main()
