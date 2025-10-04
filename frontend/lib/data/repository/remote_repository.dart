import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;

import '../models/generate_video_request_model.dart';

final remoteRepositoryProvider = Provider<RemoteRepository>((ref) {
  final client = http.Client();
  ref.onDispose(client.close);
  return RemoteRepository(client);
});

class RemoteRepository {
  RemoteRepository(this._client);

  final http.Client _client;

  static final Uri _endpoint = Uri.parse(
    'https://itsurkan4.app.n8n.cloud/webhook-test/5628f961-d272-4368-88aa-67dff5efa0d9',
  );

  Future<String> generateVideo(GenerateVideoRequestModel payload) async {
    final response = await _client.post(
      _endpoint,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(payload.toJson()),
    );

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw http.ClientException(
        'Failed to trigger video generation (${response.statusCode}): ${response.body}',
        _endpoint,
      );
    }

    try {
      final Map<String, dynamic> data = jsonDecode(response.body) as Map<String, dynamic>;
      final value = data['taskId'];
      if (value is String && value.isNotEmpty) {
        return value;
      }
    } catch (_) {
      // ignore and fall back to raw body
    }
    return response.body;
  }
}
