# Moji

Learn to read and speak basic Japanese and Mandarin. Flutter, web-first.

**Status: v0.5. Compiled, tested and deployed by CI. Katakana, XP/streak and writing practice are new and not yet run by hand.**

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

## What v0.5 does

Each language has two paths. Units unlock in order inside each path.

- **Speak** (sound first): phrases shown in romaji or pinyin, native text small. Exercises: see the phrase and pick its meaning, hear it and pick its meaning. Japanese and Mandarin: 3 units each, 12 phrases each.
- **Read**: a short explanation, each new character with a memory hint and audio, then read it, hear it, and read words built from it.
  - Japanese: all 46 hiragana and all 46 katakana, 10 units each.
  - Mandarin: tones, numbers 1 to 10, and 20 more hanzi, 7 units.
- Wrong answers come back once. Finishing a unit puts its items into flashcard review, due the next day.
- Flashcard decks with spaced repetition (SM-2 style, Again / Hard / Good / Easy)
- Audio through device or browser text-to-speech
- **Write** (pencil button on kana units): for each character, watch the strokes in order, trace over a guide, then write from memory. The check is loose: each stroke must start and end near the right place and go the right way. 5 XP per character written from memory.
- XP, levels and a daily streak. A unit gives 20 XP (5 on a redo) plus 2 per exercise right first try; a flashcard not marked Again gives 2. A level is 100 XP. The streak counts days in a row with any activity.
- Progress saved on device

## Layout

- `assets/lessons/*.json` - courses and units. Edit `tool/gen_lessons.py`, then `python3 tool/gen_lessons.py`.
- `assets/decks/*.json` - flashcards. Edit `tool/gen_decks.py`, then `python3 tool/gen_decks.py`.
- `lib/lessons/exercise.dart` - builds the exercises for a unit.
- `lib/srs/scheduler.dart` - `Scheduler` interface; swap SM-2 for FSRS here.
- `lib/services/progress_store.dart` - `ProgressStore` interface; swap for SQLite or sync here.
- `lib/services/speaker.dart` - `Speaker` interface; swap for recorded audio or cloud TTS here.

## Content and licences

All deck content is hand-written for this project.

**KanjiVG** (stroke order of hiragana and katakana, `assets/strokes/ja_kana.json`): Copyright (C) 2009-2011 Ulrich Apel, licensed CC BY-SA 3.0, http://kanjivg.tagaini.net. The file is a modified version (paths sampled into points) and stays under the same licence. Regenerate with `tool/gen_strokes.py`.

When adding CC-CEDICT, JMdict, KanjiVG or Tatoeba data, record the licence here.

## Next

1. Hiragana and katakana extras: dakuten (が, ざ), small ゃ ゅ ょ, small っ, long vowels
2. Simple sentences: は, です, の
3. Stroke order for Mandarin hanzi (Make Me a Hanzi data)
4. Speech check (say it aloud)
