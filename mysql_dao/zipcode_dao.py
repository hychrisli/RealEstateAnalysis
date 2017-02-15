import mysql.connector
import os


class ZipcodeConnector:

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

    def init_cleanup(self):
        self.__clean_table__("ZIPCODE")
        self.__clean_table__("CITY")
        self.__clean_table__("COUNTY")

    def __clean_table__(self, table):
        delete_stmt = "DELETE FROM " + table
        reset_stmt = "ALTER TABLE " + table + " AUTO_INCREMENT = 1"
        self.cursor.execute(delete_stmt)
        self.cursor.execute(reset_stmt)

    def add_county(self, county):

        insert_stmt = "INSERT INTO COUNTY (NAME) VALUES ( %(county)s )"
        value = {'county':  str(county)}
        return self.__exec_insert__(insert_stmt, value)

    def add_city(self, county_id, city):
        insert_stmt = ("INSERT INTO CITY (NAME, COUNTY_ID) "
                       "VALUES ( %(city)s, %(county_id)s )")
        value = {'city': str(city),
                 'county_id': county_id}
        return self.__exec_insert__(insert_stmt, value)

    def add_zipcode(self, city_id, zipcode):
        insert_stmt = ("INSERT INTO ZIPCODE (ZIPCODE, CITY_ID) "
                       "VALUES ( %(zipcode)s, %(city_id)s )")
        value = {'zipcode': str(zipcode),
                 'city_id': city_id}
        return self.__exec_insert__(insert_stmt, value)

    def find_county_id(self, county):
        select_stmt = "SELECT COUNTY_ID FROM COUNTY WHERE LOWER(NAME) = %(county)s"
        value = {'county': str(county).lower()}
        return self.__exec_single_select__(select_stmt, value)

    def find_city_id(self, city):
        select_stmt = "SELECT CITY_ID FROM CITY WHERE LOWER(NAME) = %(city)s"
        value = {'city': str(city).lower()}
        return self.__exec_single_select__(select_stmt, value)

    def get_zipcode_lst(self):
        select_stmt = "SELECT DISTINCT ZIPCODE FROM ZIPCODE"
        self.cursor.execute(select_stmt)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def __exec_insert__(self, insert_stmt, value):
        self.cursor.execute(insert_stmt, value)
        return self.cursor.getlastrowid()

    def __exec_single_select__(self, select_stmt, value):
        self.cursor.execute(select_stmt, value)
        return self.cursor.fetchone()[0]
