import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

import '../models/deck.dart';

/// Deck files under assets/decks/. Add new decks here.
const List<String> deckFiles = [
  'ja_hiragana',
  'ja_hiragana_extra',
  'ja_katakana',
  'ja_katakana_extra',
  'ja_phrases',
  'ja_sentences',
  'ja_read_sentences',
  'zh_tones',
  'zh_hanzi',
  'zh_phrases',
  'zh_sentences',
  'zh_read_sentences',
];

Deck parseDeck(String source) {
  return Deck.fromJson(jsonDecode(source) as Map<String, dynamic>);
}

Future<List<Deck>> loadDecks() async {
  final decks = <Deck>[];
  for (final name in deckFiles) {
    final source = await rootBundle.loadString('assets/decks/$name.json');
    decks.add(parseDeck(source));
  }
  return decks;
}
