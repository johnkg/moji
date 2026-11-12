import 'package:flutter/material.dart';

import '../app_state.dart';
import '../models/deck.dart';
import 'locales.dart';

/// Chart of every card in a deck. Tap one to hear it.
class BrowseScreen extends StatelessWidget {
  const BrowseScreen({super.key, required this.app, required this.deck});

  final AppState app;
  final Deck deck;

  Future<void> _speak(BuildContext context, StudyCard card) async {
    final messenger = ScaffoldMessenger.of(context);
    final ok = await app.speaker.speak(card.front, deck.lang);
    if (!ok) {
      messenger.showSnackBar(
        SnackBar(content: Text('No ${languageName(deck.lang)} voice on this device.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final longText = deck.cards.any((c) => c.front.length > 2);
    return Scaffold(
      appBar: AppBar(title: Text(deck.title)),
      body: GridView.builder(
        padding: const EdgeInsets.all(12),
        gridDelegate: SliverGridDelegateWithMaxCrossAxisExtent(
          maxCrossAxisExtent: longText ? 220 : 90,
          childAspectRatio: longText ? 1.8 : 0.9,
          mainAxisSpacing: 8,
          crossAxisSpacing: 8,
        ),
        itemCount: deck.cards.length,
        itemBuilder: (context, index) {
          final card = deck.cards[index];
          return Card(
            margin: EdgeInsets.zero,
            child: InkWell(
              onTap: () => _speak(context, card),
              child: Padding(
                padding: const EdgeInsets.all(6),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    FittedBox(
                      fit: BoxFit.scaleDown,
                      child: Text(
                        card.front,
                        locale: scriptLocale(deck.lang),
                        style: TextStyle(fontSize: longText ? 24 : 32),
                      ),
                    ),
                    const SizedBox(height: 4),
                    FittedBox(
                      fit: BoxFit.scaleDown,
                      child: Text(card.reading),
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
