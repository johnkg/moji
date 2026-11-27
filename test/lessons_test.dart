import 'dart:io';
import 'dart:math' as math;

import 'package:flutter_test/flutter_test.dart';
import 'package:moji/app_state.dart';
import 'package:moji/lessons/exercise.dart';
import 'package:moji/models/course.dart';
import 'package:moji/models/deck.dart';
import 'package:moji/models/stats.dart';
import 'package:moji/services/course_loader.dart';
import 'package:moji/services/deck_loader.dart';
import 'package:moji/services/progress_store.dart';
import 'package:moji/services/speaker.dart';
import 'package:moji/srs/scheduler.dart';

// Run from the project root: flutter test

class _MemoryStore implements ProgressStore {
  Map<String, CardState> cards = {};
  Set<String> units = {};
  Stats stats = const Stats();

  @override
  Future<Map<String, CardState>> load() async => cards;

  @override
  Future<void> save(Map<String, CardState> progress) async {
    cards = Map.of(progress);
  }

  @override
  Future<Set<String>> loadCompletedUnits() async => units;

  @override
  Future<void> saveCompletedUnits(Set<String> done) async {
    units = Set.of(done);
  }

  @override
  Future<Stats> loadStats() async => stats;

  @override
  Future<void> saveStats(Stats value) async {
    stats = value;
  }
}

class _SilentSpeaker implements Speaker {
  @override
  Future<bool> speak(String text, String lang) async => true;
}

List<Course> _readCourses() {
  return [
    for (final name in courseFiles)
      parseCourse(File('assets/lessons/$name.json').readAsStringSync()),
  ];
}

List<Deck> _readDecks() {
  return [
    for (final name in deckFiles) parseDeck(File('assets/decks/$name.json').readAsStringSync()),
  ];
}

