import 'package:flutter/foundation.dart' show debugPrint, kIsWeb;
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
