import 'package:json_annotation/json_annotation.dart';

part 'parse_ads_request_model.g.dart';

@JsonSerializable(fieldRename: FieldRename.snake, createFactory: false, createToJson: true)
class ParseAdsRequestModel {
  const ParseAdsRequestModel({
    required this.url,
    this.maxResults = 15,
    this.fetchAllDetails = true,
    this.outputFilename,
  });

  final String url;
  final int maxResults;
  final bool fetchAllDetails;
  final String? outputFilename;

  Map<String, dynamic> toJson() => _$ParseAdsRequestModelToJson(this);
}
