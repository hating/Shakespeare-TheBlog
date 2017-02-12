# -*- encoding:utf-8 -*-
import hashlib
import json

import datetime
from flask import Flask
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
import sys
import db

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/API/allArticle')
def allArticle():
    result = db.allArticle()
    ret = []
    for i in result:
        ret.append({
            "content": i[0],
            "href": "./article/" + str(i[1])})
    return json.dumps(ret)


@app.route('/API/article/<id>')
def getArticle(id=id):
    result = db.getArticle(id)
    ret = []
    try:
        if result[0][2] != 1:
            if not verifyToken(request.cookies.get("token"))[0]:
                ret.append("# 你无权查看此文章")
                ret.append("# 你无权查看此文章")
                ret.append("# 你无权查看此文章")
                return ret
        ret.append(result[0][0])
        ret.append(result[0][1].strftime("%Y-%m-%d"))
        ret.append(result[0][3])
    except:
        ret.append("# 该文章不存在")
        ret.append("# 该文章不存在")
        ret.append("# 该文章不存在")
    finally:
        return json.dumps(ret)


@app.route('/article/<id>')
def article(id=id):
    return render_template("article.html", id=id)


@app.route('/login/')
def login():
    return render_template("login.html")


@app.route('/API/login/', methods=["POST"])
def APIlogin():
    result = json.loads(request.get_data())  # 验证用户名和密码
    Md5 = hashlib.md5()
    Md5.update(result[1])
    Md5hex = Md5.hexdigest()
    result[1] = Md5hex
    SQLresult = db.APIlogin(result)
    try:
        if (SQLresult[0][1] == result[1]):
            ret = {"status": "success", "site": "../manage/"}
            response = make_response(json.dumps(ret))
            response.set_cookie('token', genCookie(result[1]))
            print genCookie(result[1])
            return response
        else:
            ret = {"status": "fail", "site": "../login/"}
            return json.dumps(ret)
    except:
        ret = {"status": "fail", "site": "../login/"}
        return json.dumps(ret)


@app.route('/manage/')
def manage():
    if verifyToken(request.cookies.get("token"))[0]:
        print "HERE"
        return render_template("manage.html")
    return redirect("../login/")


@app.route('/API/addArticle/', methods=["POST"])
def addArticle():
    isUser, userId = verifyToken(request.cookies.get("token"))
    if isUser:
        data = json.loads(request.get_data())
        print data
        db.addArticle(data, userId)
        ret = {"status": "success"}
        return json.dumps(ret)
    ret = {"status": "fail"}
    return json.dumps(ret)


@app.route('/API/articleManage/')
def articleManage():
    result = db.articleManage()
    ret = []
    for i in result:
        ret.append({
            "id": i[0],
            "title": i[1],
            "link": "../article/" + str(i[0]),
            "status": i[2],
            "pubTime": i[3].strftime("%Y-%m-%d")
        })
    return json.dumps(ret)


@app.route('/API/change/', methods=["POST"])
def change():
    isUser, userId = verifyToken(request.cookies.get("token"))
    if isUser:
        ret = {"status": "success"}
        result = json.loads(request.get_data())
        print result
        db.change(result)
        return json.dumps(ret)
    ret = {"status": "fail"}
    return json.dumps(ret)


@app.route('/favicon.ico')
def favicon(id=id):
    return app.send_static_file("./static/favicon.ico")


def verifyToken(token):
    SQLresult = db.verifyToken()
    if token == None:
        return False, "null"
    for i in SQLresult:
        print i
        if token == genCookie(i[0]):
            return True, i[1]
    return False, "null"


def genCookie(passMd5):
    today = datetime.date.today()
    Md5 = hashlib.md5()
    Md5.update(passMd5 + today.strftime("%Y/%m/%d"))
    Md5hex = Md5.hexdigest()
    return Md5hex


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, port=80)
