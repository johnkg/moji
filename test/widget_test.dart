import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:moji/services/deck_loader.dart';

// Run from the project root: flutter test
void main() {
  test('every listed deck file parses and has unique card ids', () {
    for (final name in deckFiles) {
      final deck = parseDeck(File('assets/decks/$name.json').readAsStringSync());
      expect(deck.id, name);
      expect(deck.lang, anyOf('ja', 'zh'));
      expect(deck.cards, isNotEmpty);
      final ids = deck.cards.map((c) => c.id).toSet();
      expect(ids.length, deck.cards.length, reason: 'duplicate ids in $name');
    }
  });
}
