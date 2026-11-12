import 'package:flutter/foundation.dart';

import 'models/deck.dart';
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

  List<Deck> decks = [];
  Map<String, CardState> progress = {};

  Future<void> load() async {
    decks = await loadDecks();
    progress = await store.load();
    notifyListeners();
  }

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
