from pymongo import MongoClient
from flask import Flask, request, render_template, jsonify
import jwt, datetime

app = Flask(__name__)

# MongoDB
client = MongoClient('localhost', 27017)
db = client.typejungle

SECRET_KEY = "JUNGLE"

# [html 뷰어]
@app.route('/')
def start():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/result')
def result():
    return render_template('result.html')

# [회원가입 API]
@app.route('/api/signup', methods=['POST'])
def api_signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    check_receive = request.form['check_give']
    
    if not id_receive:
        return jsonify({'result': 'fail', 'msg': '아이디를 입력해주세요'})
    
    if not pw_receive:
        return jsonify({'result': 'fail', 'msg': '비밀번호를 입력해주세요'})
    
    if pw_receive != check_receive:
        return jsonify({'result': 'fail', 'msg': '비밀번호를 다시 확인해주세요'})
    
    check = db.users.find_one({'id': id_receive})
    if check is not None:
        return jsonify({'result': 'fail', 'msg': '중복된 id가 존재합니다'})
        
    db.users.insert_one({'id': id_receive, 'pw': pw_receive})
    return jsonify({'result': 'success'})


# [로그인 API]
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    
    result = db.users.find_one({'id': id_receive, 'pw': pw_receive})

    if result:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1000)
        }
        # token을 클라이언트에게 전달.
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있음.
@app.route('/api/token', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        # token을 시크릿키로 디코딩
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'result': 'success', 'id': payload['id']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

# [랭킹 API]
@app.route('/api/rank', methods=['GET'])
def api_rank():
    ranking_ls = list(db.ranking.find({}, {'_id': False}).sort('score', 1))
    if len(ranking_ls) > 10:
        top10_ls = ranking_ls[:10]
    else:
        top10_ls = ranking_ls
    return jsonify({'rank': top10_ls})

# [로그 API]
@app.route('/api/log', methods=['POST'])
def api_log():
    id_receive = request.form['id_give']
    score_receive = int(request.form['score_give'])
    db.log.insert_one({'id':id_receive, 'score': score_receive, 'time': datetime.datetime.now()})

    result = db.ranking.find_one({'id':id_receive})
    if result is not None:
        db.ranking.delete_one({'id': id_receive})
        score_receive = min(result['score'], score_receive)
    db.ranking.insert_one({'id': id_receive, 'score': score_receive})
    return jsonify({'result': 'success'})

# [결과 API]
@app.route('/api/score', methods=['GET'])
def api_score():
    name = request.args.get('id_give')
    score = list(db.log.find({'id':name}, {'_id': False}))
    return jsonify({'score': score[-1]})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug = True)