import 'package:freezed_annotation/freezed_annotation.dart';

part 'create_screen_state.freezed.dart';

@freezed
class CreateScreenState with _$CreateScreenState {
  const factory CreateScreenState({
    @Default('') String prompt,
    @Default(false) bool isSubmitting,
    String? errorMessage,
    String? lastSubmittedPrompt,
  }) = _CreateScreenState;

  const CreateScreenState._();

  bool get canSubmit => prompt.trim().isNotEmpty && !isSubmitting;
}
