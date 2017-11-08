import pymysql
import dbconfig

connection = pymysql.connect(host='localhost',
                             user=dbconfig.db_user,
                             passwd=dbconfig.db_password)
cursor = ''

def db_connect():
    global cursor
    cursor = connection.cursor()