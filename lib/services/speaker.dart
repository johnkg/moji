import 'dart:convert';

import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/foundation.dart' show debugPrint, kIsWeb;
import 'package:flutter/services.dart' show rootBundle;
import 'package:flutter_tts/flutter_tts.dart';

abstract class Speaker {
  /// Speaks [text] in [lang] ('ja' or 'zh'). Returns false if it could not.
  Future<bool> speak(String text, String lang);
}

/// Uses the device or browser text-to-speech voices.
class TtsSpeaker implements Speaker {
  final FlutterTts _tts = FlutterTts();

  static const Map<String, String> _locales = {'ja': 'ja-JP', 'zh': 'zh-CN'};

  @override
  Future<bool> speak(String text, String lang) async {
    try {
      await _tts.stop();
      await _tts.setLanguage(_locales[lang] ?? lang);
      // Slower than normal speech. The scale differs between web and mobile.
      await _tts.setSpeechRate(kIsWeb ? 0.8 : 0.4);
      await _tts.speak(text);
      return true;
    } catch (error) {
      debugPrint('TTS failed for "$text" ($lang): $error');
      return false;
    }
  }
}

/// Recorded clips by language, then by text: {'ja': {'こんにちは': 'ab12cd34ef'}}.
typedef ClipManifest = Map<String, Map<String, String>>;

/// Reads assets/audio/manifest.json, made by tool/gen_audio.py.
Future<ClipManifest> loadClipManifest() async {
  final raw = await rootBundle.loadString('assets/audio/manifest.json');
  final clips = (jsonDecode(raw) as Map<String, dynamic>)['clips'] as Map<String, dynamic>;
  return {
    for (final entry in clips.entries)
      entry.key: (entry.value as Map<String, dynamic>).cast<String, String>(),
  };
}

/// Plays a recorded voice clip when there is one for the text, and uses
/// [fallback] (the device voice) for anything without a clip or if playback fails.
class RecordedSpeaker implements Speaker {
  RecordedSpeaker({
    required this.fallback,
    required Future<ClipManifest> manifest,
    required this.play,
  }) : _manifest = manifest;

  /// The normal setup: clips from assets/audio through audioplayers, device voice as fallback.
  factory RecordedSpeaker.standard({Speaker? fallback}) {
    final player = AudioPlayer();
    return RecordedSpeaker(
      fallback: fallback ?? TtsSpeaker(),
      manifest: loadClipManifest().catchError((Object error) {
        debugPrint('Could not load the clip manifest, using the device voice: $error');
        return <String, Map<String, String>>{};
      }),
      play: (assetPath) async {
        await player.stop();
        await player.play(AssetSource(assetPath));
      },
    );
  }

  final Speaker fallback;
  final Future<ClipManifest> _manifest;

  /// Plays the asset at [assetPath], relative to the assets folder, e.g. 'audio/ja/ab12cd34ef.mp3'.
  final Future<void> Function(String assetPath) play;

  @override
  Future<bool> speak(String text, String lang) async {
    final clips = await _manifest;
    final id = clips[lang]?[text];
    if (id != null) {
      try {
        await play('audio/$lang/$id.mp3');
        return true;
      } catch (error) {
        debugPrint('Clip failed for "$text" ($lang), using the device voice: $error');
      }
    }
    return fallback.speak(text, lang);
  }
}
