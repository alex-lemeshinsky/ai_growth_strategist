import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

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
            ],
          ),
        ),
      ),
    );
  }
}
