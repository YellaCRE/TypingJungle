from flask import Flask, request, render_template, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from pymongo import MongoClient

app = Flask(import_name= __name__)

app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "JUNGLE"
)

# MongoDB
client = MongoClient('localhost', 27017)
db = client.dbjungle


jwt = JWTManager(app)

# 사용자 모델 정의
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

#로그인 엔드포인트
@app.route("/")
def login_home():
    return render_template('index.html')

@app.route('/loginfunc', methods=['POST'])
def login():
    username = request.form['id']
    password = request.form['password']
    
    # MongoDB에서 사용자를 조회
    user = db.users.find_one({'name': username, 'pw': password})
    
    if user:
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200
    else:
        return {'message': '유효하지 않음'}, 401

#회원가입 엔드포인트
@app.route('/signup')
def signup_home():
    return render_template('signup.html')

@app.route('/signupfunc', methods=['POST'])
def signup():
    id = request.form["id"]
    pw = request.form["pw"]
    
    doc = {'pid': '1234', 'name': 'check', 'id': id, 'pw': pw}
    db.users.insert_one(doc)
    return jsonify({'msg': '저장 완료'})


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug = True)
    