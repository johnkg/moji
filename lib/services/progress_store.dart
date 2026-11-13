import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../srs/scheduler.dart';

/// Where progress is kept. Swap for SQLite or cloud sync later.
abstract class ProgressStore {
  /// Flashcard review state by card key.
  Future<Map<String, CardState>> load();
  Future<void> save(Map<String, CardState> progress);

  /// Keys of finished lesson units.
  Future<Set<String>> loadCompletedUnits();
  Future<void> saveCompletedUnits(Set<String> units);
}

class SharedPrefsProgressStore implements ProgressStore {
  static const String _key = 'progress_v1';
  static const String _unitsKey = 'units_done_v1';

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

  @override
  Future<Set<String>> loadCompletedUnits() async {
    final prefs = await SharedPreferences.getInstance();
    return (prefs.getStringList(_unitsKey) ?? const <String>[]).toSet();
  }

  @override
  Future<void> saveCompletedUnits(Set<String> units) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setStringList(_unitsKey, units.toList());
  }
}
