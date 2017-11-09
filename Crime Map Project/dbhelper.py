import pymysql
import dbconfig

class DBHelper:
    def connect(self, database="crimemap"):
        return pymysql.connect(host='localhost',
                               user=dbconfig.db_user,
                               passwd=dbconfig.db_password,
                               db=database)
    def get_all_inputs(self):
        connection = self.connect()
        try:
            query = "SELECT description from crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            connection.close()

    def add_input(self,data):
        connection = self.connect()
        try:
            query = "insert into crimes (description) " \
                    "values (%s);"  # str.format() is not used

            with connection.cursor() as cursor:
                cursor.execute(query, data) #cursor.execute will automatically escape special characters to mitigate SQL injection
                connection.commit()
        finally:
            connection.close()
    def clear_all(self):
        connection = self.connect()
        try:
            query = "delete from crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()

    def add_crime(self, category, date, latitude, longitude, description):
        connection = self.connect()
        try:
            query = "INSERT INTO crimes(category _in, date_in, latitude, longitude, description)" \
                    "VALUES (%s,%s,%s,%s,%s)"
            with connection.cursor() as cursor:
                cursor.execute(query,(category, date, latitude, longitude, description))
                connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()
    def get_all_crimes(self):
        return [{ 'latitude': 38.9586310,
                  'longitude': -77.3570030,
                  'date': "2017-11-04",
                  'category': "Break-in",
                  'description': "Test Description"
                }]

