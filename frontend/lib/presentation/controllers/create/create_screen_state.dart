import 'package:freezed_annotation/freezed_annotation.dart';

part 'create_screen_state.freezed.dart';

@freezed
abstract class CreateScreenState with _$CreateScreenState {
  const factory CreateScreenState({
    @Default('') String prompt,
    @Default(false) bool isSubmitting,
    @Default(false) bool isGenerating,
    String? errorMessage,
    String? lastSubmittedPrompt,
    String? taskId,
    String? lastKnownStatus,
    String? generatedFileUrl,
  }) = _CreateScreenState;

  const CreateScreenState._();

  bool get canSubmit =>
      prompt.trim().isNotEmpty && !isSubmitting && !isGenerating;
}
