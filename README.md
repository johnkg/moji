# Moji

Learn to read and speak basic Japanese and Mandarin. Flutter, web-first.

**Status: v0.1, written without a Flutter SDK. Not yet compiled or run.**

## First run

```
cd moji
flutter create . --platforms=web,android   # adds web/ and android/ folders, keeps lib/
flutter pub get
flutter test
flutter run -d chrome
```

## What v0.1 does

- 6 decks: hiragana, katakana, Japanese phrases, Mandarin tones, 30 hanzi, Mandarin phrases
- Spaced repetition (SM-2 style, Again / Hard / Good / Easy)
- Audio through device or browser text-to-speech
- Browse chart per deck, tap to hear
- Progress saved on device

## Layout

- `assets/decks/*.json` - content. Edit `tool/gen_decks.py`, then `python3 tool/gen_decks.py`.
- `lib/srs/scheduler.dart` - `Scheduler` interface; swap SM-2 for FSRS here.
- `lib/services/progress_store.dart` - `ProgressStore` interface; swap for SQLite or sync here.
- `lib/services/speaker.dart` - `Speaker` interface; swap for recorded audio or cloud TTS here.

## Content and licences

All deck content is hand-written for this project. No third-party data yet.
When adding CC-CEDICT, JMdict, KanjiVG or Tatoeba data, record the licence here.

## Next

1. Stroke order tracing
2. Speech check (say it aloud)
3. Multiple-choice quiz mode
4. More hanzi and kanji
