import mysql.connector
import os


class MySqlConnector:

    def __init__(self):
        db_user = os.environ['DB_USER']
        db_pass = os.environ['DB_PASS']
        db_host = os.environ['DB_HOST']
        database = os.environ['DATABASE']
        config = {
            'user': db_user,
            'password': db_pass,
            'host': db_host,
            'database': database
        }

        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()

    def add_county(self, county):

        insert_stmt = "INSERT INTO COUNTY (NAME) VALUES ( %(county)s )"
        value = {'county': "\'" + county + "\'"}
        self.cursor.execute(insert_stmt, value)
        self.cnx.commit()
        print(self.cursor.lastrowid)

    def close(self):
        self.cursor.close()
        self.cnx.close()



# Test
db_cnx = MySqlConnector()
db_cnx.close()