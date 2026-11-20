import 'dart:io';
import 'dart:ui' show Offset;

import 'package:flutter_test/flutter_test.dart';
import 'package:moji/services/course_loader.dart';
import 'package:moji/writing/strokes.dart';

// Run from the project root: flutter test

List<Offset> _line(Offset a, Offset b, [int steps = 10]) =>
    [for (var i = 0; i <= steps; i++) Offset.lerp(a, b, i / steps)!];

void main() {
  final kana = StrokeData.parse(File('assets/strokes/ja_kana.json').readAsStringSync());
  final hanzi = StrokeData.parse(File('assets/strokes/zh_hanzi.json').readAsStringSync());
  final data = kana.merge(hanzi);

  group('strokeMatches', () {
    final model = _line(const Offset(20, 20), const Offset(90, 20));
    const size = 109.0;

    test('accepts the exact stroke', () {
      expect(strokeMatches(model, model, size), isTrue);
    });

    test('accepts a wobbly stroke that starts and ends near the right places', () {
      final drawn = _line(const Offset(28, 30), const Offset(80, 14));
      expect(strokeMatches(drawn, model, size), isTrue);
    });

    test('rejects a stroke drawn in the wrong direction', () {
      expect(strokeMatches(model.reversed.toList(), model, size), isFalse);
    });

    test('rejects a stroke that starts in the wrong place', () {
      final drawn = _line(const Offset(20, 80), const Offset(90, 80));
      expect(strokeMatches(drawn, model, size), isFalse);
    });

    test('rejects a tiny scribble and a single point', () {
      expect(strokeMatches(_line(const Offset(20, 20), const Offset(30, 20)), model, size), isFalse);
      expect(strokeMatches(const [Offset(20, 20)], model, size), isFalse);
    });

    test('ignores direction for closed shapes', () {
      final loop = [
        const Offset(50, 20),
        const Offset(80, 50),
        const Offset(50, 80),
        const Offset(20, 50),
        const Offset(50, 22),
      ];
      expect(strokeMatches(loop.reversed.toList(), loop, size), isTrue);
    });
  });

  test('partialPath returns the first part of a path', () {
    final path = _line(const Offset(0, 0), const Offset(100, 0));
    final half = partialPath(path, 0.5);
    expect(half.first, const Offset(0, 0));
    expect(half.last.dx, closeTo(50, 0.001));
    expect(partialPath(path, 1), path);
  });

  test('every kana and Mandarin hanzi taught in a lesson has stroke data', () {
    for (final name in courseFiles) {
      if (name.contains('speaking')) continue;
      final source = File('assets/lessons/$name.json').readAsStringSync();
      final course = parseCourse(source);
      for (final unit in course.units) {
        for (final item in unit.items) {
          expect(data.has(item.front), isTrue, reason: item.front);
        }
      }
    }
  });

  test('stroke data looks sane: each stroke has a start and end inside the grid', () {
    expect(kana.chars.length, 92);
    expect(hanzi.size, kana.size);
    for (final entry in data.chars.entries) {
      for (final stroke in entry.value) {
        expect(stroke.length, greaterThan(1), reason: entry.key);
        for (final p in [stroke.first, stroke.last]) {
          expect(p.dx, inInclusiveRange(0, data.size), reason: entry.key);
          expect(p.dy, inInclusiveRange(0, data.size), reason: entry.key);
        }
      }
    }
  });
}
