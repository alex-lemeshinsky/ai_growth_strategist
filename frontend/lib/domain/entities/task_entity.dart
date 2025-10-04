import 'package:freezed_annotation/freezed_annotation.dart';

part 'task_entity.freezed.dart';
part 'task_entity.g.dart';

@freezed
abstract class TaskEntity with _$TaskEntity {
  const factory TaskEntity({
    @JsonKey(name: 'task_id') required String taskId,
    required String url,
    required String status,
    @JsonKey(name: 'page_name') String? pageName,
    @JsonKey(name: 'page_id') String? pageId,
    @JsonKey(name: 'total_ads') int? totalAds,
    @JsonKey(name: 'html_report') String? htmlReport,
  }) = _TaskEntity;

  const TaskEntity._();

  factory TaskEntity.fromJson(Map<String, dynamic> json) => _$TaskEntityFromJson(json);
}
