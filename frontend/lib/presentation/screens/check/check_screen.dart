import 'package:desktop_drop/desktop_drop.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../controllers/check/check_screen_notifier.dart';
import '../../controllers/check/check_screen_state.dart';

class CheckScreen extends ConsumerStatefulWidget {
  const CheckScreen({super.key});

  @override
  ConsumerState<CheckScreen> createState() => _CheckScreenState();
}

class _CheckScreenState extends ConsumerState<CheckScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) {
        return;
      }
      ref.read(checkScreenProvider.notifier).loadPolicyTasks();
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final state = ref.watch(checkScreenProvider);
    final notifier = ref.read(checkScreenProvider.notifier);

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            children: [
              Expanded(
                child: DecoratedBox(
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
                      ButtonSegment(
                        value: CheckSegment.policyReports,
                        label: Text('Policy reports'),
                        icon: Icon(Icons.policy_outlined),
                      ),
                    ],
                    showSelectedIcon: false,
                    selected: {state.segment},
                    onSelectionChanged: (selection) => notifier.setSegment(selection.first),
                    style: ButtonStyle(
                      elevation: WidgetStateProperty.all(0),
                      shape: WidgetStateProperty.all(
                        RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
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
              ),
              if (state.segment == CheckSegment.myVideos) ...[
                const SizedBox(width: 12),
                OutlinedButton.icon(
                  onPressed: state.isLoadingFiles ? null : () => notifier.refreshDriveFiles(),
                  icon: state.isLoadingFiles
                      ? const SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.refresh),
                  label: const Text('Refresh'),
                ),
              ] else if (state.segment == CheckSegment.policyReports) ...[
                const SizedBox(width: 12),
                OutlinedButton.icon(
                  onPressed: state.isLoadingPolicyTasks
                      ? null
                      : () => notifier.loadPolicyTasks(force: true),
                  icon: state.isLoadingPolicyTasks
                      ? const SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.refresh),
                  label: const Text('Refresh'),
                ),
              ],
            ],
          ),
          const SizedBox(height: 32),
          Expanded(
            child: AnimatedSwitcher(
              duration: const Duration(milliseconds: 250),
              child: switch (state.segment) {
                CheckSegment.myVideos =>
                  state.hasDriveAccess
                      ? _MyVideosView(
                          key: const ValueKey('drive-view'),
                          state: state,
                          onRefresh: notifier.refreshDriveFiles,
                        )
                      : _DriveConnectPrompt(
                          key: const ValueKey('drive-connect'),
                          isLoading: state.isLoadingFiles,
                          error: state.driveError,
                          onConnect: notifier.connectDrive,
                        ),
                CheckSegment.uploadVideo => const UploadVideoForm(),
                CheckSegment.policyReports => const _PolicyReportsView(),
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _MyVideosView extends StatelessWidget {
  const _MyVideosView({super.key, required this.state, required this.onRefresh});

  final CheckScreenState state;
  final Future<void> Function() onRefresh;

  @override
  Widget build(BuildContext context) {
    if (state.isLoadingFiles) {
      return const Center(child: CircularProgressIndicator());
    }

    if (state.driveError != null) {
      return _DriveErrorView(message: state.driveError!, onRetry: onRefresh);
    }

    if (state.driveFiles.isEmpty) {
      return const _EmptyDrivePlaceholder();
    }

    return RefreshIndicator(
      onRefresh: onRefresh,
      child: ListView.separated(
        physics: const AlwaysScrollableScrollPhysics(),
        itemCount: state.driveFiles.length,
        separatorBuilder: (_, __) => const SizedBox(height: 12),
        padding: const EdgeInsets.only(bottom: 16),
        itemBuilder: (context, index) {
          final file = state.driveFiles[index];
          final modified = file.modifiedTime != null
              ? 'Updated ${file.modifiedTime!.toLocal().toString().split('.').first}'
              : 'Google Drive file';
          return Card(
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: Theme.of(context).colorScheme.primary.withValues(alpha: 0.12),
                child: const Icon(Icons.insert_drive_file_outlined),
              ),
              title: Text(file.name),
              subtitle: Text(modified),
              trailing: Text(
                file.mimeType,
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

class _EmptyDrivePlaceholder extends StatelessWidget {
  const _EmptyDrivePlaceholder();

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Center(
      child: Column(
        key: const ValueKey('my-videos-empty'),
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.auto_awesome_motion, size: 48, color: theme.colorScheme.primary),
          const SizedBox(height: 16),
          Text(
            'Your generated videos will appear here.',
            style: theme.textTheme.titleMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),
          Text(
            'Track performance and request new variations in seconds.',
            style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}

class _PolicyReportsView extends ConsumerWidget {
  const _PolicyReportsView();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(checkScreenProvider);
    final notifier = ref.read(checkScreenProvider.notifier);
    final theme = Theme.of(context);
    final baseUrl = dotenv.get('BASE_URL');

    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                Text('Policy Report History', style: theme.textTheme.titleMedium),
                const Spacer(),
                IconButton(
                  tooltip: 'Refresh',
                  onPressed: state.isLoadingPolicyTasks
                      ? null
                      : () => notifier.loadPolicyTasks(force: true),
                  icon: state.isLoadingPolicyTasks
                      ? const SizedBox(
                          width: 18,
                          height: 18,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.refresh),
                ),
              ],
            ),
            const SizedBox(height: 12),
            if (state.policyTasksError != null)
              _PolicyTasksError(
                message: state.policyTasksError!,
                onRetry: () => notifier.loadPolicyTasks(force: true),
              )
            else if (state.isLoadingPolicyTasks)
              const Center(child: CircularProgressIndicator())
            else if (state.policyTasks.isEmpty)
              Text(
                'No policy reports yet. Completed policy checks will appear here.',
                style: theme.textTheme.bodySmall,
              )
            else
              Expanded(
                child: ListView.separated(
                  itemCount: state.policyTasks.length,
                  itemBuilder: (context, index) {
                    final task = state.policyTasks[index];
                    final title = (task.pageName?.trim().isNotEmpty ?? false)
                        ? task.pageName!.trim()
                        : 'Task ${task.taskId}';
                    final reportUrl = '$baseUrl/report/policy/${task.taskId}';

                    return ListTile(
                      contentPadding: EdgeInsets.zero,
                      title: Text(title, maxLines: 1, overflow: TextOverflow.ellipsis),
                      subtitle: Text(task.status, style: theme.textTheme.bodySmall),
                      trailing: const Icon(Icons.open_in_new),
                      onTap: () => _openPolicyReport(context, reportUrl),
                    );
                  },
                  separatorBuilder: (_, __) => const Divider(height: 1),
                ),
              ),
          ],
        ),
      ),
    );
  }

  Future<void> _openPolicyReport(BuildContext context, String url) async {
    final uri = Uri.parse(url);
    final messenger = ScaffoldMessenger.of(context);
    if (!await launchUrl(uri, mode: LaunchMode.externalApplication)) {
      messenger.showSnackBar(SnackBar(content: Text('Unable to open report URL: $url')));
    }
  }
}

class _PolicyTasksError extends StatelessWidget {
  const _PolicyTasksError({required this.message, required this.onRetry});

  final String message;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(message, style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.error)),
        const SizedBox(height: 8),
        TextButton.icon(
          onPressed: onRetry,
          icon: const Icon(Icons.refresh),
          label: const Text('Try again'),
        ),
      ],
    );
  }
}

