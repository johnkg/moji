import 'dart:math' as math;

import '../models/course.dart';

enum ExerciseKind {
  /// See a character, pick its reading.
  readChar,

  /// Hear a character, pick the character.
  hearChar,

  /// See a word, pick its reading.
  readWord,

  /// Hear a phrase, pick its meaning.
  hearMeaning,

  /// See a phrase in romaji or pinyin, pick its meaning.
  readMeaning,

  /// See a sentence in native script, pick its meaning.
  readSentence,

  /// See a sentence with a gap, pick the word that fits.
  fillBlank,

  /// Hear a sentence, pick the written sentence.
  hearSentence,

  /// Put word chips in the right order to build a sentence.
  arrange,
}

class Exercise {
  const Exercise({
    required this.kind,
    required this.question,
    required this.speak,
    required this.display,
    required this.displayIsNative,
    required this.options,
    required this.optionsAreNative,
    required this.answer,
    required this.reading,
    required this.reveal,
    this.parts = const [],
  });

  final ExerciseKind kind;
  final String question;

  /// Native text sent to text-to-speech.
  final String speak;

  /// Shown large on screen. Null for listening exercises.
  final String? display;
  final bool displayIsNative;
  final List<String> options;
  final bool optionsAreNative;
  final String answer;

  /// Romaji or pinyin, shown when audio is unavailable.
  final String reading;

  /// Shown after answering, e.g. "あい = ai (love)".
  final String reveal;

  /// For [ExerciseKind.arrange]: the chips in the right order. [options] holds
  /// the same chips shuffled, and [answer] is them joined.
  final List<String> parts;

