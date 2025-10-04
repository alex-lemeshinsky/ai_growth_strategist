import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../controllers/create/create_screen_notifier.dart';
import '../../controllers/create/create_screen_state.dart';

class CreateScreen extends ConsumerStatefulWidget {
  const CreateScreen({super.key});

  @override
  ConsumerState<CreateScreen> createState() => _CreateScreenState();
}

class _CreateScreenState extends ConsumerState<CreateScreen> {
  late final TextEditingController _promptController;

  @override
  void initState() {
    super.initState();
    _promptController = TextEditingController();
    ref.listenManual<CreateScreenState>(createScreenProvider, (previous, next) {
      if (previous?.isSubmitting == true && !next.isSubmitting) {
        if (!mounted) return;
        final messenger = ScaffoldMessenger.of(context);

        if (next.errorMessage != null && next.errorMessage!.isNotEmpty) {
          messenger.showSnackBar(SnackBar(content: Text(next.errorMessage!)));
        } else if (previous?.lastSubmittedPrompt != next.lastSubmittedPrompt &&
            next.lastSubmittedPrompt != null) {
          messenger.showSnackBar(const SnackBar(content: Text('Prompt sent for generation.')));
        }
      }
    });
  }

  @override
  void dispose() {
    _promptController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(createScreenProvider);
    final notifier = ref.read(createScreenProvider.notifier);

    if (_promptController.text != state.prompt) {
      _promptController.value = TextEditingValue(
        text: state.prompt,
        selection: TextSelection.collapsed(offset: state.prompt.length),
      );
    }

    final theme = Theme.of(context);

    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 720),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text('Create', textAlign: TextAlign.center, style: theme.textTheme.headlineMedium),
              const SizedBox(height: 24),
              Stack(
                children: [
                  TextField(
                    controller: _promptController,
                    onChanged: notifier.updatePrompt,
                    minLines: 8,
                    maxLines: 16,
                    textInputAction: TextInputAction.newline,
                    decoration: InputDecoration(
                      hintText:
                          'Describe the marketing video you want to generate...\nInclude audience, offer, tone, and any must-have beats.',
                      alignLabelWithHint: true,
                      filled: true,
                      fillColor: theme.colorScheme.surface,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(18)),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(18),
                        borderSide: BorderSide(color: theme.colorScheme.primary, width: 2),
                      ),
                      contentPadding: const EdgeInsets.fromLTRB(22, 24, 78, 24),
                    ),
              ),
              Positioned(
                bottom: 16,
                right: 16,
                child: IconButton.filled(
                      onPressed: state.canSubmit
                          ? () async {
                              FocusScope.of(context).unfocus();
                              await notifier.submitPrompt();
                            }
                          : null,
                      icon: state.isSubmitting
                          ? const SizedBox(
                              height: 18,
                              width: 18,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : const Icon(Icons.send_rounded),
                      tooltip: 'Submit prompt',
                ),
              ),
            ],
          ),
          if (state.isGenerating || state.taskId != null) ...[
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(16),
                color: theme.colorScheme.primary.withValues(alpha: 0.08),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      state.isGenerating
                          ? const SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : Icon(Icons.check_circle,
                              color: theme.colorScheme.primary),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          state.isGenerating
                              ? 'Generating video variations… hang tight.'
                              : 'Generation triggered successfully.',
                          style: theme.textTheme.bodyMedium,
                        ),
                      ),
                    ],
                  ),
                  if (state.lastKnownStatus != null) ...[
                    const SizedBox(height: 8),
                    Text(
                      'Status: ${state.lastKnownStatus}',
                      style: theme.textTheme.bodySmall,
                    ),
                  ],
                  if (state.generatedFileUrl != null) ...[
                    const SizedBox(height: 12),
                    TextButton.icon(
                      onPressed: () => _openGeneratedFile(state.generatedFileUrl!),
                      icon: const Icon(Icons.open_in_new),
                      label: const Text('Open generated video'),
                    ),
                  ],
                ],
              ),
            ),
          ],
        ],
      ),
        ),
      ),
    );
  }

  Future<void> _openGeneratedFile(String url) async {
    final uri = Uri.parse(url);
    final launched = await launchUrl(uri, mode: LaunchMode.externalApplication);
    if (!launched && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Unable to open generated file. URL: $url')),
      );
    }
  }
}
