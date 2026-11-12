/// One thing to learn: a character, word or phrase.
class StudyCard {
  const StudyCard({
    required this.id,
    required this.front,
    required this.reading,
    required this.meaning,
  });

  final String id;

  /// Native script. Also the text sent to text-to-speech.
  final String front;

  /// Romaji or pinyin.
  final String reading;

  /// English meaning. Empty for kana.
  final String meaning;

  factory StudyCard.fromJson(Map<String, dynamic> json) {
    return StudyCard(
      id: json['id'] as String,
      front: json['front'] as String,
      reading: json['reading'] as String,
      meaning: (json['meaning'] as String?) ?? '',
    );
  }
}

class Deck {
  const Deck({
    required this.id,
    required this.lang,
    required this.title,
    required this.description,
    required this.cards,
  });

  final String id;

  /// 'ja' or 'zh'.
  final String lang;
  final String title;
  final String description;
  final List<StudyCard> cards;

  /// Key used to store progress for [card]. Unique across decks.
  String keyFor(StudyCard card) => '$id:${card.id}';

  factory Deck.fromJson(Map<String, dynamic> json) {
    final cards = (json['cards'] as List<dynamic>)
        .map((c) => StudyCard.fromJson(c as Map<String, dynamic>))
        .toList();
    return Deck(
      id: json['id'] as String,
      lang: json['lang'] as String,
      title: json['title'] as String,
      description: (json['description'] as String?) ?? '',
      cards: cards,
    );
  }
}
