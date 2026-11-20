import 'package:flutter/material.dart';

import '../app_state.dart';
import '../models/course.dart';
import '../writing/strokes.dart';
import 'locales.dart';

enum _Phase { watch, trace, free }

/// Teaches how to write each character of a unit: watch the strokes in order,
/// trace them over a guide, then write from memory.
class WriteScreen extends StatefulWidget {
  const WriteScreen({super.key, required this.app, required this.course, required this.unitIndex});

  final AppState app;
  final Course course;
  final int unitIndex;

  @override
  State<WriteScreen> createState() => _WriteScreenState();
}

class _WriteScreenState extends State<WriteScreen> with SingleTickerProviderStateMixin {
  late final LessonUnit _unit = widget.course.units[widget.unitIndex];
  late final List<LessonItem> _items =
      _unit.items.where((i) => widget.app.strokes.has(i.front)).toList();
  late final AnimationController _anim = AnimationController(vsync: this);

  int _index = 0;
  _Phase _phase = _Phase.watch;

  /// Strokes written correctly so far in this phase.
  int _done = 0;

  /// Failed tries on the current stroke.
  int _misses = 0;
  List<Offset> _inking = [];
  List<Offset>? _rejected;
  double _side = 1;
  bool _allDone = false;
  int _earned = 0;

  LessonItem get _item => _items[_index];
  List<List<Offset>> get _model => widget.app.strokes.strokesOf(_item.front);
  bool get _complete => _done >= _model.length;

  @override
  void initState() {
    super.initState();
    if (_items.isNotEmpty) _startItem();
  }

  @override
  void dispose() {
    _anim.dispose();
    super.dispose();
  }

  void _startItem() {
    _phase = _Phase.watch;
    _done = 0;
    _misses = 0;
    _inking = [];
    _rejected = null;
    widget.app.speaker.speak(_item.front, widget.course.lang);
    _replay();
  }

  void _replay() {
    _anim.duration = Duration(milliseconds: 900 * _model.length);
    _anim.forward(from: 0);
  }

  void _startPhase(_Phase phase) {
    setState(() {
      _phase = phase;
      _done = 0;
      _misses = 0;
      _inking = [];
      _rejected = null;
    });
  }

  Future<void> _next() async {
    if (_index + 1 >= _items.length) {
      setState(() => _allDone = true);
      return;
    }
    setState(() {
      _index++;
      _startItem();
    });
  }

  Future<void> _characterDone() async {
    final earned = AppState.writeXp;
    await widget.app.awardXp(earned, DateTime.now());
    if (mounted) setState(() => _earned += earned);
  }

  void _penDown(Offset p) {
    if (_phase == _Phase.watch || _complete) return;
    setState(() {
      _rejected = null;
      _inking = [p];
    });
  }

  void _penMove(Offset p) {
    if (_inking.isEmpty) return;
    setState(() => _inking = [..._inking, p]);
  }

  void _penUp() {
    if (_inking.isEmpty) return;
    final ink = _inking;
    final data = widget.app.strokes;
    final scale = _side / data.size;
    final grid = [for (final p in ink) p / scale];
    final ok = strokeMatches(grid, _model[_done], data.size);
    setState(() {
      _inking = [];
      if (ok) {
        _done++;
        _misses = 0;
        _rejected = null;
      } else {
        _misses++;
        _rejected = ink;
      }
    });
    if (ok && _complete && _phase == _Phase.free) _characterDone();
  }

  String _instruction() {
    switch (_phase) {
      case _Phase.watch:
        return 'Watch the strokes in order. The numbers show the order.';
      case _Phase.trace:
        if (_complete) return 'Well done. Now try it without the guide.';
        return 'Trace stroke ${_done + 1}. Start at the green dot.';
      case _Phase.free:
        if (_complete) return 'You wrote ${_item.front}.';
        if (_misses >= 2) return 'Stroke ${_done + 1} is shown for you. Start at the green dot.';
        return 'Write stroke ${_done + 1} from memory.';
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    if (_items.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text('Write: ${_unit.title}')),
        body: const Center(child: Text('No stroke data for these characters yet.')),
      );
    }
    if (_allDone) return _buildFinished(theme);

