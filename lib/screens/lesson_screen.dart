import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../app_state.dart';
import '../lessons/exercise.dart';
import '../models/course.dart';
import 'locales.dart';

enum _StepKind { intro, meet, exercise }

class _Step {
  const _Step.intro()
      : kind = _StepKind.intro,
        item = null,
        exercise = null,
        isRetry = false;

  const _Step.meet(LessonItem lessonItem)
      : kind = _StepKind.meet,
        item = lessonItem,
        exercise = null,
        isRetry = false;

  const _Step.exercise(Exercise lessonExercise, {this.isRetry = false})
      : kind = _StepKind.exercise,
        item = null,
        exercise = lessonExercise;

  final _StepKind kind;
  final LessonItem? item;
  final Exercise? exercise;

  /// A second try at an exercise answered wrong. Not repeated again.
  final bool isRetry;
}

/// One unit: explanation, meet each character, then exercises.
class LessonScreen extends StatefulWidget {
  const LessonScreen({
    super.key,
    required this.app,
    required this.course,
    required this.unitIndex,
  });

  final AppState app;
  final Course course;
  final int unitIndex;

  @override
  State<LessonScreen> createState() => _LessonScreenState();
}

class _LessonScreenState extends State<LessonScreen> {
  late final LessonUnit _unit = widget.course.units[widget.unitIndex];
  late final List<_Step> _steps;
  int _index = 0;
  String? _picked;
  bool _voiceFailed = false;
  bool _finished = false;
  bool _busy = false;

  String get _lang => widget.course.lang;

  @override
  void initState() {
    super.initState();
    final exercises = buildExercises(widget.course, widget.unitIndex, math.Random());
    _steps = [
      const _Step.intro(),
      for (final item in _unit.items) _Step.meet(item),
      for (final exercise in exercises) _Step.exercise(exercise),
    ];
  }

  Future<void> _say(String text) async {
    final ok = await widget.app.speaker.speak(text, _lang);
    if (!ok && mounted) setState(() => _voiceFailed = true);
  }

  void _pick(Exercise exercise, String option) {
    if (_picked != null) return;
    setState(() => _picked = option);
    _say(exercise.display);
  }

  Future<void> _next() async {
    if (_busy) return;
    final step = _steps[_index];
    final exercise = step.exercise;
    if (exercise != null && _picked != null && _picked != exercise.answer && !step.isRetry) {
      _steps.add(_Step.exercise(exercise, isRetry: true));
    }

    if (_index + 1 >= _steps.length) {
      setState(() => _busy = true);
      await widget.app.completeUnit(widget.course, _unit, DateTime.now());
      if (!mounted) return;
      setState(() {
        _finished = true;
        _busy = false;
      });
      return;
    }

    setState(() {
      _index++;
      _picked = null;
    });
    final next = _steps[_index];
    if (next.kind == _StepKind.meet) {
      _say(next.item!.front);
    } else if (next.exercise != null && next.exercise!.kind == ExerciseKind.hearChar) {
      _say(next.exercise!.display);
    }
  }

