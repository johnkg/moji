import 'package:flutter_test/flutter_test.dart';
import 'package:moji/models/stats.dart';

void main() {
  final day1 = DateTime(2026, 3, 10, 9);

  test('first activity starts a streak of one', () {
    final s = const Stats().earn(20, day1);
    expect(s.xp, 20);
    expect(s.currentStreak(day1), 1);
  });

  test('several activities on one day count once', () {
    final s = const Stats().earn(10, day1).earn(10, day1.add(const Duration(hours: 5)));
    expect(s.xp, 20);
    expect(s.currentStreak(day1), 1);
  });

  test('consecutive days extend the streak', () {
    var s = const Stats().earn(5, day1);
    s = s.earn(5, DateTime(2026, 3, 11, 20));
    s = s.earn(5, DateTime(2026, 3, 12, 8));
    expect(s.currentStreak(DateTime(2026, 3, 12, 9)), 3);
  });

  test('streak works across month and year ends', () {
    final s = const Stats().earn(5, DateTime(2025, 12, 31, 23)).earn(5, DateTime(2026, 1, 1, 1));
    expect(s.currentStreak(DateTime(2026, 1, 1, 2)), 2);
  });

  test('a missed day ends the streak and the next activity restarts it', () {
    final s = const Stats().earn(5, day1).earn(5, DateTime(2026, 3, 11, 9));
    final later = DateTime(2026, 3, 14, 9);
    expect(s.currentStreak(later), 0);
    expect(s.earn(5, later).currentStreak(later), 1);
  });

  test('streak is still alive the day after, before studying', () {
    final s = const Stats().earn(5, day1);
    final next = DateTime(2026, 3, 11, 7);
    expect(s.currentStreak(next), 1);
    expect(s.activeToday(next), isFalse);
  });

  test('levels rise every 100 XP and round-trip through json', () {
    final s = const Stats(xp: 250, streak: 2, lastActiveDay: '2026-03-10');
    expect(s.level, 3);
    expect(s.xpIntoLevel, 50);
    final back = Stats.fromJson(s.toJson());
    expect(back.xp, 250);
    expect(back.streak, 2);
    expect(back.lastActiveDay, '2026-03-10');
  });
}
