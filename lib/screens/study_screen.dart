import 'package:flutter/material.dart';

import '../app_state.dart';
import '../models/deck.dart';
import '../srs/scheduler.dart';
import 'locales.dart';

/// One review session: due cards, then a few new ones.
class StudyScreen extends StatefulWidget {
  const StudyScreen({super.key, required this.app, required this.deck});

  final AppState app;
  final Deck deck;

  @override
  State<StudyScreen> createState() => _StudyScreenState();
}

class _StudyScreenState extends State<StudyScreen> {
  late final List<StudyCard> _queue;
  int _done = 0;
  bool _revealed = false;
  bool _currentIsNew = false;
  bool _saving = false;

  @override
  void initState() {
    super.initState();
    _queue = widget.app.buildSession(widget.deck, DateTime.now());
    _prepareCurrent();
  }

  /// New cards are shown with the answer, so there is something to learn.
  void _prepareCurrent() {
    _currentIsNew = _queue.isNotEmpty && widget.app.isNew(widget.deck, _queue.first);
    _revealed = _currentIsNew;
  }

  Future<void> _speak() async {
    if (_queue.isEmpty) return;
    final messenger = ScaffoldMessenger.of(context);
    final ok = await widget.app.speaker.speak(_queue.first.front, widget.deck.lang);
    if (!ok) {
      messenger.showSnackBar(
        SnackBar(content: Text('No ${languageName(widget.deck.lang)} voice on this device.')),
      );
    }
  }

  void _reveal() {
    setState(() => _revealed = true);
    _speak();
  }

  Future<void> _grade(Grade grade) async {
    if (_saving || _queue.isEmpty) return;
    setState(() => _saving = true);
    final card = _queue.first;
    await widget.app.grade(widget.deck, card, grade, DateTime.now());
    if (!mounted) return;
    setState(() {
      _queue.removeAt(0);
      if (grade == Grade.again) {
        _queue.add(card);
      } else {
        _done++;
      }
      _prepareCurrent();
      _saving = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.deck.title)),
      body: SafeArea(
        child: _queue.isEmpty ? _buildFinished(context) : _buildCard(context),
      ),
    );
  }

  Widget _buildFinished(BuildContext context) {
    final message = _done == 0
        ? 'Nothing due right now. Come back later.'
        : 'Session done. $_done cards reviewed.';
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              message,
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Back'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCard(BuildContext context) {
    final card = _queue.first;
    final theme = Theme.of(context);
    final total = _done + _queue.length;
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          LinearProgressIndicator(value: total == 0 ? 0 : _done / total),
          const SizedBox(height: 8),
          Text(
            _currentIsNew ? 'New' : '${_queue.length} left',
            style: theme.textTheme.labelLarge,
          ),
          Expanded(
            child: Center(
              child: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    FittedBox(
                      fit: BoxFit.scaleDown,
                      child: Text(
                        card.front,
                        locale: scriptLocale(widget.deck.lang),
                        style: const TextStyle(fontSize: 96),
                      ),
                    ),
                    const SizedBox(height: 16),
                    if (_revealed) ...[
                      Text(card.reading, style: theme.textTheme.headlineMedium),
                      if (card.meaning.isNotEmpty) ...[
                        const SizedBox(height: 8),
                        Text(
                          card.meaning,
                          textAlign: TextAlign.center,
                          style: theme.textTheme.titleMedium,
                        ),
                      ],
                      const SizedBox(height: 16),
                      IconButton.filledTonal(
                        tooltip: 'Listen',
                        iconSize: 32,
                        icon: const Icon(Icons.volume_up),
                        onPressed: _speak,
                      ),
                    ],
                  ],
                ),
              ),
            ),
          ),
          if (!_revealed)
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: _reveal,
                child: const Padding(
                  padding: EdgeInsets.all(12),
                  child: Text('Show answer'),
                ),
              ),
            )
          else
            Row(
              children: [
                _gradeButton('Again', Grade.again),
                _gradeButton('Hard', Grade.hard),
                _gradeButton('Good', Grade.good),
                _gradeButton('Easy', Grade.easy),
              ],
            ),
        ],
      ),
    );
  }

  Widget _gradeButton(String label, Grade grade) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 4),
        child: FilledButton.tonal(
          onPressed: _saving ? null : () => _grade(grade),
          style: FilledButton.styleFrom(padding: const EdgeInsets.symmetric(vertical: 14)),
          child: FittedBox(child: Text(label)),
        ),
      ),
    );
  }
}
