import random
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)
db = client.typejungle                    # 'dbjungle'라는 이름의 db를 만듭니다.


def mkdb():
    # userDB
    db.users.insert_one({'pid': '1234','name': 'hwang', 'id': 'id123', 'pw': 'pw123'})
    db.users.insert_one({'pid': '1235','name': 'choi', 'id': 'id123', 'pw': 'pw123'})
    db.users.insert_one({'pid': '1236','name': 'yang', 'id': 'id123', 'pw': 'pw123'})

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