void main() {
  final courses = _readCourses();

  test('every unit explains itself and teaches a small set', () {
    for (final course in courses) {
      expect(course.units, isNotEmpty);
      for (final unit in course.units) {
        expect(unit.intro, isNotEmpty, reason: unit.id);
        // Small tsu and the long mark are taught one at a time, through words.
        final single = unit.id.endsWith('small_tsu') || unit.id.endsWith('_long');
        expect(unit.items.length, inInclusiveRange(single ? 1 : 3, 6), reason: unit.id);
        for (final item in unit.items) {
          expect(item.hint, isNotEmpty, reason: '${unit.id}/${item.id}');
        }
      }
    }
  });

  test('lesson items point at real flashcards with the same text', () {
    final cards = <String, StudyCard>{};
    for (final deck in _readDecks()) {
      for (final card in deck.cards) {
        cards[deck.keyFor(card)] = card;
      }
    }
    for (final course in courses) {
      for (final unit in course.units) {
        for (final item in unit.items) {
          final card = cards[item.card];
          expect(card, isNotNull, reason: '${item.card}');
          expect(card!.front, item.front);
          expect(card.reading, item.reading);
        }
      }
    }
  });

  test('words only use characters taught so far', () {
    for (final course in courses.where((c) => !c.isSpeaking)) {
      final taught = <String>{};
      // Extras courses build on the basic characters of the same script.
      if (course.id.endsWith('_extra_course')) {
        final basic = courses.firstWhere((c) => c.id == course.id.replaceFirst('_extra', ''));
        for (final unit in basic.units) {
          for (final item in unit.items) {
            taught.addAll(item.front.runes.map(String.fromCharCode));
          }
        }
      }
      for (final unit in course.units) {
        // Combined sounds like きゃ teach both of their characters.
        for (final item in unit.items) {
          taught.addAll(item.front.runes.map(String.fromCharCode));
        }
        for (final word in unit.words) {
          for (final rune in word.text.runes) {
            expect(taught, contains(String.fromCharCode(rune)), reason: word.text);
          }
        }
      }
    }
  });

  test('every exercise has its answer among distinct options', () {
    for (final course in courses.where((c) => !c.isSentences)) {
      for (var i = 0; i < course.units.length; i++) {
        final unit = course.units[i];
        final exercises = buildExercises(course, i, math.Random(7));
        final listenable = unit.items.where((it) => it.listen).length;
        expect(exercises.where((e) => !e.isListening && e.kind != ExerciseKind.readWord).length,
            unit.items.length);
        expect(exercises.where((e) => e.isListening).length, listenable);
        for (final exercise in exercises) {
          expect(exercise.options, contains(exercise.answer), reason: exercise.display);
          expect(exercise.options.toSet().length, exercise.options.length);
          expect(exercise.options.length, inInclusiveRange(2, 4));
        }
      }
    }
  });

  test('finishing a unit unlocks the next and seeds flashcard review', () async {
    final store = _MemoryStore();
    final app = AppState(store: store, speaker: _SilentSpeaker());
    app.courses = courses;
    final course = courses.first;
    final now = DateTime.utc(2026, 1, 1, 12);

    expect(app.isUnitUnlocked(course, 0), isTrue);
    expect(app.isUnitUnlocked(course, 1), isFalse);

    await app.completeUnit(course, course.units[0], now);

    expect(app.isUnitDone(course, 0), isTrue);
    expect(app.isUnitUnlocked(course, 1), isTrue);
    expect(app.isUnitUnlocked(course, 2), isFalse);
    expect(store.units, contains(course.keyFor(course.units[0])));
    for (final item in course.units[0].items) {
      final state = store.cards[item.card];
      expect(state, isNotNull);
      expect(state!.isDue(now), isFalse);
      expect(state.isDue(now.add(const Duration(days: 1, minutes: 1))), isTrue);
    }
  });

  test('redoing a unit keeps existing review history', () async {
    final store = _MemoryStore();
    final app = AppState(store: store, speaker: _SilentSpeaker());
    app.courses = courses;
    final course = courses.first;
    final unit = course.units[0];
    final now = DateTime.utc(2026, 1, 1, 12);

    await app.completeUnit(course, unit, now);
    final before = store.cards[unit.items.first.card]!.dueMs;
    await app.completeUnit(course, unit, now.add(const Duration(days: 5)));
    expect(store.cards[unit.items.first.card]!.dueMs, before);
  });

  test('finishing a unit awards XP once at full rate and starts a streak', () async {
    final store = _MemoryStore();
    final app = AppState(store: store, speaker: _SilentSpeaker());
    app.courses = courses;
    final course = courses.first;
    final unit = course.units[0];
    final now = DateTime(2026, 1, 1, 12);

    final first = await app.completeUnit(course, unit, now, firstTryCorrect: 5);
    expect(first, AppState.unitXp + 5 * AppState.exerciseXp);
    expect(store.stats.xp, first);
    expect(app.stats.currentStreak(now), 1);

    final redo = await app.completeUnit(course, unit, now, firstTryCorrect: 5);
    expect(redo, AppState.redoXp + 5 * AppState.exerciseXp);
  });

  test('flashcards give XP unless marked Again', () async {
    final store = _MemoryStore();
    final app = AppState(store: store, speaker: _SilentSpeaker());
    app.decks = _readDecks();
    final deck = app.decks.first;
    final now = DateTime(2026, 1, 1, 12);

    await app.grade(deck, deck.cards[0], Grade.again, now);
    expect(app.stats.xp, 0);
    await app.grade(deck, deck.cards[1], Grade.good, now);
    expect(app.stats.xp, AppState.cardXp);
  });

  test('katakana course covers all 46 basic characters once', () {
    final kata = courses.firstWhere((c) => c.id == 'ja_katakana_course');
    final fronts = [for (final u in kata.units) ...u.items.map((i) => i.front)];
    expect(fronts.length, 46);
    expect(fronts.toSet().length, 46);
  });

  test('listening choices never sound the same as the answer', () {
    for (final course in courses.where((c) => !c.isSpeaking)) {
      final readingOf = <String, String>{
        for (final unit in course.units)
          for (final item in unit.items) item.front: item.reading,
      };
      for (var i = 0; i < course.units.length; i++) {
        for (final exercise in buildExercises(course, i, math.Random(3))) {
          if (exercise.kind != ExerciseKind.hearChar) continue;
          final wrong = exercise.options.where((o) => o != exercise.answer);
          for (final option in wrong) {
            expect(readingOf[option], isNot(exercise.reading), reason: exercise.answer);
          }
        }
      }
    }
  });

  test('speaking courses have a meaning on every phrase', () {
    final speaking = courses.where((c) => c.isSpeaking).toList();
    expect(speaking.map((c) => c.lang).toSet(), {'ja', 'zh'});
    for (final course in speaking) {
      for (final unit in course.units) {
        for (final item in unit.items) {
          expect(item.meaning, isNotEmpty, reason: item.front);
        }
        final meanings = unit.items.map((i) => i.meaning).toSet();
        expect(meanings.length, unit.items.length, reason: unit.id);
      }
      // Wrong choices come from earlier units, so a repeated meaning anywhere
      // in a course could make two options both right.
      final all = [for (final u in course.units) ...u.items.map((i) => i.meaning)];
      expect(all.toSet().length, all.length, reason: course.id);
    }
  });

  test('the Mandarin reading course teaches about a hundred distinct hanzi', () {
    final course = courses.firstWhere((c) => c.id == 'zh_basics_course');
    expect(course.units.length, greaterThanOrEqualTo(18));
    final hanzi = [for (final u in course.units) ...u.items.map((i) => i.front)];
    expect(hanzi.toSet().length, hanzi.length, reason: 'a hanzi is taught twice');
    expect(hanzi.length, greaterThanOrEqualTo(95));
    // Later units build on earlier ones, so compound words should appear.
    final words = [for (final u in course.units) ...u.words];
    expect(words.length, greaterThanOrEqualTo(80));
  });

  test('everyday sentence courses cover both languages with whole sentences', () {
    for (final lang in ['ja', 'zh']) {
      final course = courses.firstWhere((c) => c.id == '${lang}_sentences_course');
      expect(course.isSpeaking, isTrue);
      expect(course.units.length, greaterThanOrEqualTo(6));
      final items = [for (final u in course.units) ...u.items];
      expect(items.length, greaterThanOrEqualTo(30));
      for (final item in items) {
        expect(item.reading, isNotEmpty, reason: item.front);
        expect(item.hint, isNotEmpty, reason: item.front);
      }
    }
  });

  group('sentence reading courses', () {
    final sentenceCourses = courses.where((c) => c.isSentences).toList();

    test('exist for both languages with whole sentences', () {
      expect(sentenceCourses.map((c) => c.lang).toSet(), {'ja', 'zh'});
      for (final course in sentenceCourses) {
        expect(course.units.length, greaterThanOrEqualTo(8));
        final items = [for (final u in course.units) ...u.items];
        expect(items.length, greaterThanOrEqualTo(40));
        final meanings = items.map((i) => i.meaning).toList();
        expect(meanings.toSet().length, meanings.length, reason: '${course.id} repeats a meaning');
      }
    });

    test('word chips join into the sentence and gaps point at a real chip', () {
      for (final course in sentenceCourses) {
        for (final item in [for (final u in course.units) ...u.items]) {
          expect(item.parts.join(), item.front);
          final blank = item.blank;
          if (blank == null) continue;
          expect(blank.part, inInclusiveRange(0, item.parts.length - 1), reason: item.front);
          expect(blank.options, contains(item.parts[blank.part]), reason: item.front);
          expect(blank.options.toSet().length, 4, reason: item.front);
        }
      }
    });

    test('sentences only use characters the learner has already met', () {
      Set<String> runesOf(Iterable<Course> from) => {
            for (final c in from)
              for (final u in c.units)
                for (final i in u.items) ...i.front.runes.map(String.fromCharCode),
          };
      final known = {
        'ja': runesOf(courses.where((c) => c.lang == 'ja' && c.mode == CourseMode.reading)),
        'zh': runesOf(courses.where((c) => c.id == 'zh_basics_course')),
      };
      for (final course in sentenceCourses) {
        final ok = {...known[course.lang]!, '。', '？', '，'};
        for (final item in [for (final u in course.units) ...u.items]) {
          for (final rune in item.front.runes) {
            expect(ok, contains(String.fromCharCode(rune)), reason: item.front);
          }
        }
      }
    });

    test('every unit builds read, fill, hear and arrange exercises with the answer available', () {
      for (final course in sentenceCourses) {
        for (var i = 0; i < course.units.length; i++) {
          final unit = course.units[i];
          final exercises = buildExercises(course, i, math.Random(5));
          int count(ExerciseKind kind) => exercises.where((e) => e.kind == kind).length;
          expect(count(ExerciseKind.readSentence), unit.items.length, reason: unit.id);
          expect(count(ExerciseKind.hearSentence), unit.items.length, reason: unit.id);
          expect(count(ExerciseKind.fillBlank), unit.items.where((it) => it.blank != null).length,
              reason: unit.id);
          expect(count(ExerciseKind.arrange), unit.items.length, reason: unit.id);
          for (final exercise in exercises) {
            if (exercise.kind == ExerciseKind.arrange) {
              final chips = [...exercise.options]..sort();
              final parts = [...exercise.parts]..sort();
              expect(chips, parts, reason: exercise.reveal);
              expect(exercise.parts.join(), exercise.answer);
            } else {
              expect(exercise.options, contains(exercise.answer), reason: exercise.reveal);
              expect(exercise.options.toSet().length, exercise.options.length);
              expect(exercise.options.length, inInclusiveRange(2, 4));
            }
          }
        }
      }
    });
  });
}
