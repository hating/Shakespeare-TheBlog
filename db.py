# encoding:utf-8 -*-
import hashlib
import MySQLdb
import sys
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")


host = "127.0.0.1"
user = "root"
password = "root"
database = "Blog"
charset = "utf8"


def open():
    conn = MySQLdb.connect(host, user, password, database, charset=charset)
    cursor = conn.cursor()
    return conn, cursor


def close(conn, cursor):
    conn.close()
    cursor.close()


def allArticle():
    conn, cursor = open()
    cursor.execute("SELECT content,id from craft where type = '1' order by id DESC ;")
    result = cursor.fetchall()
    close(conn, cursor)
    return result


def getArticle(id):
    conn, cursor = open()
    cursor.execute("SELECT content,pubTime,type,name from craft,user where craft.id = %s and userid = user.id;" % id)
    result = cursor.fetchall()
    close(conn, cursor)
    return result


def APIlogin(result):
    conn, cursor = open()
    result[0] = MySQLdb.escape_string(result[0])
    result[1] = MySQLdb.escape_string(result[1])
    cursor.execute("select name,password from user where name = '%s'" % result[0])
    result = cursor.fetchall()
    close(conn, cursor)
    return result


def addArticle(data, userId):
    conn, cursor = open()
    data["title"] = MySQLdb.escape_string(data["title"].decode("utf-8"))
    data["content"] = MySQLdb.escape_string(data["content"].decode("utf-8"))
    cursor = conn.cursor()
    today = datetime.date.today()
    cursor.execute(
        "insert into craft(userid,title,content,pubTime,type) values ('%s','%s','%s','%s','%s')" % (
            userId, data["title"], data["content"], today.strftime("%Y-%m-%d"), "0"))
    conn.commit()
    close(conn, cursor)
    return


def articleManage():
    conn, cursor = open()
    cursor.execute("SELECT id,title,type,pubTime from craft where type != '4' ORDER BY pubTime desc;")
    result = cursor.fetchall()
    close(conn, cursor)
    return result


def change(result):
    conn, cursor = open()
    result[0] = MySQLdb.escape_string(str(result[0]))
    result[1] = MySQLdb.escape_string(result[1])
    cursor = conn.cursor()
    cursor.execute("UPDATE craft set type = '%s' where id = '%s';" % (result[1], result[0]))
    conn.commit()
    close(conn, cursor)
    return


def verifyToken():
    conn, cursor = open()
    cursor.execute("select password,id from user ;")
    result = cursor.fetchall()
    close(conn, cursor)
    return result


def createUser():
    conn, cursor = open()
    cursor.execute("DROP table if EXISTS user")
    cursor.execute('''create table user (
id INT(11) primary key not null unique auto_increment,
name VARCHAR(45),
isAdmin VARCHAR(45),
regTime DATE,
password VARCHAR(45)
)''')
    close(conn, cursor)
    return


def createCraft():
    conn, cursor = open()
    cursor.execute("DROP table if EXISTS craft")
    cursor.execute('''create table craft (
id INT(11) primary key not null unique auto_increment,
userid INT(11),
title LONGTEXT,
content LONGTEXT,
pubTime date,
type INT(11)
)
''')
    close(conn, cursor)
    return


def insertUser(username, password):
    conn, cursor = open()
    today = datetime.date.today()
    Md5 = hashlib.md5()
    Md5.update(password)
    Md5hex = Md5.hexdigest()
    Md52 = hashlib.md5()
    Md52.update(Md5hex)
    password_twice = Md52.hexdigest()
    cursor.execute("insert into user values('1','%s','1','%s','%s')" % (
        username, today.strftime("%Y-%m-%d"), password_twice))
    conn.commit()
    close(conn, cursor)
    return


def insertCraft():
    conn, cursor = open()
    today = datetime.date.today()
    cursor.execute(
        "insert into craft values('1','1','你好世界！','# 你好世界！\n\n* Shakespeare是一个轻量型的，基于ES6编写的个人博客； \n* 这是博客的第一篇文章；\n* 赶紧进入后台发表文章吧！','%s','1');" % (
            today.strftime(
                "%Y-%m-%d")))
    conn.commit()
    close(conn, cursor)
    return