  bool get isListening => display == null;
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

/// The chips in a random order, not already in the right one when that can be avoided.
List<String> _shuffledChips(List<String> parts, math.Random rng) {
  final chips = List.of(parts);
  for (var attempt = 0; attempt < 8; attempt++) {
    chips.shuffle(rng);
    if (chips.join() != parts.join()) break;
  }
  return chips;
}

String _reveal(String text, String reading, String meaning) {
  return meaning.isEmpty ? '$text = $reading' : '$text = $reading ($meaning)';
}

/// Exercises for one unit of [course].
List<Exercise> buildExercises(Course course, int unitIndex, math.Random rng) {
  if (course.isSentences) return _sentenceExercises(course, unitIndex, rng);
  return course.isSpeaking
      ? _speakingExercises(course, unitIndex, rng)
      : _readingExercises(course, unitIndex, rng);
}

/// Read each sentence and pick its meaning, fill the gap, hear each sentence
/// and pick the written one, then build each sentence from word chips.
List<Exercise> _sentenceExercises(Course course, int unitIndex, math.Random rng) {
  final unit = course.units[unitIndex];
  final earlierItems = course.units.sublist(0, unitIndex).expand((u) => u.items).toList();

  final reads = <Exercise>[];
  final fills = <Exercise>[];
  final hears = <Exercise>[];
  final arranges = <Exercise>[];
  for (final item in unit.items) {
    final reveal = '${item.front} = ${item.reading} (${item.meaning})';
    reads.add(Exercise(
      kind: ExerciseKind.readSentence,
      question: 'What does this say?',
      speak: item.front,
      display: item.front,
      displayIsNative: true,
      options: _options(
        item.meaning,
        unit.items.map((i) => i.meaning),
        earlierItems.map((i) => i.meaning),
        rng,
      ),
      optionsAreNative: false,
      answer: item.meaning,
      reading: item.reading,
      reveal: reveal,
    ));

    final blank = item.blank;
    if (blank != null) {
      final shown = StringBuffer();
      for (var i = 0; i < item.parts.length; i++) {
        shown.write(i == blank.part ? '＿＿' : item.parts[i]);
      }
      fills.add(Exercise(
        kind: ExerciseKind.fillBlank,
        question: 'Which word fits the gap?',
        speak: item.front,
        display: shown.toString(),
        displayIsNative: true,
        options: List.of(blank.options)..shuffle(rng),
        optionsAreNative: true,
        answer: item.parts[blank.part],
        reading: item.reading,
        reveal: reveal,
      ));
    }

    hears.add(Exercise(
      kind: ExerciseKind.hearSentence,
      question: 'Which sentence did you hear?',
      speak: item.front,
      display: null,
      displayIsNative: true,
      options: _options(
        item.front,
        unit.items.map((i) => i.front),
        earlierItems.map((i) => i.front),
        rng,
      ),
      optionsAreNative: true,
      answer: item.front,
      reading: item.reading,
      reveal: reveal,
    ));

    if (item.parts.length >= 2) {
      arranges.add(Exercise(
        kind: ExerciseKind.arrange,
        question: 'Put the words in order.',
        speak: item.front,
        display: item.meaning,
        displayIsNative: false,
        options: _shuffledChips(item.parts, rng),
        optionsAreNative: true,
        answer: item.parts.join(),
        reading: item.reading,
        reveal: reveal,
        parts: item.parts,
      ));
    }
  }
  reads.shuffle(rng);
  fills.shuffle(rng);
  hears.shuffle(rng);
  arranges.shuffle(rng);
  return [...reads, ...fills, ...hears, ...arranges];
}

/// Read each character, then hear each character, then read words built from
/// what has been taught so far.
List<Exercise> _readingExercises(Course course, int unitIndex, math.Random rng) {
  final unit = course.units[unitIndex];
  final earlier = course.units.sublist(0, unitIndex);
  final earlierItems = earlier.expand((u) => u.items).toList();
  final earlierWords = earlier.expand((u) => u.words).toList();

  final reads = <Exercise>[];
  final hears = <Exercise>[];
  for (final item in unit.items) {
    final reveal = _reveal(item.front, item.reading, item.meaning);
    reads.add(Exercise(
      kind: ExerciseKind.readChar,
      question: 'How do you read this?',
      speak: item.front,
      display: item.front,
      displayIsNative: true,
      options: _options(
        item.reading,
        unit.items.map((i) => i.reading),
        earlierItems.map((i) => i.reading),
        rng,
      ),
      optionsAreNative: false,
      answer: item.reading,
      reading: item.reading,
      reveal: reveal,
    ));

    if (!item.listen) continue;
    // A wrong choice must not sound the same as the answer (他 and 她 are
    // both tā), or the question has two right answers.
    bool soundsDifferent(LessonItem other) => other.listen && other.reading != item.reading;
    hears.add(Exercise(
      kind: ExerciseKind.hearChar,
      question: 'Which one did you hear?',
      speak: item.front,
      display: null,
      displayIsNative: true,
      options: _options(
        item.front,
        unit.items.where(soundsDifferent).map((i) => i.front),
        earlierItems.where(soundsDifferent).map((i) => i.front),
        rng,
      ),
      optionsAreNative: true,
      answer: item.front,
      reading: item.reading,
      reveal: reveal,
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
      speak: word.text,
      display: word.text,
      displayIsNative: true,
      options: options,
      optionsAreNative: false,
      answer: word.reading,
      reading: word.reading,
      reveal: _reveal(word.text, word.reading, word.meaning),
    ));
  }
  wordExercises.shuffle(rng);

  return [...reads, ...hears, ...wordExercises];
}

/// See each phrase in romaji or pinyin and pick its meaning, then hear each
/// phrase and pick its meaning. No reading of native script is needed.
List<Exercise> _speakingExercises(Course course, int unitIndex, math.Random rng) {
  final unit = course.units[unitIndex];
  final earlierItems = course.units.sublist(0, unitIndex).expand((u) => u.items).toList();

  final reads = <Exercise>[];
  final hears = <Exercise>[];
  for (final item in unit.items) {
    final options = _options(
      item.meaning,
      unit.items.map((i) => i.meaning),
      earlierItems.map((i) => i.meaning),
      rng,
    );
    final reveal = '${item.reading} = ${item.meaning}';
    reads.add(Exercise(
      kind: ExerciseKind.readMeaning,
      question: 'What does this mean?',
      speak: item.front,
      display: item.reading,
      displayIsNative: false,
      options: options,
      optionsAreNative: false,
      answer: item.meaning,
      reading: item.reading,
      reveal: reveal,
    ));
    if (!item.listen) continue;
    hears.add(Exercise(
      kind: ExerciseKind.hearMeaning,
      question: 'What did you hear?',
      speak: item.front,
      display: null,
      displayIsNative: false,
      options: List.of(options)..shuffle(rng),
      optionsAreNative: false,
      answer: item.meaning,
      reading: item.reading,
      reveal: reveal,
    ));
  }
  reads.shuffle(rng);
  hears.shuffle(rng);
  return [...reads, ...hears];
}
