import 'dart:convert';

import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;

import '../models/generate_video_request_model.dart';
import '../models/parse_ads_request_model.dart';
import '../../domain/entities/task_entity.dart';

final remoteRepositoryProvider = Provider<RemoteRepository>((ref) {
  final client = http.Client();
  ref.onDispose(client.close);
  return RemoteRepository(client: client);
});

class RemoteRepository {
  RemoteRepository({required http.Client client, Uri? baseUri})
    : _client = client,
      _baseUri = baseUri ?? Uri.parse(dotenv.get("BASE_URL"));

  final http.Client _client;
  final Uri _baseUri;

  Uri _resolve(String path, [Map<String, dynamic>? query]) {
    final normalized = path.startsWith('/') ? path : '/$path';
    final uri = _baseUri.resolve(normalized);
    if (query == null || query.isEmpty) {
      return uri;
    }
    return uri.replace(
      queryParameters: {
        ...uri.queryParameters,
        ...query.map((key, value) => MapEntry(key, value.toString())),
      },
    );
  }

  Map<String, dynamic> _decodeOrThrow(Uri uri, http.Response response) {
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw http.ClientException(
        'Request to $uri failed with ${response.statusCode}: ${response.body}',
        uri,
      );
    }

    if (response.body.isEmpty) {
      return const {};
    }

    final decoded = jsonDecode(response.body);
    if (decoded is Map<String, dynamic>) {
      return decoded;
    }
    if (decoded is List<dynamic>) {
      return {'data': decoded};
    }
    return {'data': decoded.toString()};
  }

  Future<Map<String, dynamic>> _postJson(Uri uri, Map<String, dynamic> body) async {
    final response = await _client.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(body),
    );
    return _decodeOrThrow(uri, response);
  }

  Future<String> generateVideo(GenerateVideoRequestModel payload) async {
    final uri = Uri.parse(dotenv.get("GENERATE_VIDEO_HOOK_URL"));
    final result = await _postJson(uri, payload.toJson());
    return result['taskId']?.toString() ?? result['task_id']?.toString() ?? '';
  }

  Future<Map<String, dynamic>> parseAds(ParseAdsRequestModel payload) =>
      _postJson(_resolve('/api/v1/parse-ads'), payload.toJson());

  Future<Map<String, dynamic>> debugParseAds(ParseAdsRequestModel payload) =>
      _postJson(_resolve('/api/v1/debug-parse'), payload.toJson());

  Future<List<dynamic>> listTasks({int skip = 0, int limit = 20, String? status}) async {
    final query = <String, dynamic>{'skip': skip, 'limit': limit};
    if (status != null && status.isNotEmpty) {
      query['status'] = status;
    }
    final uri = _resolve('/api/v1/tasks', query);
    final decoded = _decodeOrThrow(uri, await _client.get(uri));
    final data = decoded['data'];
    if (data is List) {
      return data;
    }
    if (decoded['items'] is List) {
      return decoded['items'] as List<dynamic>;
    }
    return const [];
  }

  Future<Map<String, dynamic>> getTask(String taskId) async {
    final uri = _resolve('/api/v1/task/$taskId');
    final res = _decodeOrThrow(uri, await _client.get(uri));
    return res['task'] ?? res;
  }

  Future<TaskEntity> getTaskEntity(String taskId) async {
    final json = await getTask(taskId);
    return TaskEntity.fromJson(json);
  }

  Future<Map<String, dynamic>> analyzeCreatives(String taskId) async {
    final uri = _resolve('/api/v1/analyze-creatives/$taskId');
    return _postJson(uri, const {});
  }

  Future<Map<String, dynamic>> healthCheck() async {
    final uri = _resolve('/api/v1/health');
    return _decodeOrThrow(uri, await _client.get(uri));
  }

  Future<Map<String, dynamic>> root() async {
    final uri = _resolve('/');
    return _decodeOrThrow(uri, await _client.get(uri));
  }
}
