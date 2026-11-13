import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

import '../models/course.dart';

/// Course files under assets/lessons/. Add new courses here.
const List<String> courseFiles = [
  'ja_hiragana_course',
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
