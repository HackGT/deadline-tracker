from pymongo import MongoClient

from app.config import CONFIG

def _getConnection():
    dbConfig = CONFIG.mongo
    conn = MongoClient(host=dbConfig['HOST'], port=int(dbConfig['PORT']))
    return conn[dbConfig['DB']]

CONNECTION = _getConnection()
