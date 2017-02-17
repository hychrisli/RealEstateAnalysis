import mysql.connector
import os


class GenericConnector(object):

    def __init__(self):
        db_user = os.environ['DB_USER']
        db_pass = os.environ['DB_PASS']
        db_host = os.environ['DB_HOST']
        database = os.environ['DATABASE']
        config = {
            'user': db_user,
            'password': db_pass,
            'host': db_host,
            'database': database,
            'autocommit': True
        }

        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def __clean_table__(self, table):
        delete_stmt = "DELETE FROM " + table
        reset_stmt = "ALTER TABLE " + table + " AUTO_INCREMENT = 1"
        self.cursor.execute(delete_stmt)
        self.cursor.execute(reset_stmt)

    def __single_upsert__(self, upsert_stmt, value):
        self.cursor.execute(upsert_stmt, value)
        return self.cursor.getlastrowid()

    def __select_all__(self, select_stmt):
        self.cursor.execute(select_stmt)
        return self.cursor.fetchall()
