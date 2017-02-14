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
            'database': database,
            'autocommit': True
        }

        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()
        self.__clean_tables__()

    def __clean_tables__(self):
        stmt_delete_city = "DELETE FROM CITY"
        stmt_delete_county = "DELETE FROM COUNTY"
        stmt_reset_city_rowid = "ALTER TABLE CITY AUTO_INCREMENT = 1"
        stmt_reset_county_rowid = "ALTER TABLE COUNTY AUTO_INCREMENT = 1"

        self.cursor.execute(stmt_delete_city)
        self.cursor.execute(stmt_delete_county)
        self.cursor.execute(stmt_reset_city_rowid)
        self.cursor.execute(stmt_reset_county_rowid)

    def add_county(self, county):

        insert_stmt = "INSERT INTO COUNTY (NAME) VALUES ( %(county)s )"
        value = {'county':  str(county)}
        return self.__exec_insert__(insert_stmt, value)

    def add_city(self, county_id, city):
        insert_stmt = ("INSERT INTO CITY (NAME, COUNTY_ID) "
                       "VALUES ( %(city)s, %(county_id)s)")
        value = {'city': str(city),
                 'county_id': county_id}
        return self.__exec_insert__(insert_stmt, value)

    def find_county_id(self, county):
        select_stmt = "SELECT COUNTY_ID FROM COUNTY WHERE LOWER(NAME) = %(county)s"
        value = {'county': str(county).lower()}
        self.cursor.execute(select_stmt, value)
        return self.cursor.fetchone()[0]

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def __exec_insert__(self, insert_stmt, value):
        self.cursor.execute(insert_stmt, value)
        return self.cursor.getlastrowid()


# Test
db_cnx = MySqlConnector()
db_cnx.close()