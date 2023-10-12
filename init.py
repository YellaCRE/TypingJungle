import random
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.typejungle


def mkdb():
    # userDB
    db.users.insert_one({'id': 'admin', 'pw': 'admin'})

    # rankingDB
    db.ranking.insert_one({'id': 'bot1','score': 2000})
    db.ranking.insert_one({'id': 'bot2','score': 3000})
    db.ranking.insert_one({'id': 'bot3','score': 4000})
    db.ranking.insert_one({'id': 'bot4','score': 5000})
    db.ranking.insert_one({'id': 'bot5','score': 6000})



if __name__ == '__main__':
    # 초기화
    db.users.drop()
    db.ranking.drop()
    db.log.drop()

    # db 생성
    mkdb()
