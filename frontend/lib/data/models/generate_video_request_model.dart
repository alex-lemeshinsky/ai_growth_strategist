import 'package:json_annotation/json_annotation.dart';

part 'generate_video_request_model.g.dart';

@JsonSerializable(createFactory: false, createToJson: true)
class GenerateVideoRequestModel {
  const GenerateVideoRequestModel({required this.input, required this.images});

  final String input;
  final List<String> images;

  Map<String, dynamic> toJson() => _$GenerateVideoRequestModelToJson(this);
}
