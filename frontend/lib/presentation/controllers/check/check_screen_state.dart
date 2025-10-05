import 'package:freezed_annotation/freezed_annotation.dart';

import '../../../data/repository/google_drive_repository.dart';
import '../../../domain/entities/task_entity.dart';

part 'check_screen_state.freezed.dart';

enum CheckSegment { myVideos, uploadVideo, policyReports }

@freezed
abstract class CheckScreenState with _$CheckScreenState {
  const factory CheckScreenState({
    @Default(CheckSegment.myVideos) CheckSegment segment,
    @Default(false) bool isHovering,
    @Default(false) bool hasDriveAccess,
    String? selectedVideoName,
    int? selectedVideoSize,
    String? errorMessage,
    @Default(<DriveFile>[]) List<DriveFile> driveFiles,
    @Default(false) bool isLoadingFiles,
    String? driveError,
    @Default(<TaskEntity>[]) List<TaskEntity> policyTasks,
    @Default(false) bool isLoadingPolicyTasks,
    String? policyTasksError,
  }) = _CheckScreenState;

  const CheckScreenState._();

  bool get hasSelection => selectedVideoName != null;
}
