import random
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.typejungle


def mkdb():
    # userDB
    db.users.insert_one({'pid': '1', 'id': 'id1', 'pw': 'pw1', 'name': 'user1'})
    db.users.insert_one({'pid': '2', 'id': 'id2', 'pw': 'pw2', 'name': 'user2'})
    db.users.insert_one({'pid': '3', 'id': 'id3', 'pw': 'pw3', 'name': 'user3'})

    # rankingDB
    db.ranking.insert_one({'pid': '1','score': '1'})
    db.ranking.insert_one({'pid': '2','score': '2'})
    db.ranking.insert_one({'pid': '3','score': '3'})
    db.ranking.insert_one({'pid': '1','score': '4'})
    db.ranking.insert_one({'pid': '2','score': '5'})
    db.ranking.insert_one({'pid': '3','score': '6'})
    db.ranking.insert_one({'pid': '1','score': '7'})
    db.ranking.insert_one({'pid': '2','score': '8'})
    db.ranking.insert_one({'pid': '3','score': '9'})
    db.ranking.insert_one({'pid': '1','score': '10'})
    db.ranking.insert_one({'pid': '2','score': '11'})
    db.ranking.insert_one({'pid': '3','score': '12'})
    db.ranking.insert_one({'pid': '1','score': '13'})
    db.ranking.insert_one({'pid': '2','score': '14'})
    db.ranking.insert_one({'pid': '3','score': '10000'})
    db.ranking.insert_one({'pid': '1','score': '100'})
    db.ranking.insert_one({'pid': '2','score': '1000'})
    db.ranking.insert_one({'pid': '3','score': '10000'})

    
    # logDB
    db.log.insert_one({'pid': '1','score': '100', 'time': '200'})
    db.log.insert_one({'pid': '2','score': '1000', 'time': '300'})
    db.log.insert_one({'pid': '1','score': '1000', 'time': '400'})


if __name__ == '__main__':
    # 초기화
    db.users.drop()
    db.ranking.drop()
    db.log.drop()

    # db 생성
    mkdb()
