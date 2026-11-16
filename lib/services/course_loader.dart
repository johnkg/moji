import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

import '../models/course.dart';

/// Course files under assets/lessons/. Add new courses here.
/// Speaking paths come first so they show above reading on the home screen.
const List<String> courseFiles = [
  'ja_speaking_course',
  'ja_hiragana_course',
  'zh_speaking_course',
  'zh_basics_course',
];

Course parseCourse(String source) {
  return Course.fromJson(jsonDecode(source) as Map<String, dynamic>);
}

Future<List<Course>> loadCourses() async {
  final courses = <Course>[];
  for (final name in courseFiles) {
    final source = await rootBundle.loadString('assets/lessons/$name.json');
    courses.add(parseCourse(source));
  }
  return courses;
}
