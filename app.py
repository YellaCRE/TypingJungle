from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import *
from pymongo import MongoClient

app = Flask(import_name= __name__)

app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "JUNGLE"
)

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.dbjungle
users_collection = db["users"]


jwt = JWTManager(app)

# 사용자 모델 정의
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route("/")
def test_test():
    return "<h1> Hello, I'm IML!</h1>"

#로그인 엔드포인트
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # MongoDB에서 사용자를 조회
    user = users_collection.find_one({'username': username, 'password': password})
    
    if user:
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200
    else:
        return {'message': '유효하지 않음'}, 401

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)