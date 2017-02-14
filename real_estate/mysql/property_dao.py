import mysql.connector
import os


class PropertyConnector:

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
        self.__init_cleanup__()

    def __init_cleanup__(self):
        self.__clean_table__("PROPERTY_STG")

    def __clean_table__(self, table):
        delete_stmt = "DELETE FROM " + table
        reset_stmt = "ALTER TABLE " + table + " AUTO_INCREMENT = 1"
        self.cursor.execute(delete_stmt)
        self.cursor.execute(reset_stmt)

    def add_property(self, property):

        insert_stmt = "INSERT INTO COUNTY (NAME) VALUES ( %(county)s )"
        value = {'county':  str(county)}
        return self.__exec_insert__(insert_stmt, value)

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def __exec_insert__(self, insert_stmt, value):
        self.cursor.execute(insert_stmt, value)
        return self.cursor.getlastrowid()

    def __exec_single_select__(self, select_stmt, value):
        self.cursor.execute(select_stmt, value)
        return self.cursor.fetchone()[0]
