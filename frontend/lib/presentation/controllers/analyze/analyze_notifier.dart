import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../data/models/parse_ads_request_model.dart';
import '../../../data/repository/remote_repository.dart';
import 'analyze_state.dart';

final analyzeProvider = NotifierProvider<AnalyzeNotifier, AnalyzeState>(AnalyzeNotifier.new);

class AnalyzeNotifier extends Notifier<AnalyzeState> {
  late final RemoteRepository _remoteRepository;
  Timer? _pollingTimer;

  @override
  AnalyzeState build() {
    _remoteRepository = ref.read(remoteRepositoryProvider);
    ref.onDispose(() {
      _pollingTimer?.cancel();
    });
    return const AnalyzeState();
  }

  Future<void> parseAds(String url) async {
    final trimmed = url.trim();
    if (trimmed.isEmpty) {
      state = state.copyWith(error: 'Please enter a Facebook Ads Library URL.');
      return;
    }

    state = state.copyWith(isLoading: true, error: null);
    try {
      final response = await _remoteRepository.parseAds(ParseAdsRequestModel(url: trimmed));
      final taskId = response['task_id']?.toString();

      state = state.copyWith(isLoading: false, taskId: taskId, task: null, isAnalyzing: true);

      if (taskId != null && taskId.isNotEmpty) {
        await _fetchTask(taskId, setLoading: false);
        _startPolling(taskId);
      }
    } catch (error) {
      state = state.copyWith(isLoading: false, error: error.toString());
    }
  }

  Future<void> fetchTask([String? taskId]) async {
    await _fetchTask(taskId, setLoading: true);
  }

  Future<void> analyzeCreatives(String taskId) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final response = await _remoteRepository.analyzeCreatives(taskId);
      state = state.copyWith(
        isLoading: false,
        task: state.task,
        error: response['message']?.toString(),
      );
    } catch (error) {
      state = state.copyWith(isLoading: false, error: error.toString());
    }
  }

  Future<void> _fetchTask(String? taskId, {required bool setLoading}) async {
    final id = (taskId ?? state.taskId)?.trim();
    if (id == null || id.isEmpty) {
      state = state.copyWith(error: 'No task id specified.');
      return;
    }

    if (setLoading) {
      state = state.copyWith(isLoading: true, error: null);
    }

    try {
      final task = await _remoteRepository.getTaskEntity(id);
      final isCompleted = task.status.toUpperCase() == 'COMPLETED';

      state = state.copyWith(
        isLoading: false,
        error: null,
        task: task,
        taskId: id,
        isAnalyzing: !isCompleted,
      );

      if (isCompleted) {
        _pollingTimer?.cancel();
      }
    } catch (error) {
      _pollingTimer?.cancel();
      state = state.copyWith(isLoading: false, error: error.toString());
    }
  }

  void _startPolling(String taskId) {
    _pollingTimer?.cancel();
    _pollingTimer = Timer.periodic(const Duration(seconds: 5), (_) {
      _fetchTask(taskId, setLoading: false);
    });
  }
}
