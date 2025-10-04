import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_html/flutter_html.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../controllers/analyze/analyze_notifier.dart';

class AnalyzeScreen extends ConsumerStatefulWidget {
  const AnalyzeScreen({super.key});

  @override
  ConsumerState<AnalyzeScreen> createState() => _AnalyzeScreenState();
}

class _AnalyzeScreenState extends ConsumerState<AnalyzeScreen> {
  final TextEditingController _urlController = TextEditingController();
  String? _lastSeenTaskId;

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(analyzeProvider);
    final notifier = ref.read(analyzeProvider.notifier);
    final theme = Theme.of(context);

    if (_lastSeenTaskId != state.taskId) {
      if (_lastSeenTaskId == null && state.taskId != null) {
        _urlController.clear();
      }
      _lastSeenTaskId = state.taskId;
    }

    if (state.taskId == null) {
      return Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 520),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                'Analyze Ads',
                textAlign: TextAlign.center,
                style: theme.textTheme.headlineMedium,
              ),
              const SizedBox(height: 24),
              TextField(
                controller: _urlController,
                decoration: const InputDecoration(
                  labelText: 'Facebook Ads Library URL',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: state.isLoading
                    ? null
                    : () {
                        FocusScope.of(context).unfocus();
                        notifier.parseAds(_urlController.text);
                      },
                child: state.isLoading
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text('Submit'),
              ),
              if (state.error != null) ...[
                const SizedBox(height: 12),
                Text(
                  state.error!,
                  textAlign: TextAlign.center,
                  style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.error),
                ),
              ],
            ],
          ),
        ),
      );
    }

    final task = state.task;
    final isCompleted = task?.status.toUpperCase() == 'COMPLETED';
    final htmlReport = task?.htmlReport;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text('Task ID: ${state.taskId}', style: theme.textTheme.titleMedium),
          const SizedBox(height: 16),
          Text('Status: ${task?.status ?? 'unknown'}', style: theme.textTheme.bodyMedium),
          const SizedBox(height: 16),
          if (state.error != null)
            Text(
              state.error!,
              style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.error),
            )
          else if (isCompleted && htmlReport != null && htmlReport.isNotEmpty)
            Expanded(
              child: Center(
                child: SingleChildScrollView(
                  child: Html(
                    data: htmlReport,
                    style: {
                      "h1": Style(color: Colors.black),
                      "strong": Style(color: Colors.black),
                      "div.meta": Style(color: Colors.black),
                    },
                  ),
                ),
              ),
            )
          else if (task != null)
            LinearProgressIndicator()
          else
            Text('No task details loaded yet.', style: theme.textTheme.bodyMedium),
        ],
      ),
    );
  }
}
