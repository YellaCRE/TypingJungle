import random
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.typejungle


def mkdb():
    # userDB
    db.users.insert_one({'pid': '1234', 'id': 'id123', 'pw': 'pw123', 'name': 'hwang'})
    db.users.insert_one({'pid': '1235', 'id': 'id123', 'pw': 'pw123', 'name': 'choi'})
    db.users.insert_one({'pid': '1236', 'id': 'id123', 'pw': 'pw123', 'name': 'yang'})

    # rankingDB
    db.ranking.insert_one({'pid': '1234','score': '100'})
    db.ranking.insert_one({'pid': '1235','score': '1000'})
    db.ranking.insert_one({'pid': '1236','score': '10000'})
    
    # logDB
    db.log.insert_one({'pid': '1234','score': '100', 'time': '200'})


if __name__ == '__main__':
    # 초기화
    db.users.drop()
    db.ranking.drop()
    db.log.drop()

    # db 생성
    mkdb()
