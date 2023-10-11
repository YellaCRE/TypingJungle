from pymongo import MongoClient
from flask import Flask, request, render_template, jsonify, redirect, url_for

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
    nickname_receive = request.form['nickname_give']
    
    db.users.insert_one({'pid': 1234,'id': id_receive, 'pw': pw_receive, 'name': nickname_receive})
    return jsonify({'result': 'success'})


# [로그인 API]
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    
    result = db.users.find_one({'id': id_receive, 'pw': pw_receive})

    if result is not None:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# [랭킹 API]
@app.route('/api/rank', methods=['GET'])
def api_rank():
    ranking_ls = list(db.ranking.find({}, {'_id': False}))
    if len(ranking_ls) > 10:
        top10_ls = ranking_ls[:10]
    else:
        top10_ls = ranking_ls
    
    return jsonify({'rank': top10_ls})

@app.route('/api/score', methods=['GET'])
def api_score():
    pid = request.args.get('pid')
    score = db.log.find_one({'pid':pid}, {'_id': False})
    print(score)
    return jsonify({'score': score})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug = True)