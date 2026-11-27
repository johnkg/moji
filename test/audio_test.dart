import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:moji/services/course_loader.dart';
import 'package:moji/services/deck_loader.dart';
import 'package:moji/services/speaker.dart';

// Run from the project root: flutter test

class _FakeSpeaker implements Speaker {
  final List<String> spoken = [];

  @override
  Future<bool> speak(String text, String lang) async {
    spoken.add('$lang:$text');
    return true;
  }
}

ClipManifest _readManifest() {
  final raw = File('assets/audio/manifest.json').readAsStringSync();
  final clips = (jsonDecode(raw) as Map<String, dynamic>)['clips'] as Map<String, dynamic>;
  return {
    for (final e in clips.entries) e.key: (e.value as Map<String, dynamic>).cast<String, String>(),
  };
}

/// Every (language, text) the app can speak: flashcards, lesson items and lesson words.
Set<String> _spokenTexts() {
  final out = <String>{};
  for (final name in deckFiles) {
    final deck = parseDeck(File('assets/decks/$name.json').readAsStringSync());
    for (final card in deck.cards) {
      out.add('${deck.lang}|${card.front}');
    }
  }
  for (final name in courseFiles) {
    final course = parseCourse(File('assets/lessons/$name.json').readAsStringSync());
    for (final unit in course.units) {
      for (final item in unit.items) {
        out.add('${course.lang}|${item.front}');
      }
      for (final word in unit.words) {
        out.add('${course.lang}|${word.text}');
      }
    }
  }
  return out;
}

void main() {
  // A lone small tsu or long mark has no sound of its own, so no clip.
  const silent = {'ー', 'っ', 'ッ'};

  test('every text the app speaks has a recorded clip', () {
    final manifest = _readManifest();
    final missing = <String>[];
    for (final key in _spokenTexts()) {
      final lang = key.split('|').first;
      final text = key.substring(lang.length + 1);
      if (silent.contains(text)) continue;
      if (manifest[lang]?[text] == null) missing.add(key);
    }
    expect(missing, isEmpty, reason: 'regenerate with tool/gen_audio.py');
  });

  test('every manifest entry points at a real, non-empty mp3', () {
    final manifest = _readManifest();
    expect(manifest.keys.toSet(), {'ja', 'zh'});
    for (final lang in manifest.keys) {
      for (final entry in manifest[lang]!.entries) {
        final file = File('assets/audio/$lang/${entry.value}.mp3');
        expect(file.existsSync(), isTrue, reason: '$lang ${entry.key}');
        expect(file.lengthSync(), greaterThan(1000), reason: '$lang ${entry.key}');
      }
    }
  });

  group('RecordedSpeaker', () {
    final manifest = Future.value(<String, Map<String, String>>{
      'ja': {'こんにちは': 'abc123'},
    });

    test('plays the clip when there is one', () async {
      final fallback = _FakeSpeaker();
      final played = <String>[];
      final speaker = RecordedSpeaker(
        fallback: fallback,
        manifest: manifest,
        play: (path) async => played.add(path),
      );
      expect(await speaker.speak('こんにちは', 'ja'), isTrue);
      expect(played, ['audio/ja/abc123.mp3']);
      expect(fallback.spoken, isEmpty);
    });

    test('uses the device voice when there is no clip', () async {
      final fallback = _FakeSpeaker();
      final played = <String>[];
      final speaker = RecordedSpeaker(
        fallback: fallback,
        manifest: manifest,
        play: (path) async => played.add(path),
      );
      await speaker.speak('さようなら', 'ja');
      await speaker.speak('こんにちは', 'zh');
      expect(played, isEmpty);
      expect(fallback.spoken, ['ja:さようなら', 'zh:こんにちは']);
    });

    test('uses the device voice when playback fails', () async {
      final fallback = _FakeSpeaker();
      final speaker = RecordedSpeaker(
        fallback: fallback,
        manifest: manifest,
        play: (path) async => throw StateError('no audio device'),
      );
      expect(await speaker.speak('こんにちは', 'ja'), isTrue);
      expect(fallback.spoken, ['ja:こんにちは']);
    });
  });
}
