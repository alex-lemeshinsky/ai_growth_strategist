import 'package:flutter_test/flutter_test.dart';
import 'package:mongo_dart/mongo_dart.dart';

import 'package:frontend/data/repository/mongo_repository.dart';

class _FakeDb extends Db {
  _FakeDb() : super('mongodb://localhost:27017/test');

  bool opened = false;

  @override
  Future open({
    WriteConcern writeConcern = WriteConcern.acknowledged,
    bool secure = false,
    bool tlsAllowInvalidCertificates = false,
    String? tlsCAFile,
    String? tlsCertificateKeyFile,
    String? tlsCertificateKeyFilePassword,
  }) async {
    opened = true;
  }
}

void main() {
  group('MongoRepository', () {
    test('connect returns an open Db instance', () async {
      final fakeDb = _FakeDb();
      final repository = MongoRepository(dbFactory: () async => fakeDb);

      final db = await repository.connect();

      expect(db, equals(fakeDb));
      expect(fakeDb.opened, isTrue);
    });

    test('connect reuses existing open connection', () async {
      final fakeDb = _FakeDb();
      final repository = MongoRepository(dbFactory: () async => fakeDb);

      final first = await repository.connect();
      final second = await repository.connect();

      expect(identical(first, second), isTrue);
    });
  });
}