class _DriveConnectPrompt extends StatelessWidget {
  const _DriveConnectPrompt({
    super.key,
    required this.isLoading,
    required this.onConnect,
    this.error,
  });

  final bool isLoading;
  final VoidCallback onConnect;
  final String? error;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 420),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.cloud_sync_outlined, size: 48, color: theme.colorScheme.primary),
            const SizedBox(height: 16),
            Text(
              'Connec Google Drive',
              textAlign: TextAlign.center,
              style: theme.textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Text(
              'All your generated videos will be stored in Google Drive.',
              textAlign: TextAlign.center,
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: isLoading ? null : onConnect,
              icon: isLoading
                  ? const SizedBox(
                      width: 16,
                      height: 16,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.lock_open_rounded),
              label: const Text('Connect Google Drive'),
            ),
            if (error != null) ...[
              const SizedBox(height: 12),
              Text(
                error!,
                textAlign: TextAlign.center,
                style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.error),
              ),
            ],
          ],
        ),
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
            color: state.isHovering ? theme.colorScheme.primary : theme.colorScheme.outlineVariant,
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
            Icon(Icons.cloud_upload_rounded, size: 54, color: theme.colorScheme.primary),
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
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
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
                style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.error),
                textAlign: TextAlign.center,
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class _DriveErrorView extends StatelessWidget {
  const _DriveErrorView({required this.message, required this.onRetry});

  final String message;
  final Future<void> Function() onRetry;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.error_outline, size: 48, color: theme.colorScheme.error),
          const SizedBox(height: 16),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Text(
              message,
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
          ),
          const SizedBox(height: 16),
          ElevatedButton.icon(
            onPressed: () => onRetry(),
            icon: const Icon(Icons.refresh),
            label: const Text('Try again'),
          ),
        ],
      ),
    );
  }
}

class _SelectedVideoTile extends StatelessWidget {
  const _SelectedVideoTile({required this.name, this.size, required this.onClear});

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
            child: Icon(Icons.play_circle_fill, color: theme.colorScheme.primary, size: 24),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  name,
                  style: theme.textTheme.bodyLarge?.copyWith(fontWeight: FontWeight.w600),
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
