import 'package:flutter/material.dart';

class AnalyzeScreen extends StatelessWidget {
  const AnalyzeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text(
        'Analyze',
        style: Theme.of(context).textTheme.headlineMedium,
      ),
    );
  }
}