  @override
  Widget build(BuildContext context) {
    final Widget content;
    final Widget button;
    if (_finished) {
      content = _buildFinished(context);
      button = _bottomButton('Done', () => Navigator.of(context).pop());
    } else {
      final step = _steps[_index];
      switch (step.kind) {
        case _StepKind.intro:
          content = _buildIntro(context);
          button = _bottomButton('Start', _next);
          break;
        case _StepKind.meet:
          content = _buildMeet(context, step.item!);
          button = _bottomButton('Next', _next);
          break;
        case _StepKind.exercise:
          content = _buildExercise(context, step.exercise!);
          button = _bottomButton('Continue', _picked == null || _busy ? null : _next);
          break;
      }
    }

    return Scaffold(
      appBar: AppBar(title: Text(_unit.title)),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              LinearProgressIndicator(value: _finished ? 1 : _index / _steps.length),
              const SizedBox(height: 16),
              Expanded(child: SingleChildScrollView(child: content)),
              const SizedBox(height: 12),
              button,
            ],
          ),
        ),
      ),
    );
  }

  Widget _bottomButton(String label, VoidCallback? onPressed) {
    return SizedBox(
      width: double.infinity,
      child: FilledButton(
        onPressed: onPressed,
        child: Padding(padding: const EdgeInsets.all(12), child: Text(label)),
      ),
    );
  }

  Widget _voiceNote(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 8),
      child: Text(
        'No ${languageName(_lang)} voice found on this device, so audio is off.',
        textAlign: TextAlign.center,
        style: Theme.of(context).textTheme.bodySmall,
      ),
    );
  }

  Widget _buildIntro(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(_unit.title, style: theme.textTheme.headlineSmall),
        const SizedBox(height: 16),
        for (final paragraph in _unit.intro)
          Padding(
            padding: const EdgeInsets.only(bottom: 14),
            child: Text(paragraph, style: theme.textTheme.bodyLarge),
          ),
      ],
    );
  }

  Widget _buildMeet(BuildContext context, LessonItem item) {
    final theme = Theme.of(context);
    return Column(
      children: [
        Text('New character', style: theme.textTheme.labelLarge),
        FittedBox(
          fit: BoxFit.scaleDown,
          child: Text(
            item.front,
            locale: scriptLocale(_lang),
            style: const TextStyle(fontSize: 112),
          ),
        ),
        Text(item.reading, style: theme.textTheme.headlineMedium),
        if (item.meaning.isNotEmpty) ...[
          const SizedBox(height: 4),
          Text(item.meaning, style: theme.textTheme.titleMedium),
        ],
        const SizedBox(height: 12),
        IconButton.filledTonal(
          tooltip: 'Listen',
          iconSize: 32,
          icon: const Icon(Icons.volume_up),
          onPressed: () => _say(item.front),
        ),
        if (_voiceFailed) _voiceNote(context),
        if (item.hint.isNotEmpty) ...[
          const SizedBox(height: 16),
          Card(
            margin: EdgeInsets.zero,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Text(item.hint, style: theme.textTheme.bodyLarge),
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildExercise(BuildContext context, Exercise exercise) {
    final theme = Theme.of(context);
    final answered = _picked != null;
    final correct = _picked == exercise.answer;
    final hearing = exercise.kind == ExerciseKind.hearChar;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(exercise.question, textAlign: TextAlign.center, style: theme.textTheme.titleMedium),
        const SizedBox(height: 12),
        if (hearing) ...[
          Center(
            child: IconButton.filledTonal(
              tooltip: 'Play again',
              iconSize: 48,
              icon: const Icon(Icons.volume_up),
              onPressed: () => _say(exercise.display),
            ),
          ),
          if (_voiceFailed) ...[
            _voiceNote(context),
            Text(
              'The sound is "${exercise.reading}".',
              textAlign: TextAlign.center,
              style: theme.textTheme.bodyMedium,
            ),
          ],
        ] else
          Center(
            child: FittedBox(
              fit: BoxFit.scaleDown,
              child: Text(
                exercise.display,
                locale: scriptLocale(_lang),
                style: const TextStyle(fontSize: 80),
              ),
            ),
          ),
        const SizedBox(height: 16),
        for (final option in exercise.options) _optionTile(context, exercise, option),
        if (answered) ...[
          const SizedBox(height: 8),
          Text(
            correct ? 'Correct!' : 'Not quite.',
            textAlign: TextAlign.center,
            style: theme.textTheme.titleMedium,
          ),
          const SizedBox(height: 4),
          Text(
            exercise.reveal,
            textAlign: TextAlign.center,
            locale: scriptLocale(_lang),
            style: theme.textTheme.titleLarge,
          ),
        ],
      ],
    );
  }

  Widget _optionTile(BuildContext context, Exercise exercise, String option) {
    final scheme = Theme.of(context).colorScheme;
    final answered = _picked != null;
    Color background = scheme.secondaryContainer;
    Color foreground = scheme.onSecondaryContainer;
    if (answered && option == exercise.answer) {
      background = const Color(0xFFB7E4C7);
      foreground = Colors.black87;
    } else if (answered && option == _picked) {
      background = scheme.errorContainer;
      foreground = scheme.onErrorContainer;
    }
    final native = exercise.kind == ExerciseKind.hearChar;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Material(
        color: background,
        borderRadius: BorderRadius.circular(12),
        clipBehavior: Clip.antiAlias,
        child: InkWell(
          onTap: answered ? null : () => _pick(exercise, option),
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
            child: Center(
              child: Text(
                option,
                locale: native ? scriptLocale(_lang) : null,
                style: TextStyle(fontSize: native ? 32 : 20, color: foreground),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildFinished(BuildContext context) {
    final theme = Theme.of(context);
    final hasNext = widget.unitIndex + 1 < widget.course.units.length;
    return Column(
      children: [
        const SizedBox(height: 24),
        const Icon(Icons.check_circle, size: 72, color: Colors.green),
        const SizedBox(height: 16),
        Text('Unit complete', style: theme.textTheme.headlineSmall),
        const SizedBox(height: 12),
        FittedBox(
          fit: BoxFit.scaleDown,
          child: Text(
            _unit.items.map((i) => i.front).join('  '),
            locale: scriptLocale(_lang),
            style: const TextStyle(fontSize: 40),
          ),
        ),
        const SizedBox(height: 16),
        Text(
          'These characters are now in your flashcard review. They come back tomorrow.',
          textAlign: TextAlign.center,
          style: theme.textTheme.bodyLarge,
        ),
        if (hasNext) ...[
          const SizedBox(height: 8),
          Text(
            'Next unit unlocked: ${widget.course.units[widget.unitIndex + 1].title}.',
            textAlign: TextAlign.center,
            style: theme.textTheme.bodyLarge,
          ),
        ],
      ],
    );
  }
}
