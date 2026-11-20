import 'dart:convert';
import 'dart:ui' show Offset;

import 'package:flutter/services.dart' show rootBundle;

/// Stroke order of characters, on a square grid of [size] units.
/// Data: KanjiVG, (c) Ulrich Apel, CC BY-SA 3.0. See assets/strokes/README.txt.
class StrokeData {
  const StrokeData({required this.size, required this.chars});

  static const StrokeData empty = StrokeData(size: 109, chars: {});

  final double size;

  /// Character -> strokes in writing order -> points along the stroke.
  final Map<String, List<List<Offset>>> chars;

  bool has(String char) => chars[char]?.isNotEmpty ?? false;

  List<List<Offset>> strokesOf(String char) => chars[char] ?? const [];

  factory StrokeData.parse(String source) {
    final json = jsonDecode(source) as Map<String, dynamic>;
    final raw = json['chars'] as Map<String, dynamic>;
    return StrokeData(
      size: (json['size'] as num).toDouble(),
      chars: {
        for (final entry in raw.entries)
          entry.key: [
            for (final stroke in entry.value as List<dynamic>)
              [
                for (final p in stroke as List<dynamic>)
                  Offset((p[0] as num).toDouble(), (p[1] as num).toDouble()),
              ],
          ],
      },
    );
  }
}

Future<StrokeData> loadStrokes() async {
  final source = await rootBundle.loadString('assets/strokes/ja_kana.json');
  return StrokeData.parse(source);
}

double pathLength(List<Offset> points) {
  var total = 0.0;
  for (var i = 1; i < points.length; i++) {
    total += (points[i] - points[i - 1]).distance;
  }
  return total;
}

/// The first [fraction] (0 to 1) of [points], measured along its length.
List<Offset> partialPath(List<Offset> points, double fraction) {
  if (points.length < 2 || fraction >= 1) return points;
  if (fraction <= 0) return [points.first];
  final target = pathLength(points) * fraction;
  final out = <Offset>[points.first];
  var walked = 0.0;
  for (var i = 1; i < points.length; i++) {
    final seg = (points[i] - points[i - 1]).distance;
    if (walked + seg >= target) {
      final t = seg == 0 ? 0.0 : (target - walked) / seg;
      out.add(Offset.lerp(points[i - 1], points[i], t)!);
      return out;
    }
    out.add(points[i]);
    walked += seg;
  }
  return out;
}

/// A forgiving check of one stroke, both paths in grid units. It passes when
/// the stroke starts and ends near the right places, heads the right way,
/// and is not just a tiny scribble. The exact shape is not compared.
bool strokeMatches(List<Offset> drawn, List<Offset> model, double size) {
  if (drawn.length < 2 || model.length < 2) return false;
  final tolerance = size * 0.28;
  if ((drawn.first - model.first).distance > tolerance) return false;
  if ((drawn.last - model.last).distance > tolerance) return false;

  final modelLength = pathLength(model);
  if (pathLength(drawn) < modelLength * 0.35) return false;

  // Direction only matters when the model does not return to where it began.
  final want = model.last - model.first;
  if (want.distance > size * 0.12) {
    final got = drawn.last - drawn.first;
    if (got.distance == 0) return false;
    final cosine = (want.dx * got.dx + want.dy * got.dy) / (want.distance * got.distance);
    if (cosine < 0.2) return false;
  }
  return true;
}
