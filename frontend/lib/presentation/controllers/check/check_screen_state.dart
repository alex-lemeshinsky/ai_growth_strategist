import 'package:freezed_annotation/freezed_annotation.dart';

part 'check_screen_state.freezed.dart';

enum CheckSegment { myVideos, uploadVideo }

@freezed
class CheckScreenState with _$CheckScreenState {
  const factory CheckScreenState({
    @Default(CheckSegment.myVideos) CheckSegment segment,
    @Default(false) bool isHovering,
    String? selectedVideoName,
    int? selectedVideoSize,
    String? errorMessage,
  }) = _CheckScreenState;

  const CheckScreenState._();

  bool get hasSelection => selectedVideoName != null;
}
