import mysql.connector
import os
import math


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

        insert_stmt = "INSERT INTO PROPERTY_STG " \
                      "(MLS_ID, ZIPCODE, CITY, ADDR, BEDS, FULL_BATHS, PART_BATHS, STRUCT_SQFT, " \
                      "LOT_SIZE, LOT_SIZE_UNIT, YEAR_BUILT, LIST_PRICE, LIST_STATUS, URL) " \
                      "VALUES " \
                      "( %(mls_id)s, %(zipcode)s, %(city)s, %(addr)s, %(beds)s, %(full_baths)s, " \
                      "%(part_baths)s, %(struct_sqft)s, %(lot_size)s, %(lot_size_unit)s, %(year_built)s, " \
                      "%(list_price)s, %(list_status)s, %(url)s)"

        value = {'mls_id':  property.mls_id,
                 'zipcode': property.zipcode,
                 'city': property.city,
                 'addr': property.addr,
                 'beds': property.beds,
                 'full_baths': property.full_baths,
                 'part_baths': property.part_baths,
                 'struct_sqft': PropertyConnector.__handle_nan__(property.struct_sqft),
                 'lot_size': PropertyConnector.__handle_nan__(property.lot_size),
                 'lot_size_unit': property.lot_size_unit,
                 'year_built': property.year_built,
                 'list_price': PropertyConnector.__handle_nan__(property.list_price),
                 'list_status': property.list_status,
                 'url': property.url
                 }

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

    @staticmethod
    def __handle_nan__(num_float):
        if math.isnan(num_float):
            return None
        return num_float
