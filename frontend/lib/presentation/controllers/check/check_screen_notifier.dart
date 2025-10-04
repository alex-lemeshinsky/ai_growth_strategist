import 'dart:async';

import 'package:cross_file/cross_file.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../data/repository/google_drive_repository.dart';
import 'check_screen_state.dart';

final checkScreenProvider =
    NotifierProvider<CheckScreenNotifier, CheckScreenState>(
  CheckScreenNotifier.new,
);

class CheckScreenNotifier extends Notifier<CheckScreenState> {
  static const _folderId = '11rTyyKmSJKhC7QvH1RnmjxagFlw56I9F';

  final GoogleDriveRepository _repository = GoogleDriveRepository();

  @override
  CheckScreenState build() {
    Future.microtask(_loadDriveFiles);
    return const CheckScreenState();
  }

  void setSegment(CheckSegment segment) {
    if (state.segment == segment) {
      return;
    }
    state = state.copyWith(segment: segment);
    if (segment == CheckSegment.myVideos &&
        state.driveFiles.isEmpty &&
        !state.isLoadingFiles) {
      unawaited(_loadDriveFiles());
    }
  }

  void setHovering(bool hovering) {
    if (state.isHovering == hovering) {
      return;
    }
    state = state.copyWith(isHovering: hovering);
  }

  void clearSelection() {
    state = state.copyWith(
      selectedVideoName: null,
      selectedVideoSize: null,
      errorMessage: null,
    );
  }

  void registerVideo({required String name, int? sizeInBytes}) {
    state = state.copyWith(
      selectedVideoName: name,
      selectedVideoSize: sizeInBytes,
      segment: CheckSegment.uploadVideo,
      errorMessage: null,
    );
  }

  Future<void> handleDroppedFiles(List<XFile> files) async {
    if (files.isEmpty) {
      return;
    }
    final file = files.first;
    int? size;
    try {
      size = await file.length();
    } catch (_) {
      size = null;
    }
    registerVideo(name: file.name, sizeInBytes: size);
  }

  Future<void> pickVideo() async {
    try {
      final result = await FilePicker.platform.pickFiles(type: FileType.video);
      if (result == null || result.files.isEmpty) {
        return;
      }
      final file = result.files.first;
      registerVideo(name: file.name, sizeInBytes: file.size);
    } catch (_) {
      state = state.copyWith(errorMessage: 'Unable to access media library.');
    }
  }

  Future<void> refreshDriveFiles() => _loadDriveFiles(force: true);

  Future<void> _loadDriveFiles({bool force = false}) async {
    if (state.isLoadingFiles && !force) {
      return;
    }

    state = state.copyWith(isLoadingFiles: true, driveError: null);

    try {
      final files = await _repository.listAllFilesInFolder(folderId: _folderId);
      state = state.copyWith(
        isLoadingFiles: false,
        driveFiles: files,
      );
    } catch (error) {
      state = state.copyWith(
        isLoadingFiles: false,
        driveError:
            'Failed to load your Google Drive files. Please try again. (${error.toString()})',
      );
    }
  }
}
