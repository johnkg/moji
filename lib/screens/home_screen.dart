import 'package:flutter/material.dart';

import '../app_state.dart';
import '../models/deck.dart';
import 'browse_screen.dart';
import 'locales.dart';
import 'study_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, required this.app});

  final AppState app;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Moji')),
      body: AnimatedBuilder(
        animation: app,
        builder: (context, _) {
          final now = DateTime.now();
          final children = <Widget>[];
          for (final lang in const ['ja', 'zh']) {
            final decks = app.decks.where((d) => d.lang == lang).toList();
            if (decks.isEmpty) continue;
            children.add(
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 20, 16, 8),
                child: Text(
                  languageName(lang),
                  style: Theme.of(context).textTheme.titleLarge,
                ),
              ),
            );
            for (final deck in decks) {
              children.add(_DeckTile(app: app, deck: deck, now: now));
            }
          }
          return ListView(children: children);
        },
      ),
    );
  }
}

class _DeckTile extends StatelessWidget {
  const _DeckTile({required this.app, required this.deck, required this.now});

  final AppState app;
  final Deck deck;
  final DateTime now;

  @override
  Widget build(BuildContext context) {
    final due = app.dueCount(deck, now);
    final fresh = app.newCount(deck);
    final learned = deck.cards.length - fresh;
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      child: ListTile(
        title: Text(deck.title),
        subtitle: Text(
          '$due due · $fresh new · $learned/${deck.cards.length} seen\n${deck.description}',
        ),
        isThreeLine: true,
        trailing: IconButton(
          tooltip: 'Browse all',
          icon: const Icon(Icons.grid_view),
          onPressed: () {
            Navigator.of(context).push(
              MaterialPageRoute<void>(
                builder: (_) => BrowseScreen(app: app, deck: deck),
              ),
            );
          },
        ),
        onTap: () {
          Navigator.of(context).push(
            MaterialPageRoute<void>(
              builder: (_) => StudyScreen(app: app, deck: deck),
            ),
          );
        },
      ),
    );
  }
}
