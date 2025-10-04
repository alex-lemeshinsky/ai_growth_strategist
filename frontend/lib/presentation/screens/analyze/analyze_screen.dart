import 'package:flutter/material.dart';
import 'package:flutter_html/flutter_html.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';

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
    final reportUrl = state.taskId != null
        ? 'https://2c41e381b565.ngrok-free.app/report/task/${state.taskId}'
        : null;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text('Task ID: ${state.taskId}', style: theme.textTheme.titleMedium),
          const SizedBox(height: 16),
          Text('Status: ${task?.status ?? 'unknown'}', style: theme.textTheme.bodyMedium),
          if (isCompleted && reportUrl != null) ...[
            const SizedBox(height: 12),
            ElevatedButton.icon(
              onPressed: () => _openReport(reportUrl),
              icon: const Icon(Icons.open_in_new),
              label: const Text('View Report'),
            ),
          ],
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

  Future<void> _openReport(String url) async {
    final uri = Uri.parse(url);
    if (!await launchUrl(uri, mode: LaunchMode.externalApplication) && mounted) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Unable to open report URL: $url')));
    }
  }
}
