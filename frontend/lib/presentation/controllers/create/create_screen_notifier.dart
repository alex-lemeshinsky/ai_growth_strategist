import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'create_screen_state.dart';

final createScreenProvider = NotifierProvider.autoDispose<CreateScreenNotifier, CreateScreenState>(
  CreateScreenNotifier.new,
);

class CreateScreenNotifier extends Notifier<CreateScreenState> {
  @override
  CreateScreenState build() => const CreateScreenState();

  void updatePrompt(String value) {
    state = state.copyWith(prompt: value, errorMessage: null);
  }

  Future<bool> submitPrompt() async {
    final trimmedPrompt = state.prompt.trim();
    if (trimmedPrompt.isEmpty || state.isSubmitting) {
      return false;
    }

    state = state.copyWith(isSubmitting: true, errorMessage: null);

    try {
      await Future<void>.delayed(const Duration(milliseconds: 400));
      state = state.copyWith(prompt: '', lastSubmittedPrompt: trimmedPrompt);
      return true;
    } catch (_) {
      state = state.copyWith(errorMessage: 'Unable to submit prompt. Please try again.');
      return false;
    } finally {
      state = state.copyWith(isSubmitting: false);
    }
  }
}
