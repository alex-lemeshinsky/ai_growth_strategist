import 'package:freezed_annotation/freezed_annotation.dart';

part 'task_entity.freezed.dart';
part 'task_entity.g.dart';

@freezed
abstract class TaskEntity with _$TaskEntity {
  @JsonSerializable(fieldRename: FieldRename.snake)
  const factory TaskEntity({
    required String taskId,
    required String status,
    String? pageName,
    String? pageId,
    int? totalAds,
    String? htmlReport,
  }) = _TaskEntity;

  factory TaskEntity.fromJson(Map<String, dynamic> json) => _$TaskEntityFromJson(json);
}
