# Moji

Learn to read and speak basic Japanese and Mandarin. Flutter, web-first.

**Status: v0.2. Compiled, tested and deployed by CI. Lesson flow not yet tried by hand on a device.**

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

## What v0.2 does

- **Lessons** that teach before they test: a short explanation, each new character with a memory hint and audio, then mixed exercises (read it, hear it, read words built from it). Wrong answers come back once.
- Units unlock in order. So far: hiragana vowels, K row, S row; Mandarin tones, numbers 1 to 5, numbers 6 to 10.
- Finishing a unit puts its characters into flashcard review, due the next day.
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

1. Remaining hiragana rows, katakana, more hanzi units
2. Stroke order tracing
3. Speech check (say it aloud)
