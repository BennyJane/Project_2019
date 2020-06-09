import json
from functools import wraps

from flask import Flask, request, render_template, session, redirect, url_for, g, flash
from flask_sqlalchemy import SQLAlchemy
import os

from datetime import timedelta
from sqlCore import valid_login, valid_regist, addUser, getSite, getHotel, getManySite, getContent, sqlBase
from crawlCore import crawlCore


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/travel?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=1)
app.secret_key = 'benny jane'
db = SQLAlchemy(app)

sqlBaseFunc = sqlBase()


# 登录  ==> 闭包
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        username = session.get('username')
        print('username', username)
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))  #

    return wrapper


@app.route('/')
def index():
    # 首页
    orderSite = getSite()
    allHotel = getHotel()
    allSite = getManySite()
    # print(allSite)
    return render_template('index.html', allSite=allSite, allHotel=allHotel, orderSite=orderSite,
                           username=session.get('username'))


@app.route('/content', methods=['GET'])
@login_required
def content():
    username = session.get('username')
    if request.method == 'GET':
        siteId = request.args.get('id')
        itemInfo = getContent(siteId)
        if itemInfo:
            itemInfo = itemInfo[0]
            other_text = itemInfo.get('other')
            if other_text:
                other_text = json.loads(other_text)
                comment_category_text = ' '.join(other_text.get('comment_category'))
                itemInfo['comment_category'] = comment_category_text
            else:
                itemInfo['comment_category'] = ''
            # print(itemInfo)
            commentList = sqlBaseFunc.getComment(siteId)

            return render_template('content.html', itemInfo=itemInfo, commentList=commentList, username=username)
    return redirect(url_for('index'))


@app.route('/top')
@login_required
def top():
    # 首页
    username = session.get('username')
    print('top', username)
    ten_site, ten_hotel, ten_site_info = sqlBaseFunc.topFirst()
    picData = sqlBaseFunc.picData()
    if picData:
        picDataText = json.dumps(picData, ensure_ascii=False)
    # print(picDataText, '\n', type(picDataText))
    return render_template('top.html', username=username, ten_site=ten_site, ten_hotel=ten_hotel,
                           ten_site_info=ten_site_info, picDataText=picDataText)


@app.route('/top/hotel')
@login_required
def hotelData():
    # 首页
    username = session.get('username')
    picData = sqlBaseFunc.hotelPicData()
    if picData:
        picDataText = json.dumps(picData, ensure_ascii=False)
        # print(picDataText)
    # print(picData)
    print(picDataText, '\n', type(picDataText))
    return render_template('topHotel.html', username=username, picDataText=picDataText)


@app.route('/userList', methods=['GET'])
@login_required
def userList():
    username = session.get('username')
    if username == 'admin':
        userList = sqlBaseFunc.getUser()
    else:
        userList = sqlBaseFunc.getUserByName(username)
    return render_template('userList.html', username=username, userList=userList)


@app.route('/userList/eidt', methods=['GET','POST'])
@login_required
def userEdit():
    error = ''
    username = session.get('username')
    if request.method == 'GET':
        userId = request.args.get('id')
        if userId:
            targetUser = sqlBaseFunc.getUserById(userId)
            if targetUser:
                target_user = targetUser[0]
                return render_template('userEdit.html', username=username, target_user=target_user)
    if request.method == 'POST':
        print(request.form)
        userId = request.form.get('userId')
        name = request.form.get('name')
        password = request.form.get('password')
        second_password = request.form.get('second_password')
        print(userId, name, password)
        if password != second_password:
            error = '两次密码不一致'
        if not error:
            sqlBaseFunc.updateUserInfo(name, password, userId)
        else:
            flash(error)
    return redirect(url_for('userList'))


@app.route('/userList/delete', methods=['POST'])
@login_required
def userDel():
    userId = ''

    try:
        userId = request.args.get('id')
    except Exception:
        pass
    if userId:
        sqlBaseFunc.delUserInfo(userId)
    return redirect(url_for('userList'))


@app.route('/crawl', methods=['GET'])
@login_required
def crawl():
    username = session.get('username')
    targetList = crawlCore.crawlUrls()
    return render_template('crawl.html', username=username, targetList=targetList)


from threading import Thread


@app.route('/crawl/start', methods=['GET'])
@login_required
def crawlStart():
    if not crawlCore.isCrawling:
        crawl_task = Thread(target=crawlCore.first, args=())
        crawl_task.start()
    return redirect(url_for('crawl'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        forntEnd = dict(request.form)
        if valid_login(forntEnd['username'], forntEnd['password']):
            #   保存登录状态
            session['username'] = forntEnd.get('username')
            return redirect(url_for('index'))
        else:
            error = '错误的用户名或密码！'
        flash(error)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        forntEnd = dict(request.form)
        if forntEnd['password'] != forntEnd['password2']:
            error = '两次密码不相同！'
        elif valid_regist(forntEnd['username']):
            username = forntEnd['username']
            password = forntEnd['password']
            addUser(username, password)
            return redirect(url_for('login'))
        else:
            error = '该用户名已被注册！'
        flash(error)
    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
