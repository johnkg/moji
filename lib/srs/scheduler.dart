import 'dart:math' as math;

enum Grade { again, hard, good, easy }

/// Review state of one card. A card with no stored state is new.
class CardState {
  const CardState({
    required this.reps,
    required this.lapses,
    required this.ease,
    required this.intervalDays,
    required this.dueMs,
  });

  /// Successful reviews in a row.
  final int reps;
  final int lapses;
  final double ease;
  final int intervalDays;

  /// Due time, milliseconds since epoch.
  final int dueMs;

  bool isDue(DateTime now) => dueMs <= now.millisecondsSinceEpoch;

  Map<String, dynamic> toJson() => {
        'r': reps,
        'l': lapses,
        'e': ease,
        'i': intervalDays,
        'd': dueMs,
      };

  factory CardState.fromJson(Map<String, dynamic> json) {
    return CardState(
      reps: (json['r'] as num).toInt(),
      lapses: (json['l'] as num).toInt(),
      ease: (json['e'] as num).toDouble(),
      intervalDays: (json['i'] as num).toInt(),
      dueMs: (json['d'] as num).toInt(),
    );
  }
}

/// Swap point for the algorithm (SM-2 now, FSRS later).
abstract class Scheduler {
  CardState review(CardState? previous, Grade grade, DateTime now);
}

/// SM-2 style scheduler with four answer buttons.
class Sm2Scheduler implements Scheduler {
  const Sm2Scheduler();

  static const double startEase = 2.5;
  static const double minEase = 1.3;

  /// A failed card comes back after this long.
  static const Duration relearnDelay = Duration(minutes: 1);

  @override
  CardState review(CardState? previous, Grade grade, DateTime now) {
    final reps = previous?.reps ?? 0;
    final lapses = previous?.lapses ?? 0;
    final ease = previous?.ease ?? startEase;
    final interval = previous?.intervalDays ?? 0;

    if (grade == Grade.again) {
      return CardState(
        reps: 0,
        lapses: lapses + 1,
        ease: math.max(minEase, ease - 0.2),
        intervalDays: 0,
        dueMs: now.add(relearnDelay).millisecondsSinceEpoch,
      );
    }

    double newEase = ease;
    int newInterval;
    switch (grade) {
      case Grade.hard:
        newEase = math.max(minEase, ease - 0.15);
        newInterval = reps == 0 ? 1 : math.max(interval + 1, (interval * 1.2).round());
        break;
      case Grade.easy:
        newEase = ease + 0.15;
        newInterval = reps == 0 ? 4 : math.max(interval + 1, (interval * ease * 1.3).round());
        break;
      case Grade.good:
      case Grade.again:
        if (reps == 0) {
          newInterval = 1;
        } else if (reps == 1) {
          newInterval = math.max(interval + 1, 3);
        } else {
          newInterval = math.max(interval + 1, (interval * ease).round());
        }
        break;
    }

    return CardState(
      reps: reps + 1,
      lapses: lapses,
      ease: newEase,
      intervalDays: newInterval,
      dueMs: now.add(Duration(days: newInterval)).millisecondsSinceEpoch,
    );
  }
}
