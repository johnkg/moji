/// A gap in a sentence: the part to hide and the four words to choose from.
class LessonBlank {
  const LessonBlank({required this.part, required this.options});

  /// Index into [LessonItem.parts] of the hidden word.
  final int part;
  final List<String> options;

  factory LessonBlank.fromJson(Map<String, dynamic> json) {
    return LessonBlank(
      part: json['part'] as int,
      options: (json['options'] as List<dynamic>).cast<String>(),
    );
  }
}

/// A character taught in a lesson.
class LessonItem {
  const LessonItem({
    required this.id,
    required this.front,
    required this.reading,
    required this.meaning,
    required this.hint,
    required this.card,
    this.listen = true,
    this.parts = const [],
    this.blank,
  });

  final String id;

  /// Native script. Also the text sent to text-to-speech.
  final String front;

  /// Romaji or pinyin.
  final String reading;
  final String meaning;

  /// Memory hook and pronunciation tip.
  final String hint;

  /// Progress key of the matching flashcard ("deckId:cardId"), if any.
  final String? card;

  /// False when the sound alone is ambiguous (を sounds like お), so no
  /// listening exercise is made for it.
  final bool listen;

  /// For sentences: the word chips. Joined, they are [front].
  final List<String> parts;

  /// For sentences: an optional gap to fill, such as a particle.
  final LessonBlank? blank;

  factory LessonItem.fromJson(Map<String, dynamic> json) {
    return LessonItem(
      id: json['id'] as String,
      front: json['front'] as String,
      reading: json['reading'] as String,
      meaning: (json['meaning'] as String?) ?? '',
      hint: (json['hint'] as String?) ?? '',
      card: json['card'] as String?,
      listen: (json['listen'] as bool?) ?? true,
      parts: ((json['parts'] as List<dynamic>?) ?? const <dynamic>[]).cast<String>(),
      blank: json['blank'] == null
          ? null
          : LessonBlank.fromJson(json['blank'] as Map<String, dynamic>),
    );
  }
}

/// A word built only from characters the learner has already met.
class LessonWord {
  const LessonWord({required this.text, required this.reading, required this.meaning});

  final String text;
  final String reading;
  final String meaning;

  factory LessonWord.fromJson(Map<String, dynamic> json) {
    return LessonWord(
      text: json['text'] as String,
      reading: json['reading'] as String,
      meaning: (json['meaning'] as String?) ?? '',
    );
  }
}

class LessonUnit {
  const LessonUnit({
    required this.id,
    required this.title,
    required this.intro,
    required this.items,
    required this.words,
  });

  final String id;
  final String title;

  /// Explanation shown before anything is tested, one paragraph per entry.
  final List<String> intro;
  final List<LessonItem> items;
  final List<LessonWord> words;

  factory LessonUnit.fromJson(Map<String, dynamic> json) {
    return LessonUnit(
      id: json['id'] as String,
      title: json['title'] as String,
      intro: (json['intro'] as List<dynamic>).cast<String>(),
      items: (json['items'] as List<dynamic>)
          .map((i) => LessonItem.fromJson(i as Map<String, dynamic>))
          .toList(),
      words: ((json['words'] as List<dynamic>?) ?? const <dynamic>[])
          .map((w) => LessonWord.fromJson(w as Map<String, dynamic>))
          .toList(),
    );
  }
}

/// An ordered path of units. A unit unlocks when the one before it is done.
enum CourseMode {
  /// Learn to read a script. Native text is shown large.
  reading,

  /// Learn to say phrases. Romaji or pinyin is shown large, native text small.
  speaking,

  /// Read whole sentences, with the small grammar words taught on the way.
  sentences,
}

class Course {
  const Course({
    required this.id,
    required this.lang,
    this.mode = CourseMode.reading,
    required this.title,
    required this.description,
    required this.units,
  });

  final String id;

  /// 'ja' or 'zh'.
  final String lang;
  final CourseMode mode;
  final String title;
  final String description;
  final List<LessonUnit> units;

  bool get isSpeaking => mode == CourseMode.speaking;
  bool get isSentences => mode == CourseMode.sentences;

  /// Key used to store that [unit] is finished. Unique across courses.
  String keyFor(LessonUnit unit) => '$id:${unit.id}';

  factory Course.fromJson(Map<String, dynamic> json) {
    return Course(
      id: json['id'] as String,
      lang: json['lang'] as String,
      mode: switch (json['mode']) {
        'speaking' => CourseMode.speaking,
        'sentences' => CourseMode.sentences,
        _ => CourseMode.reading,
      },
      title: json['title'] as String,
      description: (json['description'] as String?) ?? '',
      units: (json['units'] as List<dynamic>)
          .map((u) => LessonUnit.fromJson(u as Map<String, dynamic>))
          .toList(),
    );
  }
}
