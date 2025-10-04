// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/app/app.dart';

void main() {
  testWidgets('Create tab shows prompt input', (WidgetTester tester) async {
    await tester
        .pumpWidget(const ProviderScope(child: AIGrowthStrategistApp()));

    expect(find.text('Analyze'), findsOneWidget);

    await tester.tap(find.text('Create'));
    await tester.pumpAndSettle();

    expect(find.text('Create'), findsWidgets);
    expect(find.byType(TextField), findsOneWidget);
    final sendButton = find.byTooltip('Submit prompt');
    expect(sendButton, findsOneWidget);
  });
}
