import 'package:flutter/foundation.dart';

import 'models/course.dart';
import 'models/deck.dart';
import 'services/course_loader.dart';
import 'services/deck_loader.dart';
import 'services/progress_store.dart';
import 'services/speaker.dart';
import 'srs/scheduler.dart';

class AppState extends ChangeNotifier {
  AppState({
    required this.store,
    required this.speaker,
    this.scheduler = const Sm2Scheduler(),
  });

  final ProgressStore store;
  final Speaker speaker;
  final Scheduler scheduler;

  List<Course> courses = [];
  List<Deck> decks = [];
  Map<String, CardState> progress = {};
  Set<String> completedUnits = {};

  Future<void> load() async {
    courses = await loadCourses();
    decks = await loadDecks();
    progress = await store.load();
    completedUnits = await store.loadCompletedUnits();
    notifyListeners();
  }

  // Lessons

  bool isUnitDone(Course course, int unitIndex) {
    return completedUnits.contains(course.keyFor(course.units[unitIndex]));
  }

  /// The first unit is always open; the rest open one at a time.
  bool isUnitUnlocked(Course course, int unitIndex) {
    return unitIndex == 0 || isUnitDone(course, unitIndex - 1);
  }

  /// Marks the unit finished and puts its characters into flashcard review,
  /// due tomorrow. Cards that already have review history are left alone.
  Future<void> completeUnit(Course course, LessonUnit unit, DateTime now) async {
    completedUnits.add(course.keyFor(unit));
    for (final item in unit.items) {
      final key = item.card;
      if (key != null && !progress.containsKey(key)) {
        progress[key] = scheduler.review(null, Grade.good, now);
      }
    }
    notifyListeners();
    await store.saveCompletedUnits(completedUnits);
    await store.save(progress);
  }

  // Flashcards

  bool isNew(Deck deck, StudyCard card) => !progress.containsKey(deck.keyFor(card));

  int newCount(Deck deck) => deck.cards.where((c) => isNew(deck, c)).length;

  int dueCount(Deck deck, DateTime now) {
    return deck.cards.where((c) {
      final state = progress[deck.keyFor(c)];
      return state != null && state.isDue(now);
    }).length;
  }

  /// Due reviews first, then up to [maxNew] new cards in deck order.
  List<StudyCard> buildSession(Deck deck, DateTime now, {int maxNew = 10}) {
    final due = <StudyCard>[];
    final fresh = <StudyCard>[];
    for (final card in deck.cards) {
      final state = progress[deck.keyFor(card)];
      if (state == null) {
        if (fresh.length < maxNew) fresh.add(card);
      } else if (state.isDue(now)) {
        due.add(card);
      }
    }
    return [...due, ...fresh];
  }

  Future<void> grade(Deck deck, StudyCard card, Grade grade, DateTime now) async {
    final key = deck.keyFor(card);
    progress[key] = scheduler.review(progress[key], grade, now);
    notifyListeners();
    await store.save(progress);
  }
}
