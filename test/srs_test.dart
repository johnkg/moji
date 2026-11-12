import 'package:flutter_test/flutter_test.dart';
import 'package:moji/srs/scheduler.dart';

void main() {
  const scheduler = Sm2Scheduler();
  final now = DateTime.utc(2026, 1, 1, 12);

  int daysUntilDue(CardState state) {
    return DateTime.fromMillisecondsSinceEpoch(state.dueMs, isUtc: true).difference(now).inDays;
  }

  test('new card graded good is due tomorrow', () {
    final state = scheduler.review(null, Grade.good, now);
    expect(state.reps, 1);
    expect(state.intervalDays, 1);
    expect(daysUntilDue(state), 1);
  });

  test('new card graded easy skips ahead four days', () {
    final state = scheduler.review(null, Grade.easy, now);
    expect(state.intervalDays, 4);
    expect(state.ease, greaterThan(Sm2Scheduler.startEase));
  });

  test('good answers grow the interval each time', () {
    CardState? state;
    var last = 0;
    for (var i = 0; i < 5; i++) {
      state = scheduler.review(state, Grade.good, now);
      expect(state.intervalDays, greaterThan(last));
      last = state.intervalDays;
    }
    expect(last, greaterThan(14));
  });

  test('again resets reps, counts a lapse and comes back within minutes', () {
    var state = scheduler.review(null, Grade.good, now);
    state = scheduler.review(state, Grade.good, now);
    state = scheduler.review(state, Grade.again, now);
    expect(state.reps, 0);
    expect(state.lapses, 1);
    expect(state.intervalDays, 0);
    expect(state.isDue(now), isFalse);
    expect(state.isDue(now.add(const Duration(minutes: 2))), isTrue);
  });

  test('ease never drops below the floor', () {
    CardState? state;
    for (var i = 0; i < 20; i++) {
      state = scheduler.review(state, Grade.again, now);
    }
    expect(state!.ease, Sm2Scheduler.minEase);
  });

  test('state survives a JSON round trip', () {
    final state = scheduler.review(null, Grade.hard, now);
    final copy = CardState.fromJson(state.toJson());
    expect(copy.reps, state.reps);
    expect(copy.lapses, state.lapses);
    expect(copy.ease, state.ease);
    expect(copy.intervalDays, state.intervalDays);
    expect(copy.dueMs, state.dueMs);
  });
}
