/// XP, level and daily streak. Pure data: no clock of its own, so it is easy to test.
class Stats {
  const Stats({this.xp = 0, this.streak = 0, this.lastActiveDay});

  static const int xpPerLevel = 100;

  final int xp;

  /// Days in a row with some activity, as of [lastActiveDay].
  final int streak;

  /// Local calendar day of the last activity, as yyyy-mm-dd.
  final String? lastActiveDay;

  int get level => xp ~/ xpPerLevel + 1;
  int get xpIntoLevel => xp % xpPerLevel;

  static String dayKey(DateTime day) {
    final m = day.month.toString().padLeft(2, '0');
    final d = day.day.toString().padLeft(2, '0');
    return '${day.year}-$m-$d';
  }

  /// The streak to show now. It is still alive if the last activity was today
  /// or yesterday; after a missed day it has ended.
  int currentStreak(DateTime now) {
    final last = lastActiveDay;
    if (last == null) return 0;
    final today = dayKey(now);
    final yesterday = dayKey(DateTime(now.year, now.month, now.day - 1));
    return (last == today || last == yesterday) ? streak : 0;
  }

  /// True when something was already done today.
  bool activeToday(DateTime now) => lastActiveDay == dayKey(now);

  /// Adds [amount] XP for activity at [now] and updates the streak.
  Stats earn(int amount, DateTime now) {
    final today = dayKey(now);
    final int nextStreak;
    if (lastActiveDay == today) {
      nextStreak = streak;
    } else {
      nextStreak = currentStreak(now) + 1;
    }
    return Stats(xp: xp + amount, streak: nextStreak, lastActiveDay: today);
  }

  Map<String, dynamic> toJson() => {'xp': xp, 'streak': streak, 'last': lastActiveDay};

  factory Stats.fromJson(Map<String, dynamic> json) {
    return Stats(
      xp: (json['xp'] as num?)?.toInt() ?? 0,
      streak: (json['streak'] as num?)?.toInt() ?? 0,
      lastActiveDay: json['last'] as String?,
    );
  }
}
