import mysql.connector
from DBUtils.PooledDB import PooledDB
pool = PooledDB(mysql.connector,5,host='localhost',user='root',passwd='123456',db='test',port=3306)
def createConnect():
    # mydb = mysql.connector.connect(
    #     host="localhost",       # 数据库主机地址
    #     user="root",    # 数据库用户名
    #     passwd="123456",   # 数据库密码
    #     database="test"
    # )
    mydb=pool.connection()
    return mydb

def insert(sql,data):
    try:
        mydb=createConnect()
        mycursor = mydb.cursor()
        mycursor.execute(sql,data)
        mydb.commit()
        print(mycursor.rowcount, "记录插入成功。")
    finally:
        mycursor.close()
        mydb.close()


def selectOne(sql,data):
    try:
        mydb=createConnect()
        mycursor = mydb.cursor()
        mycursor.execute(sql,data)
        myresult = mycursor.fetchone()
        return myresult
    finally:
        mydb.close()

def selectAll(sql,data):
    try:
        mydb=createConnect()
        mycursor = mydb.cursor()
        mycursor.execute(sql,data)
        myresult = mycursor.fetchall()
        return myresult
    finally:
        mycursor.close()
        mydb.close()

def delete(sql,data):
    try:
        mydb=createConnect()
        mycursor = mydb.cursor()
        mycursor.execute(sql,data)
        mydb.commit()
        print(mycursor.rowcount, "删除成功。")
    finally:
        mycursor.close()
        mydb.close()
