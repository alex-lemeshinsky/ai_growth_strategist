import 'package:desktop_drop/desktop_drop.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../controllers/check/check_screen_notifier.dart';
import '../../controllers/check/check_screen_state.dart';

class CheckScreen extends ConsumerWidget {
  const CheckScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);
    final state = ref.watch(checkScreenProvider);
    final notifier = ref.read(checkScreenProvider.notifier);

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          DecoratedBox(
            decoration: BoxDecoration(
              color: theme.colorScheme.surface,
              borderRadius: BorderRadius.circular(28),
              border: Border.all(color: theme.colorScheme.outlineVariant),
            ),
            child: SegmentedButton<CheckSegment>(
              segments: const [
                ButtonSegment(
                  value: CheckSegment.myVideos,
                  label: Text('My videos'),
                  icon: Icon(Icons.video_library_outlined),
                ),
                ButtonSegment(
                  value: CheckSegment.uploadVideo,
                  label: Text('Upload video'),
                  icon: Icon(Icons.cloud_upload_outlined),
                ),
              ],
              showSelectedIcon: false,
              selected: {state.segment},
              onSelectionChanged: (selection) =>
                  notifier.setSegment(selection.first),
              style: ButtonStyle(
                elevation: WidgetStateProperty.all(0),
                shape: WidgetStateProperty.all(
                  RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(24)),
                ),
                backgroundColor: WidgetStateProperty.resolveWith(
                  (states) => states.contains(WidgetState.selected)
                      ? theme.colorScheme.primary
                      : Colors.transparent,
                ),
                foregroundColor: WidgetStateProperty.resolveWith(
                  (states) => states.contains(WidgetState.selected)
                      ? theme.colorScheme.onPrimary
                      : theme.colorScheme.onSurfaceVariant,
                ),
                overlayColor: WidgetStateProperty.all(
                  theme.colorScheme.primary.withValues(alpha: 0.08),
                ),
              ),
            ),
          ),
          const SizedBox(height: 32),
          Expanded(
            child: AnimatedSwitcher(
              duration: const Duration(milliseconds: 250),
              child: state.segment == CheckSegment.myVideos
                  ? _MyVideosPlaceholder(theme: theme)
                  : const UploadVideoForm(),
            ),
          ),
        ],
      ),
    );
  }
}

class _MyVideosPlaceholder extends StatelessWidget {
  const _MyVideosPlaceholder({required this.theme});

  final ThemeData theme;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        key: const ValueKey('my-videos'),
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.auto_awesome_motion,
              size: 48, color: theme.colorScheme.primary),
          const SizedBox(height: 16),
          Text(
            'Your generated videos will appear here.',
            style: theme.textTheme.titleMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),
          Text(
            'Track performance and request new variations in seconds.',
            style: theme.textTheme.bodyMedium
                ?.copyWith(color: theme.colorScheme.onSurfaceVariant),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}

class UploadVideoForm extends ConsumerWidget {
  const UploadVideoForm({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);
    final state = ref.watch(checkScreenProvider);
    final notifier = ref.read(checkScreenProvider.notifier);

    return DropTarget(
      onDragEntered: (_) => notifier.setHovering(true),
      onDragExited: (_) => notifier.setHovering(false),
      onDragDone: (details) async {
        notifier.setHovering(false);
        await notifier.handleDroppedFiles(details.files);
      },
      child: AnimatedContainer(
        key: const ValueKey('upload-video'),
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 40),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(24),
          border: Border.all(
            color: state.isHovering
                ? theme.colorScheme.primary
                : theme.colorScheme.outlineVariant,
            width: 1.6,
          ),
          color: state.isHovering
              ? theme.colorScheme.primary.withValues(alpha: 0.05)
              : theme.colorScheme.surface,
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.cloud_upload_rounded,
                size: 54, color: theme.colorScheme.primary),
            const SizedBox(height: 18),
            Text(
              'Drop your video here',
              style: theme.textTheme.titleMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            Text(
              'MP4, MOV, or WEBM • up to 500MB',
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: notifier.pickVideo,
              icon: const Icon(Icons.video_file_outlined),
              label: const Text('Select video from device'),
              style: ElevatedButton.styleFrom(
                padding:
                    const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(14)),
              ),
            ),
            if (state.selectedVideoName != null) ...[
              const SizedBox(height: 24),
              _SelectedVideoTile(
                name: state.selectedVideoName!,
                size: state.selectedVideoSize,
                onClear: notifier.clearSelection,
              ),
            ],
            if (state.errorMessage != null) ...[
              const SizedBox(height: 16),
              Text(
                state.errorMessage!,
                style: theme.textTheme.bodySmall
                    ?.copyWith(color: theme.colorScheme.error),
                textAlign: TextAlign.center,
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class _SelectedVideoTile extends StatelessWidget {
  const _SelectedVideoTile(
      {required this.name, this.size, required this.onClear});

  final String name;
  final int? size;
  final VoidCallback onClear;

  String get _readableSize {
    if (size == null || size == 0) {
      return '';
    }
    const units = ['B', 'KB', 'MB', 'GB'];
    var value = size!.toDouble();
    var unitIndex = 0;
    while (value >= 1024 && unitIndex < units.length - 1) {
      value /= 1024;
      unitIndex++;
    }
    return '${value.toStringAsFixed(value < 10 ? 1 : 0)} ${units[unitIndex]}';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(18),
        color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.4),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.max,
        children: [
          Container(
            decoration: BoxDecoration(
              color: theme.colorScheme.primary.withValues(alpha: 0.12),
              borderRadius: BorderRadius.circular(12),
            ),
            padding: const EdgeInsets.all(12),
            child: Icon(Icons.play_circle_fill,
                color: theme.colorScheme.primary, size: 24),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  name,
                  style: theme.textTheme.bodyLarge
                      ?.copyWith(fontWeight: FontWeight.w600),
                  overflow: TextOverflow.ellipsis,
                ),
                if (_readableSize.isNotEmpty)
                  Text(
                    _readableSize,
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: theme.colorScheme.onSurfaceVariant,
                    ),
                  ),
              ],
            ),
          ),
          const SizedBox(width: 12),
          IconButton(
            onPressed: onClear,
            icon: const Icon(Icons.close_rounded),
            tooltip: 'Remove video',
          ),
        ],
      ),
    );
  }
}
