import 'package:flutter/material.dart';

import 'app_state.dart';
import 'screens/home_screen.dart';
import 'services/progress_store.dart';
import 'services/speaker.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MojiApp());
}

class MojiApp extends StatefulWidget {
  const MojiApp({super.key});

  @override
  State<MojiApp> createState() => _MojiAppState();
}

class _MojiAppState extends State<MojiApp> {
  late final AppState _app = AppState(
    store: SharedPrefsProgressStore(),
    speaker: TtsSpeaker(),
  );
  late final Future<void> _loading = _app.load();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Moji',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(colorSchemeSeed: Colors.teal, useMaterial3: true),
      home: FutureBuilder<void>(
        future: _loading,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return Scaffold(
              body: Center(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Text('Could not load: ${snapshot.error}'),
                ),
              ),
            );
          }
          if (snapshot.connectionState != ConnectionState.done) {
            return const Scaffold(body: Center(child: CircularProgressIndicator()));
          }
          return HomeScreen(app: _app);
        },
      ),
    );
  }
}
