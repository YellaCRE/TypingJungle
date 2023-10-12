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
    check_receive = request.form['check_give']
    
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

    if result is not None:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# [랭킹 API]
@app.route('/api/rank', methods=['GET'])
def api_rank():
    cursor = db.ranking.aggregate([
        {"$sort": {"score": 1}},
        {"$group": {
            "_id": "$id",
            "unique_ids": {"$addToSet": "$_id"},
            "count": {"$sum": 1}
            }},
        {"$match": {"count": { "$gte": 2 }}}
    ])
    
    for doc in list(cursor):
        for id in doc['unique_ids'][1:]:
            db.ranking.delete_one({'_id': id})
    
    ranking_ls = list(db.ranking.find({}, {'_id': False}).sort("score"))
    if len(ranking_ls) > 10:
        top10_ls = ranking_ls[:10]
    else:
        top10_ls = ranking_ls
    
    return jsonify({'rank': top10_ls})

# [결과 API]
@app.route('/api/score', methods=['GET'])
def api_score():
    name = request.args.get('id')
    score = db.log.find_one({'id':name}, {'_id': False})
    return jsonify({'score': score})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug = True)