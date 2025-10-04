import 'dart:async';

import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:googleapis/drive/v3.dart' as drive;
import 'package:googleapis_auth/auth_io.dart' as auth;
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';

/// A lightweight value object representing a Google Drive file.
class DriveFile {
  DriveFile({
    required this.id,
    required this.name,
    required this.mimeType,
    this.modifiedTime,
    this.iconLink,
    this.thumbnailLink,
  });

  factory DriveFile.fromApi(drive.File file) => DriveFile(
        id: file.id ?? '',
        name: file.name ?? 'Untitled',
        mimeType: file.mimeType ?? 'application/octet-stream',
        modifiedTime: file.modifiedTime,
        iconLink: file.iconLink,
        thumbnailLink: file.thumbnailLink,
      );

  final String id;
  final String name;
  final String mimeType;
  final DateTime? modifiedTime;
  final String? iconLink;
  final String? thumbnailLink;
}

/// Signature used to surface the OAuth consent URL to the user interface.
typedef ConsentPrompt = FutureOr<void> Function(Uri consentUrl);

/// Repository responsible for interacting with the Google Drive API.
///
/// The repository relies on `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
/// entries inside the `.env` file. Make sure to call `dotenv.load()` before
/// constructing this class (typically in `main()`).
class GoogleDriveRepository {
  GoogleDriveRepository._internal({
    ConsentPrompt? promptUserForConsent,
    http.Client? httpClient,
  })  : _baseClient = httpClient ?? http.Client(),
        _promptUserForConsent =
            promptUserForConsent ?? GoogleDriveRepository._defaultConsentPrompt;

  factory GoogleDriveRepository({ConsentPrompt? promptUserForConsent}) {
    if (promptUserForConsent != null) {
      _instance._promptUserForConsent = promptUserForConsent;
    }
    return _instance;
  }

  static final GoogleDriveRepository _instance =
      GoogleDriveRepository._internal();

  static const _scopes = <String>[drive.DriveApi.driveReadonlyScope];

  ConsentPrompt _promptUserForConsent;
  final http.Client _baseClient;

  auth.AuthClient? _authorizedClient;

  /// Returns a page of files from the user's Drive.
  ///
  /// [folderId] can be provided to scope the query to a single folder.
  /// [pageSize] controls the number of items per call (max 1000 per API).
  /// [pageToken] supports pagination with the token returned from the
  /// previous invocation.
  Future<drive.FileList> listFiles({
    String? folderId,
    int pageSize = 100,
    String? pageToken,
  }) async {
    final client = await _obtainAuthorizedClient();
    final driveApi = drive.DriveApi(client);

    final buffer = StringBuffer('trashed = false');
    if (folderId != null && folderId.isNotEmpty) {
      buffer
        ..write(" and '")
        ..write(folderId)
        ..write("' in parents");
    }

    return driveApi.files.list(
      q: buffer.toString(),
      pageSize: pageSize.clamp(1, 1000),
      pageToken: pageToken,
      $fields:
          'files(id,name,mimeType,modifiedTime,iconLink,thumbnailLink),nextPageToken',
      orderBy: 'modifiedTime desc',
      spaces: 'drive',
    );
  }

  /// Convenience helper to convert the API response into strongly typed
  /// [DriveFile] instances.
  Future<List<DriveFile>> listDriveFiles({
    String? folderId,
    int pageSize = 100,
    String? pageToken,
  }) async {
    final response = await listFiles(
        folderId: folderId, pageSize: pageSize, pageToken: pageToken);
    final files = response.files ?? const <drive.File>[];
    return files.map(DriveFile.fromApi).toList(growable: false);
  }

  Future<List<DriveFile>> listAllFilesInFolder(
      {required String folderId}) async {
    final files = <DriveFile>[];
    String? token;

    do {
      final response =
          await listFiles(folderId: folderId, pageSize: 1000, pageToken: token);
      final pageFiles = response.files ?? const <drive.File>[];
      files.addAll(pageFiles.map(DriveFile.fromApi));
      token = response.nextPageToken;
    } while (token != null && token.isNotEmpty);

    return files;
  }

  Future<auth.AuthClient> _obtainAuthorizedClient() async {
    if (_authorizedClient != null) {
      return _authorizedClient!;
    }

    if (!dotenv.isInitialized) {
      try {
        await dotenv.load(isOptional: true);
      } catch (error, stackTrace) {
        Error.throwWithStackTrace(
          StateError('Unable to load environment configuration: $error'),
          stackTrace,
        );
      }
    }

    final clientIdValue = dotenv.maybeGet('GOOGLE_CLIENT_ID');
    final clientSecretValue = dotenv.maybeGet('GOOGLE_CLIENT_SECRET');

    if (clientIdValue == null || clientIdValue.isEmpty) {
      throw StateError(
        'GOOGLE_CLIENT_ID is missing. Add it to your .env file or set it as an environment variable.',
      );
    }

    if (clientSecretValue == null || clientSecretValue.isEmpty) {
      throw StateError(
        'GOOGLE_CLIENT_SECRET is missing. Add it to your .env file or set it as an environment variable.',
      );
    }

    final clientId = auth.ClientId(clientIdValue, clientSecretValue);

    _authorizedClient = await auth.clientViaUserConsent(
      clientId,
      _scopes,
      (url) {
        final result = _promptUserForConsent(Uri.parse(url));
        if (result is Future) {
          unawaited(result);
        }
      },
      baseClient: _baseClient,
    );

    return _authorizedClient!;
  }

  static Future<void> _defaultConsentPrompt(Uri uri) async {
    final augmentedParams = Map<String, String>.from(uri.queryParameters)
      ..putIfAbsent('access_type', () => 'offline')
      ..putIfAbsent('prompt', () => 'consent');
    final authUri = uri.replace(queryParameters: augmentedParams);

    final launched = await launchUrl(
      authUri,
      mode: LaunchMode.externalApplication,
    );

    if (!launched) {
      throw StateError('Unable to open Google authorization screen.');
    }
  }
}
