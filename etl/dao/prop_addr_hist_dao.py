from ..abstr_cnx import GenericConnector
from random import randint

import mysql.connector
import os


class PropAddrHistDao(GenericConnector):
    HIST_STG_TABLE = 'prop_addr_hist_stg'
    PROP_ADDR_FACT_TABLE = 'prop_addr_fact'
    PROP_ADDR_HIST_TABLE = 'prop_addr_hist'

    def __init__(self):
        super(PropAddrHistDao, self).__init__()
        file_prefix = 'prop_addr_hist_rej_'
        # file_number = str(datetime.now().strftime('%Y%m%d%H%M%S'))
        file_number = '20170301'
        file_suffix = '.dat'
        file_dir = os.environ['REA_DATA']
        file_name = file_prefix + file_number + file_suffix
        self.rej_rec_file = open(file_dir + '/' + file_name, 'a')
        # print ("Rejected Record File: " + self.rej_rec_file.name)

    def init_cleanup(self):
        self.__clean_table__(PropAddrHistDao.HIST_STG_TABLE)

    def select_url_batch(self, batch_size):
        select_stmt = self.__gen_select_url_batch_stmt__(batch_size)
        return self.__select_all__(select_stmt)

    def get_total_num(self):
        select_stmt = self.__gen_select_cnt_stmt__()
        return self._select_single_value_(select_stmt)

    def get_latest_date(self, prop_addr_id):
        select_stmt = self.__gen_select_latest_date_stmt__(prop_addr_id)
        return self._select_single_value_(select_stmt)

    def add_prop_addr_hist_event(self, hist_event):

        # Insert into HIST_STG_TABLE
        insert_stmt = self.__gen_insert_stmt__()
        insert_value = self.__gen_insert_value__(hist_event)

        try:
            self.cursor.execute(insert_stmt, insert_value)
        except mysql.connector.Error:
            rej_rec = hist_event.to_string()
            print ('Rejected Record: ' + rej_rec)
            self.rej_rec_file.write(rej_rec + '\n')

    def mark_is_updated(self, prop_addr_id):
        # update PROP_ADDR_FACT_TABLE
        upd_stmt = self.__gen_upd_stmt__()
        upd_value = self.__gen_upd_value__(prop_addr_id)

        self.cursor.execute(upd_stmt, upd_value)
        self.rej_rec_file.flush()

    def close(self):
        self.rej_rec_file.close()
        self.cursor.close()
        self.cnx.close()

    @staticmethod
    def __gen_select_url_batch_stmt__(batch_size):
        return "SELECT PROP_ADDR_ID, REALTOR_URL FROM " + \
               PropAddrHistDao.PROP_ADDR_FACT_TABLE + " WHERE IS_UPDATED = 0 LIMIT " + str(batch_size)

    @staticmethod
    def __gen_select_cnt_stmt__():
        return "SELECT COUNT(*) FROM " + \
               PropAddrHistDao.PROP_ADDR_FACT_TABLE + " WHERE IS_UPDATED = 0"

    @staticmethod
    def __gen_select_latest_date_stmt__(prop_addr_id):
        return "SELECT MAX(EVENT_DATE) FROM " + \
               PropAddrHistDao.PROP_ADDR_HIST_TABLE + " WHERE PROP_ADDR_ID = " + str(prop_addr_id)

    @staticmethod
    def __gen_insert_stmt__():
        return "INSERT INTO " + PropAddrHistDao.HIST_STG_TABLE + \
               " (PROP_ADDR_ID, EVENT_DATE, EVENT, PRICE, PRICE_SQFT)" \
               " VALUES (%(prop_addr_id)s, %(event_date)s," \
               " %(event)s, %(price)s, %(price_sqft)s)"

    @staticmethod
    def __gen_insert_value__(hist):
        value = {
            'prop_addr_id': hist.prop_addr_id,
            'event_date': hist.event_date,
            'event': str(hist.event),
            'price': hist.price,
            'price_sqft': hist.price_sqft
        }
        return value

    @staticmethod
    def __gen_upd_stmt__():
        return "UPDATE " + PropAddrHistDao.PROP_ADDR_FACT_TABLE + \
               " SET IS_UPDATED = 1 WHERE PROP_ADDR_ID = %(prop_addr_id)s"

    @staticmethod
    def __gen_upd_value__(prop_addr_id):
        return {'prop_addr_id': prop_addr_id}
