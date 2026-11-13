import 'dart:math' as math;

import '../models/course.dart';

enum ExerciseKind {
  /// See a character, pick its reading.
  readChar,

  /// Hear a character, pick the character.
  hearChar,

  /// See a word, pick its reading.
  readWord,
}

class Exercise {
  const Exercise({
    required this.kind,
    required this.question,
    required this.display,
    required this.reading,
    required this.options,
    required this.answer,
    required this.reveal,
  });

  final ExerciseKind kind;
  final String question;

  /// Native text. Spoken aloud; hidden on screen for [ExerciseKind.hearChar].
  final String display;
  final String reading;
  final List<String> options;
  final String answer;

  /// Shown after answering, e.g. "あい = ai (love)".
  final String reveal;
}

/// Up to three wrong choices plus [answer], shuffled. Wrong choices come from
/// [near] first (same unit), then [far] (earlier units).
List<String> _options(
  String answer,
  Iterable<String> near,
  Iterable<String> far,
  math.Random rng,
) {
  final picks = <String>[];
  for (final source in <Iterable<String>>[near, far]) {
    final candidates = source.where((s) => s != answer && !picks.contains(s)).toSet().toList();
    candidates.shuffle(rng);
    for (final candidate in candidates) {
      if (picks.length < 3) picks.add(candidate);
    }
  }
  final all = <String>[...picks, answer];
  all.shuffle(rng);
  return all;
}

String _reveal(String text, String reading, String meaning) {
  return meaning.isEmpty ? '$text = $reading' : '$text = $reading ($meaning)';
}

/// Exercises for one unit: read each character, then hear each character,
/// then read words built from what has been taught so far.
List<Exercise> buildExercises(Course course, int unitIndex, math.Random rng) {
  final unit = course.units[unitIndex];
  final earlier = course.units.sublist(0, unitIndex);
  final earlierItems = earlier.expand((u) => u.items).toList();
  final earlierWords = earlier.expand((u) => u.words).toList();

  final reads = <Exercise>[];
  final hears = <Exercise>[];
  for (final item in unit.items) {
    reads.add(Exercise(
      kind: ExerciseKind.readChar,
      question: 'How do you read this?',
      display: item.front,
      reading: item.reading,
      options: _options(
        item.reading,
        unit.items.map((i) => i.reading),
        earlierItems.map((i) => i.reading),
        rng,
      ),
      answer: item.reading,
      reveal: _reveal(item.front, item.reading, item.meaning),
    ));
    hears.add(Exercise(
      kind: ExerciseKind.hearChar,
      question: 'Which one did you hear?',
      display: item.front,
      reading: item.reading,
      options: _options(
        item.front,
        unit.items.map((i) => i.front),
        earlierItems.map((i) => i.front),
        rng,
      ),
      answer: item.front,
      reveal: _reveal(item.front, item.reading, item.meaning),
    ));
  }
  reads.shuffle(rng);
  hears.shuffle(rng);

  final wordExercises = <Exercise>[];
  for (final word in unit.words) {
    final options = _options(
      word.reading,
      unit.words.map((w) => w.reading),
      earlierWords.map((w) => w.reading),
      rng,
    );
    if (options.length < 2) continue;
    wordExercises.add(Exercise(
      kind: ExerciseKind.readWord,
      question: 'Read the word.',
      display: word.text,
      reading: word.reading,
      options: options,
      answer: word.reading,
      reveal: _reveal(word.text, word.reading, word.meaning),
    ));
  }
  wordExercises.shuffle(rng);

  return [...reads, ...hears, ...wordExercises];
}
