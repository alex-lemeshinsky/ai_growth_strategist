import 'package:freezed_annotation/freezed_annotation.dart';

import '../../../domain/entities/task_entity.dart';

part 'analyze_state.freezed.dart';

@freezed
abstract class AnalyzeState with _$AnalyzeState {
  const factory AnalyzeState({
    @Default(false) bool isLoading,
    @Default(false) bool isAnalyzing,
    String? taskId,
    TaskEntity? task,
    String? error,
    @Default(<TaskEntity>[]) List<TaskEntity> completedTasks,
    @Default(false) bool isLoadingCompletedTasks,
  }) = _AnalyzeState;

  const AnalyzeState._();
}
