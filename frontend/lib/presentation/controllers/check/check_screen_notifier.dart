import 'package:cross_file/cross_file.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'check_screen_state.dart';

final checkScreenProvider =
    NotifierProvider.autoDispose<CheckScreenNotifier, CheckScreenState>(
  CheckScreenNotifier.new,
);

class CheckScreenNotifier extends Notifier<CheckScreenState> {
  @override
  CheckScreenState build() => const CheckScreenState();

  void setSegment(CheckSegment segment) {
    if (state.segment == segment) {
      return;
    }
    state = state.copyWith(segment: segment);
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
}
