import mysql.connector
import os


class MySqlConnector:

    def __init__(self):
        db_user = os.environ['DB_USER']
        db_pass = os.environ['DB_PASS']
        db_host = os.environ['DB_HOST']
        config = {
            'user': db_user,
            'password': db_pass,
            'host': db_host}

        self.cnx = mysql.connector.connect(**config)

    def close(self):
        self.cnx.close()



# Test
db_cnx = MySqlConnector()
db_cnx.close()