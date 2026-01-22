# @Auther   :Mateo
from fastapi import FastAPI
import pymysql

app = FastAPI()


class student:
    def __init__(self, username, password, register_code):
        self.username = username
        self.password = password
        self.register_code = register_code

    #
    # def getUserName(self):
    #     return self.username
    #
    # def getPassword(self):
    #     return self.password


def add_stu(username, password, register_code):
    db = pymysql.connect(host='localhost', user='root', database='db01', password='hsp')
    cursor = db.cursor()
    data = (username, password, register_code)
    sql = "insert into stu (username, password, register_code) values (%s,%s,%s)"
    cursor.execute(sql, data)
    db.commit()
    cursor.close()
    db.close()


# def change(username, new_password):
#     db2 = pymysql.connect(host='localhost', user='root', database='db01', password='hsp')
#     cursor2 = db2.cursor()
#     data = (new_password, username)
#     sql = "update stu set password=%s where username = %s"
#     cursor2.execute(sql, data)
#     return "密码修改成功"
#     db2.commit()
#     cursor2.close()
#     db2.close()


# def login(a):
#     print(a)
#     db = pymysql.connect(host='localhost', user='root', database='db01', password='hsp')
#     cursor = db.cursor()
#     sql = "select username, password from stu"
#     cursor.execute(sql)
#     result1 = cursor.fetchall()
#     print(result1)
#     if a in result1:
#         return "登陆成功"
#     else:
#         return "账号或密码错误"
#     db.commit()
#     cursor.close()
#     db.close()


# @app.get("/")
# async def root1():
#     yyw = student(1, "666", "123456")
#     # return {"message": "Hello FastAPI!"}
#     return yyw


# @app.get("/login/{username}/{password}")
# async def root2(username: str, password: str):
#     # return {"message": "Hello FastAPI!"}
#     return None


new_student = []


#  注册账号，并将账号密码保存至数据库
@app.get("/register")
async def root4(username: str = "", password: str = "", register_code: str = ""):
    if username and password and register_code:
        add_stu(username, password, register_code)
        # new = student(username, password, register_code)
        # new_student.append(new)
        # # return "注册成功"
        # return new_student
        return "注册成功"


#  登录账号，判断输入的账号密码与数据库中的账号密码是否相同
@app.get("/login2")
async def root4(username: str = "", password: str = ""):
    if username and password:
        a = (username, password)
        # print(a)
        # login(a)
        db = pymysql.connect(host='localhost', user='root', database='db01', password='hsp')
        cursor = db.cursor()
        sql = "select username, password from stu"
        cursor.execute(sql)
        result1 = cursor.fetchall()
        print(result1)
        if a in result1:
            return "登陆成功"
        else:
            return "账号或密码错误"
        db.commit()
        cursor.close()
        db.close()
    # yyw = student(1, "yeyuwei", "123456")
    # for i in new_student:
    #     print(i)
    #     if getattr(i, "username") == username and getattr(i, "password") == password:
    #         return i

    # else:
    # return "账号或密码错误"

# 这里只是单纯的修改密码
# @app.get("/change")
# async def root4(username: str = "", password: str = "", new_password: str = ""):
#     if username and password and new_password:
#         db = pymysql.connect(host='localhost', user='root', database='db01', password='hsp')
#         cursor = db.cursor()
#         data = (new_password, username)
#         sql = "update stu set password=%s where username = %s"
#         cursor.execute(sql, data)
#
#         db.commit()
#         cursor.close()
#         db.close()
#         return "密码修改成功"


# 这里需要先判断用户名和密码是否正确，正确的话再修改密码
@app.get("/change1")
async def root4(username: str = "", password: str = "", new_password: str = ""):
    if username and password and new_password:
        a = (username, password)
        # print(a)
        # login(a)
        db1 = pymysql.connect(host='localhost', user='root', database='db01', password='hsp')
        cursor1 = db1.cursor()
        sql1 = "select username, password from stu"
        cursor1.execute(sql1)
        result1 = cursor1.fetchall()
        if a in result1:
            db2 = pymysql.connect(host='localhost', user='root', database='db01', password='hsp')
            cursor2 = db2.cursor()
            data = (new_password, username)
            sql2 = "update stu set password=%s where username = %s"
            cursor2.execute(sql2, data)
        else:
            return "账号或密码错误"
        db1.commit()
        cursor1.close()
        db1.close()
        db2.commit()
        cursor2.close()
        db2.close()
        return "密码修改成功"


# 启动命令：uvicorn main:app --reload
