import 'dart:io';
import 'dart:math' as math;

import 'package:flutter_test/flutter_test.dart';
import 'package:moji/app_state.dart';
import 'package:moji/lessons/exercise.dart';
import 'package:moji/models/course.dart';
import 'package:moji/models/deck.dart';
import 'package:moji/services/course_loader.dart';
import 'package:moji/services/deck_loader.dart';
import 'package:moji/services/progress_store.dart';
import 'package:moji/services/speaker.dart';
import 'package:moji/srs/scheduler.dart';

// Run from the project root: flutter test

class _MemoryStore implements ProgressStore {
  Map<String, CardState> cards = {};
  Set<String> units = {};

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
        expect(unit.items.length, inInclusiveRange(3, 6), reason: unit.id);
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
    for (final course in courses) {
      final taught = <String>{};
      for (final unit in course.units) {
        taught.addAll(unit.items.map((i) => i.front));
        for (final word in unit.words) {
          for (final rune in word.text.runes) {
            expect(taught, contains(String.fromCharCode(rune)), reason: word.text);
          }
        }
      }
    }
  });

  test('every exercise has its answer among distinct options', () {
    for (final course in courses) {
      for (var i = 0; i < course.units.length; i++) {
        final unit = course.units[i];
        final exercises = buildExercises(course, i, math.Random(7));
        final reads = exercises.where((e) => e.kind == ExerciseKind.readChar).length;
        final hears = exercises.where((e) => e.kind == ExerciseKind.hearChar).length;
        expect(reads, unit.items.length);
        expect(hears, unit.items.length);
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
}
