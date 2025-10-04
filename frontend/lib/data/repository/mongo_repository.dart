import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:mongo_dart/mongo_dart.dart';

class MongoRepository {
  MongoRepository._internal({Future<Db> Function()? dbFactory})
    : _dbFactory = dbFactory ?? (() => Db.create(dotenv.get('MONGODB_URI')));

  static final MongoRepository _instance = MongoRepository._internal();

  factory MongoRepository({Future<Db> Function()? dbFactory}) {
    if (dbFactory != null) {
      _instance._dbFactory = dbFactory;
    }
    return _instance;
  }

  Future<Db> Function()? _dbFactory;
  Db? _db;

  Future<Db> connect() async {
    if (_db != null && _db!.isConnected) {
      return _db!;
    }

    final db = await _dbFactory!();
    if (!db.isConnected) {
      await db.open(secure: true, tlsAllowInvalidCertificates: true);
    }
    _db = db;
    return db;
  }
}
