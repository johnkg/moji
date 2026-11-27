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
  int _firstTryCorrect = 0;

  /// Word chips placed so far in an arrange exercise, as indexes into its options.
  List<int> _placed = [];
  int _earnedXp = 0;
  int _streak = 0;

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

  bool get _isRetryStep => _steps[_index].isRetry;

  void _pick(Exercise exercise, String option) {
    if (_picked != null) return;
    if (option == exercise.answer && !_isRetryStep) _firstTryCorrect++;
    setState(() => _picked = option);
    _say(exercise.speak);
  }

  void _place(Exercise exercise, int chip) {
    if (_picked != null || _placed.contains(chip)) return;
    setState(() => _placed = [..._placed, chip]);
    if (_placed.length == exercise.options.length) {
      _pick(exercise, [for (final i in _placed) exercise.options[i]].join());
    }
  }

  void _unplace(int position) {
    if (_picked != null) return;
    setState(() => _placed = [..._placed]..removeAt(position));
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
      final now = DateTime.now();
      final earned = await widget.app.completeUnit(
        widget.course,
        _unit,
        now,
        firstTryCorrect: _firstTryCorrect,
      );
      if (!mounted) return;
      setState(() {
        _earnedXp = earned;
        _streak = widget.app.stats.currentStreak(now);
        _finished = true;
        _busy = false;
      });
      return;
    }

    setState(() {
      _index++;
      _picked = null;
      _placed = [];
    });
    final next = _steps[_index];
    if (next.kind == _StepKind.meet) {
      _say(next.item!.front);
    } else if (next.exercise != null && next.exercise!.isListening) {
      _say(next.exercise!.speak);
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
    final speaking = widget.course.isSpeaking;
    final sentences = widget.course.isSentences;
    return Column(
      children: [
        Text(
          sentences ? 'New sentence' : (speaking ? 'New phrase' : 'New character'),
          style: theme.textTheme.labelLarge,
        ),
        const SizedBox(height: 8),
        if (sentences) ...[
          Wrap(
            alignment: WrapAlignment.center,
            spacing: 8,
            runSpacing: 4,
            children: [
              for (final part in item.parts)
                Text(part, locale: scriptLocale(_lang), style: const TextStyle(fontSize: 32)),
            ],
          ),
          const SizedBox(height: 8),
          Text(item.reading, textAlign: TextAlign.center, style: theme.textTheme.titleMedium),
          const SizedBox(height: 4),
          Text(item.meaning, textAlign: TextAlign.center, style: theme.textTheme.titleLarge),
        ] else if (speaking) ...[
          FittedBox(
            fit: BoxFit.scaleDown,
            child: Text(item.reading, style: const TextStyle(fontSize: 44)),
          ),
          const SizedBox(height: 8),
          Text(item.meaning, textAlign: TextAlign.center, style: theme.textTheme.titleLarge),
          const SizedBox(height: 8),
          Text(
            item.front,
            locale: scriptLocale(_lang),
            style: theme.textTheme.titleMedium?.copyWith(color: theme.colorScheme.outline),
          ),
        ] else ...[
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
    if (exercise.kind == ExerciseKind.arrange) return _buildArrange(context, exercise);
    final theme = Theme.of(context);
    final sentence =
        exercise.kind == ExerciseKind.readSentence || exercise.kind == ExerciseKind.fillBlank;
    final answered = _picked != null;
    final correct = _picked == exercise.answer;
    final hearing = exercise.isListening;
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
              onPressed: () => _say(exercise.speak),
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
        ] else if (sentence)
          Center(
            child: Text(
              exercise.display!,
              textAlign: TextAlign.center,
              locale: scriptLocale(_lang),
              style: const TextStyle(fontSize: 34),
            ),
          )
        else
          Center(
            child: FittedBox(
              fit: BoxFit.scaleDown,
              child: Text(
                exercise.display!,
                locale: exercise.displayIsNative ? scriptLocale(_lang) : null,
                style: TextStyle(fontSize: exercise.displayIsNative ? 80 : 44),
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

  Widget _buildArrange(BuildContext context, Exercise exercise) {
    final theme = Theme.of(context);
    final answered = _picked != null;
    final correct = _picked == exercise.answer;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(exercise.question, textAlign: TextAlign.center, style: theme.textTheme.titleMedium),
        const SizedBox(height: 12),
        Text(exercise.display!, textAlign: TextAlign.center, style: theme.textTheme.headlineSmall),
        const SizedBox(height: 16),
        Container(
          constraints: const BoxConstraints(minHeight: 72),
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            border: Border.all(color: theme.colorScheme.outline),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              for (var n = 0; n < _placed.length; n++)
                _chip(
                  context,
                  exercise.options[_placed[n]],
                  answered
                      ? (correct ? const Color(0xFFB7E4C7) : theme.colorScheme.errorContainer)
                      : theme.colorScheme.primaryContainer,
                  answered ? null : () => _unplace(n),
                ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        Wrap(
          alignment: WrapAlignment.center,
          spacing: 8,
          runSpacing: 8,
          children: [
            for (var i = 0; i < exercise.options.length; i++)
              if (!_placed.contains(i))
                _chip(
                  context,
                  exercise.options[i],
                  theme.colorScheme.secondaryContainer,
                  answered ? null : () => _place(exercise, i),
                ),
          ],
        ),
        if (answered) ...[
          const SizedBox(height: 16),
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

  Widget _chip(BuildContext context, String text, Color background, VoidCallback? onTap) {
    return Material(
      color: background,
      borderRadius: BorderRadius.circular(10),
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 14),
          child: Text(text, locale: scriptLocale(_lang), style: const TextStyle(fontSize: 26)),
        ),
      ),
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
    final native = exercise.optionsAreNative;
    final longNative = exercise.kind == ExerciseKind.hearSentence;
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
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: native ? (longNative ? 24 : 32) : 20, color: foreground),
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
        if (widget.course.isSentences)
          for (final item in _unit.items)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 2),
              child: Text(
                item.front,
                textAlign: TextAlign.center,
                locale: scriptLocale(_lang),
                style: const TextStyle(fontSize: 22),
              ),
            )
        else
          FittedBox(
            fit: BoxFit.scaleDown,
            child: Text(
              widget.course.isSpeaking
                  ? _unit.items.map((i) => i.reading).join(' · ')
                  : _unit.items.map((i) => i.front).join('  '),
              locale: scriptLocale(_lang),
              style: TextStyle(fontSize: widget.course.isSpeaking ? 24 : 40),
            ),
          ),
        const SizedBox(height: 16),
        Text(
          widget.course.isSentences
              ? 'These sentences are now in your flashcard review. They come back tomorrow.'
              : widget.course.isSpeaking
                  ? 'These phrases are now in your flashcard review. They come back tomorrow. Keep saying them out loud.'
                  : 'These characters are now in your flashcard review. They come back tomorrow.',
          textAlign: TextAlign.center,
          style: theme.textTheme.bodyLarge,
        ),
        const SizedBox(height: 16),
        Text('+$_earnedXp XP', style: theme.textTheme.headlineSmall),
        if (_streak > 0) Text('🔥 $_streak-day streak', style: theme.textTheme.titleMedium),
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
