import 'package:flutter/widgets.dart';

/// Japanese and Chinese share code points but draw some glyphs differently.
/// Passing the locale to Text picks the right font variant.
Locale scriptLocale(String lang) {
  return lang == 'zh' ? const Locale('zh', 'CN') : const Locale('ja', 'JP');
}

String languageName(String lang) => lang == 'zh' ? 'Mandarin' : 'Japanese';
