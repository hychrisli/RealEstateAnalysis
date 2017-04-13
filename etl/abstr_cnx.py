import mysql.connector
import os
import logging
from utility.constants import REA_ROOT_LOGGER


class GenericConnector(object):

    def __init__(self):
        self.logger = logging.getLogger(REA_ROOT_LOGGER + '.ETL')

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

    def _select_single_value_(self, select_stmt):
        return self._select_single_row_(select_stmt)[0]

    def _select_single_row_(self, select_stmt):
        self.cursor.execute(select_stmt)
        return self.cursor.fetchone()

    def _select_count_(self, table):
        select_stmt = "SELECT COUNT(*) FROM " + table
        cnt = self._select_single_value_(select_stmt)
        self.logger.info ("COUNT [" + table + "] : " + str(cnt))
