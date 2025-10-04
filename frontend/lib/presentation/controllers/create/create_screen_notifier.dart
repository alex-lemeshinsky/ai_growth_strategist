import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../../data/models/generate_video_request_model.dart';
import '../../../data/repository/mongo_repository.dart';
import '../../../data/repository/remote_repository.dart';
import 'create_screen_state.dart';

final createScreenProvider = NotifierProvider<CreateScreenNotifier, CreateScreenState>(
  CreateScreenNotifier.new,
);

class CreateScreenNotifier extends Notifier<CreateScreenState> {
  late final RemoteRepository _remoteRepository;
  final MongoRepository _mongoRepository = MongoRepository();
  Timer? _pollingTimer;

  @override
  CreateScreenState build() {
    _remoteRepository = ref.read(remoteRepositoryProvider);
    ref.onDispose(() {
      _pollingTimer?.cancel();
    });
    return const CreateScreenState();
  }

  void updatePrompt(String value) {
    state = state.copyWith(prompt: value, errorMessage: null);
  }

  Future<bool> submitPrompt() async {
    final trimmedPrompt = state.prompt.trim();
    if (trimmedPrompt.isEmpty || state.isSubmitting) {
      return false;
    }

    state = state.copyWith(
      isSubmitting: true,
      errorMessage: null,
      generatedFileUrl: null,
      lastKnownStatus: 'Queued',
    );

    try {
      final request = GenerateVideoRequestModel(input: trimmedPrompt, images: const []);
      final taskId = await _remoteRepository.generateVideo(request);
      state = state.copyWith(
        prompt: '',
        lastSubmittedPrompt: trimmedPrompt,
        taskId: taskId,
        isGenerating: true,
        lastKnownStatus: 'Started',
      );
      _startGenerationPolling(taskId);
      return true;
    } catch (_) {
      state = state.copyWith(
        errorMessage: 'Unable to submit prompt. Please try again.',
        isGenerating: false,
      );
      return false;
    } finally {
      state = state.copyWith(isSubmitting: false);
    }
  }

  void _startGenerationPolling(String taskId) {
    _pollingTimer?.cancel();
    _pollingTimer = Timer.periodic(const Duration(seconds: 5), (_) async {
      try {
        final db = await _mongoRepository.connect();
        final collection = db.collection('Generation');
        final document = await collection.findOne({'taskId': taskId});

        if (document == null) {
          return;
        }

        final status = (document['status'] as String?)?.trim();
        final fileUrl = (document['fileUrl'] as String?)?.trim();

        if (status != null && status != state.lastKnownStatus) {
          state = state.copyWith(lastKnownStatus: status);
        }

        if (fileUrl != null && fileUrl.isNotEmpty) {
          _pollingTimer?.cancel();
          state = state.copyWith(isGenerating: false, generatedFileUrl: fileUrl);
          await _openFileUrl(fileUrl);
        } else if (status != null && status.toLowerCase() == 'completed') {
          _pollingTimer?.cancel();
          state = state.copyWith(isGenerating: false);
        }
      } catch (error) {
        _pollingTimer?.cancel();
        state = state.copyWith(
          isGenerating: false,
          errorMessage: 'Failed to check generation status. $error',
        );
      }
    });
  }

  Future<void> _openFileUrl(String url) async {
    final uri = Uri.parse(url);
    final launched = await launchUrl(uri, mode: LaunchMode.externalApplication);
    if (!launched) {
      state = state.copyWith(errorMessage: 'Generated file available at $url (unable to open).');
    }
  }
}
