import 'package:flutter/material.dart';

import '../app_state.dart';
import '../models/course.dart';
import '../models/deck.dart';
import '../models/stats.dart';
import 'browse_screen.dart';
import 'lesson_screen.dart';
import 'locales.dart';
import 'study_screen.dart';
import 'write_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, required this.app});

  final AppState app;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Moji')),
      body: AnimatedBuilder(
        animation: app,
        builder: (context, _) {
          final now = DateTime.now();
          final children = <Widget>[_StatsBar(stats: app.stats, now: now)];
          for (final lang in const ['ja', 'zh']) {
            final courses = app.courses.where((c) => c.lang == lang).toList();
            final decks = app.decks.where((d) => d.lang == lang).toList();
            if (courses.isEmpty && decks.isEmpty) continue;
            children.add(
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 24, 16, 4),
                child: Text(languageName(lang), style: theme.textTheme.headlineSmall),
              ),
            );
            for (final course in courses) {
              children.add(_sectionLabel(theme, course.title, course.description));
              for (var i = 0; i < course.units.length; i++) {
                children.add(_UnitTile(app: app, course: course, unitIndex: i));
              }
            }
            if (decks.isNotEmpty) {
              children.add(_sectionLabel(
                theme,
                'Flashcard review',
                'Finished lessons come back here. Opening a deck also adds untaught cards.',
              ));
              for (final deck in decks) {
                children.add(_DeckTile(app: app, deck: deck, now: now));
              }
            }
          }
          children.add(const SizedBox(height: 24));
          return ListView(children: children);
        },
      ),
    );
  }

  Widget _sectionLabel(ThemeData theme, String title, String caption) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: theme.textTheme.titleMedium),
          if (caption.isNotEmpty) Text(caption, style: theme.textTheme.bodySmall),
        ],
      ),
    );
  }
}

class _UnitTile extends StatelessWidget {
  const _UnitTile({required this.app, required this.course, required this.unitIndex});

  final AppState app;
  final Course course;
  final int unitIndex;

  @override
  Widget build(BuildContext context) {
    final unit = course.units[unitIndex];
    final done = app.isUnitDone(course, unitIndex);
    final unlocked = app.isUnitUnlocked(course, unitIndex);
    final canWrite = unit.items.any((i) => app.strokes.has(i.front));
    final IconData icon;
    if (done) {
      icon = Icons.check_circle;
    } else if (unlocked) {
      icon = Icons.play_circle;
    } else {
      icon = Icons.lock;
    }
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      child: ListTile(
        enabled: unlocked,
        leading: Icon(icon, size: 32),
        title: Text('${unitIndex + 1}. ${unit.title}'),
        subtitle: Text(
          course.isSpeaking
              ? unit.items.map((i) => i.reading).join(' · ')
              : unit.items.map((i) => i.front).join('  '),
          locale: scriptLocale(course.lang),
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
        ),
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (done) const Text('Redo'),
            if (unlocked && !course.isSpeaking && canWrite)
              IconButton(
                tooltip: 'Learn to write these',
                icon: const Icon(Icons.edit),
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute<void>(
                      builder: (_) => WriteScreen(app: app, course: course, unitIndex: unitIndex),
                    ),
                  );
                },
              ),
          ],
        ),
        onTap: () {
          Navigator.of(context).push(
            MaterialPageRoute<void>(
              builder: (_) => LessonScreen(app: app, course: course, unitIndex: unitIndex),
            ),
          );
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
        subtitle: Text('$due due · $fresh new · $learned/${deck.cards.length} seen'),
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

/// Streak, level and XP toward the next level.
class _StatsBar extends StatelessWidget {
  const _StatsBar({required this.stats, required this.now});

  final Stats stats;
  final DateTime now;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final streak = stats.currentStreak(now);
    final String streakText;
    if (streak == 0) {
      streakText = 'Start a streak today';
    } else if (stats.activeToday(now)) {
      streakText = '🔥 $streak-day streak';
    } else {
      streakText = '🔥 $streak-day streak: study today to keep it';
    }
    return Card(
      margin: const EdgeInsets.fromLTRB(12, 12, 12, 0),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(streakText, style: theme.textTheme.titleMedium),
            const SizedBox(height: 12),
            Text(
              'Level ${stats.level} · ${stats.xpIntoLevel}/${Stats.xpPerLevel} XP',
              style: theme.textTheme.bodyMedium,
            ),
            const SizedBox(height: 6),
            LinearProgressIndicator(value: stats.xpIntoLevel / Stats.xpPerLevel),
          ],
        ),
      ),
    );
  }
}