    final isLast = _index + 1 >= _items.length;
    final Widget button;
    switch (_phase) {
      case _Phase.watch:
        button = _bottomButton('Trace it', () => _startPhase(_Phase.trace));
      case _Phase.trace:
        button = _bottomButton(
          'Without the guide',
          _complete ? () => _startPhase(_Phase.free) : null,
        );
      case _Phase.free:
        button = _bottomButton(isLast ? 'Finish' : 'Next character', _complete ? _next : null);
    }

    return Scaffold(
      appBar: AppBar(title: Text('Write: ${_unit.title}')),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              LinearProgressIndicator(value: _index / _items.length),
              const SizedBox(height: 12),
              Text(
                '${_item.front}  ·  ${_item.reading}',
                locale: scriptLocale(widget.course.lang),
                style: theme.textTheme.headlineSmall,
              ),
              const SizedBox(height: 4),
              Text(_instruction(), textAlign: TextAlign.center, style: theme.textTheme.bodyLarge),
              if (_rejected != null)
                Padding(
                  padding: const EdgeInsets.only(top: 4),
                  child: Text(
                    'Not quite. Start at the green dot and follow the numbered direction.',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: theme.colorScheme.error),
                  ),
                ),
              const SizedBox(height: 12),
              Expanded(
                child: Center(
                  child: AspectRatio(
                    aspectRatio: 1,
                    child: LayoutBuilder(
                      builder: (context, box) {
                        _side = box.maxWidth;
                        return GestureDetector(
                          behavior: HitTestBehavior.opaque,
                          onPanStart: (d) => _penDown(d.localPosition),
                          onPanUpdate: (d) => _penMove(d.localPosition),
                          onPanEnd: (_) => _penUp(),
                          onPanCancel: _penUp,
                          child: AnimatedBuilder(
                            animation: _anim,
                            builder: (context, _) => CustomPaint(
                              painter: _CharPainter(
                                strokes: _model,
                                gridSize: widget.app.strokes.size,
                                phase: _phase,
                                done: _done,
                                showHint: _phase == _Phase.free && _misses >= 2 && !_complete,
                                watchProgress: _anim.value * _model.length,
                                inking: _inking,
                                rejected: _rejected,
                                ink: theme.colorScheme.onSurface,
                                guide: theme.colorScheme.outlineVariant,
                                accent: theme.colorScheme.primary,
                                error: theme.colorScheme.error,
                                paper: theme.colorScheme.surfaceContainerHighest,
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 8),
              if (_phase == _Phase.watch)
                TextButton.icon(
                  onPressed: _replay,
                  icon: const Icon(Icons.replay),
                  label: const Text('Watch again'),
                )
              else
                TextButton.icon(
                  onPressed: () => _startPhase(_phase),
                  icon: const Icon(Icons.refresh),
                  label: const Text('Clear'),
                ),
              button,
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFinished(ThemeData theme) {
    return Scaffold(
      appBar: AppBar(title: Text('Write: ${_unit.title}')),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              const SizedBox(height: 24),
              const Icon(Icons.check_circle, size: 72, color: Colors.green),
              const SizedBox(height: 16),
              Text('Writing practice done', style: theme.textTheme.headlineSmall),
              const SizedBox(height: 12),
              Text(
                _items.map((i) => i.front).join('  '),
                locale: scriptLocale(widget.course.lang),
                style: const TextStyle(fontSize: 40),
              ),
              const SizedBox(height: 16),
              Text('+$_earned XP', style: theme.textTheme.headlineSmall),
              const Spacer(),
              _bottomButton('Done', () => Navigator.of(context).pop()),
            ],
          ),
        ),
      ),
    );
  }

  Widget _bottomButton(String label, VoidCallback? onPressed) {
    return SizedBox(
      width: double.infinity,
      child: FilledButton(onPressed: onPressed, child: Text(label)),
    );
  }
}

class _CharPainter extends CustomPainter {
  _CharPainter({
    required this.strokes,
    required this.gridSize,
    required this.phase,
    required this.done,
    required this.showHint,
    required this.watchProgress,
    required this.inking,
    required this.rejected,
    required this.ink,
    required this.guide,
    required this.accent,
    required this.error,
    required this.paper,
  });

  final List<List<Offset>> strokes;
  final double gridSize;
  final _Phase phase;
  final int done;
  final bool showHint;

  /// Watch phase: how many strokes have been drawn, with a fraction.
  final double watchProgress;
  final List<Offset> inking;
  final List<Offset>? rejected;
  final Color ink;
  final Color guide;
  final Color accent;
  final Color error;
  final Color paper;

  @override
  void paint(Canvas canvas, Size size) {
    final scale = size.width / gridSize;
    Offset px(Offset p) => p * scale;
    Path pathOf(List<Offset> pts) {
      final path = Path()..moveTo(px(pts.first).dx, px(pts.first).dy);
      for (final p in pts.skip(1)) {
        path.lineTo(px(p).dx, px(p).dy);
      }
      return path;
    }

    Paint line(Color color, double width) => Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = width
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;

    final box = Rect.fromLTWH(0, 0, size.width, size.height);
    canvas.drawRRect(
      RRect.fromRectAndRadius(box, const Radius.circular(12)),
      Paint()..color = paper,
    );
    final cross = line(guide.withValues(alpha: 0.5), 1);
    canvas.drawLine(Offset(size.width / 2, 8), Offset(size.width / 2, size.height - 8), cross);
    canvas.drawLine(Offset(8, size.height / 2), Offset(size.width - 8, size.height / 2), cross);

    final thick = size.width * 0.05;

    void number(int n, Offset at, Color color) {
      final tp = TextPainter(
        text: TextSpan(
          text: '$n',
          style: TextStyle(color: color, fontSize: size.width * 0.06, fontWeight: FontWeight.bold),
        ),
        textDirection: TextDirection.ltr,
      )..layout();
      tp.paint(canvas, px(at) - Offset(tp.width / 2 + 8, tp.height / 2 + 8));
    }

    void dot(Offset at) {
      canvas.drawCircle(px(at), size.width * 0.025, Paint()..color = Colors.green);
    }

    if (phase == _Phase.watch) {
      for (var i = 0; i < strokes.length; i++) {
        final fraction = (watchProgress - i).clamp(0.0, 1.0);
        if (fraction <= 0) continue;
        final pts = partialPath(strokes[i], fraction);
        canvas.drawPath(pathOf(pts), line(ink, thick));
        number(i + 1, strokes[i].first, accent);
      }
      return;
    }

    if (phase == _Phase.trace) {
      for (var i = done; i < strokes.length; i++) {
        canvas.drawPath(pathOf(strokes[i]), line(guide, thick));
        number(i + 1, strokes[i].first, guide);
      }
    }
    if (done < strokes.length && (phase == _Phase.trace || showHint)) {
      canvas.drawPath(pathOf(strokes[done]), line(accent.withValues(alpha: 0.35), thick));
      dot(strokes[done].first);
    }
    for (var i = 0; i < done; i++) {
      canvas.drawPath(pathOf(strokes[i]), line(ink, thick * 0.8));
    }
    if (rejected != null && rejected!.length > 1) {
      canvas.drawPath(
        Path()..addPolygon(rejected!, false),
        line(error.withValues(alpha: 0.7), thick * 0.6),
      );
    }
    if (inking.length > 1) {
      canvas.drawPath(Path()..addPolygon(inking, false), line(accent, thick * 0.6));
    }
  }

  @override
  bool shouldRepaint(_CharPainter old) => true;
}
