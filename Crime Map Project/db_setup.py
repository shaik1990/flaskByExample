import pymysql
import dbconfig

connection = pymysql.connect(host='localhost',
                             user=dbconfig.db_user,
                             passwd=dbconfig.db_password)
cursor = ''

def db_connect():
    global cursor
    cursor = connection.cursor()


#
# try:
#     with connection.cursor() as cursor:
#         global cursor
#         # sql = "CREATE DATABASE IF NOT EXISTS crimemap"
#         # cursor.execute(sql)
