# Moji

Learn to read and speak basic Japanese and Mandarin. Flutter, web-first.

**Status: v0.3. Compiled, tested and deployed by CI. Lesson flow not yet tried by hand on a device.**

## First run

```
cd moji
flutter create . --platforms=web,android   # adds web/ and android/ folders, keeps lib/
flutter pub get
flutter test
flutter run -d chrome
```

## Deployment

Every push to `main` runs `.github/workflows/pages.yml`: analyze, test, build web, deploy to GitHub Pages.

One-time setup: repo Settings > Pages > Source: **GitHub Actions**. Free Pages needs a public repo.

Site: https://johnkg.github.io/moji/

## What v0.3 does

Each language has two paths. Units unlock in order inside each path.

- **Speak** (sound first): phrases shown in romaji or pinyin, native text small. Exercises: see the phrase and pick its meaning, hear it and pick its meaning. Japanese and Mandarin: 3 units each, 12 phrases each.
- **Read**: a short explanation, each new character with a memory hint and audio, then read it, hear it, and read words built from it.
  - Japanese: all 46 hiragana in 10 units.
  - Mandarin: tones, numbers 1 to 10, and 20 more hanzi, 7 units.
- Wrong answers come back once. Finishing a unit puts its items into flashcard review, due the next day.
- Flashcard decks with spaced repetition (SM-2 style, Again / Hard / Good / Easy)
- Audio through device or browser text-to-speech
- Progress saved on device

## Layout

- `assets/lessons/*.json` - courses and units. Edit `tool/gen_lessons.py`, then `python3 tool/gen_lessons.py`.
- `assets/decks/*.json` - flashcards. Edit `tool/gen_decks.py`, then `python3 tool/gen_decks.py`.
- `lib/lessons/exercise.dart` - builds the exercises for a unit.
- `lib/srs/scheduler.dart` - `Scheduler` interface; swap SM-2 for FSRS here.
- `lib/services/progress_store.dart` - `ProgressStore` interface; swap for SQLite or sync here.
- `lib/services/speaker.dart` - `Speaker` interface; swap for recorded audio or cloud TTS here.

## Content and licences

All deck content is hand-written for this project. No third-party data yet.
When adding CC-CEDICT, JMdict, KanjiVG or Tatoeba data, record the licence here.

## Next

1. Katakana path
2. Hiragana extras: dakuten (が, ざ), small ゃ ゅ ょ, small っ, long vowels
3. Simple sentences: は, です, の
4. Stroke order tracing
5. Speech check (say it aloud)
