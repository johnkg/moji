import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../srs/scheduler.dart';

/// Where review progress is kept. Swap for SQLite or cloud sync later.
abstract class ProgressStore {
  Future<Map<String, CardState>> load();
  Future<void> save(Map<String, CardState> progress);
}

class SharedPrefsProgressStore implements ProgressStore {
  static const String _key = 'progress_v1';

  @override
  Future<Map<String, CardState>> load() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_key);
    if (raw == null) return {};
    final decoded = jsonDecode(raw) as Map<String, dynamic>;
    return decoded.map(
      (key, value) => MapEntry(key, CardState.fromJson(value as Map<String, dynamic>)),
    );
  }

  @override
  Future<void> save(Map<String, CardState> progress) async {
    final prefs = await SharedPreferences.getInstance();
    final encoded = jsonEncode(progress.map((key, value) => MapEntry(key, value.toJson())));
    await prefs.setString(_key, encoded);
  }
}
