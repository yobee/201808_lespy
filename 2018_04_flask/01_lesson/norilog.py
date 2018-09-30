import json

from datetime import datetime

from flask import Flask, render_template, redirect, request,Markup,escape # redirect,requestを追加
application = Flask(__name__)

DATA_FILE = 'norilog.json'

def save_data(start,finish,memo,created_at):
    """ 記録データを保存します。
    :param start: 乗った駅
    :type start str
    :param finish: 降りた駅
    :type finish str
    :param memo: 乗り降りメモ
    :type memo: str
    :param created_at: datetime.datetime
    :return: none
    """

    try:
        # jsonモジュールでデータベースファイルを開きます。
        database =  json.load(open(DATA_FILE,mode="r",encoding="utf-8"))
    except FileNotFoundError:
        database =[]

    database.insert(0,{
        "start": start,
        "finish":finish,
        "memo": memo,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M")
    })


    json.dump(database,open(DATA_FILE,mode="w",encoding="utf-8"),indent=4,ensure_ascii=False)


def load_data():
    try:
        database = json.load(open(DATA_FILE,mode="r",encoding="utf-8"))
    except:
        database =[]

    return database

@application.route('/')
def index():
    """
    テンプレートを表示します
    :return:
    """
    rides = load_data()

    return render_template('index.html',rides=rides)



@application.route('/save',methods=['post'])
def save():
    """記録用URL"""

    start = request.form.get('start')
    finish = request.form.get('finish')
    memo = request.form.get('memo')
    create_at = datetime.now()
    save_data(start,finish,memo,create_at)

    return redirect('/')

@application.template_filter('n12br')
def n12br_filter(s):
    """改行文字を<br>タグに置き換える"""
    return escape(s).replace('¥n',Markup('<br>'))


if __name__ == '__main__':
    application.run('0.0.0.0',8000,debug=True)