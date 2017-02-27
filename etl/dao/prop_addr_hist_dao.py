from ..abstr_cnx import GenericConnector
from utility.display import show_progress


class PropAddrHistDao(GenericConnector):

    HIST_STG_TABLE = 'prop_addr_hist_stg'

    def init_cleanup(self):
        self.__clean_table__(PropAddrHistDao.HIST_STG_TABLE)

    def add_prop_addr_hist(self, hist):
        insert_stmt = self.__gen_insert_stmt__()
        insert_value = self.__gen_insert_value__(hist)

        return self.cursor.execute(insert_stmt, insert_value)

    @staticmethod
    def __gen_insert_stmt__():
        return "INSERT INTO " + PropAddrHistDao.HIST_STG_TABLE + \
               " (PROP_ADDR_ID, EVENT_DATE, EVENT, PRICE, PRICE_SQFT)" \
               " VALUES (%(prop_addr_id)s, %(event_date)s," \
               " %(event)s, %(price)s, %(price_sqft)s)"

    @staticmethod
    def __gen_insert_value__(hist):
        value = {
            'prop_addr_id': str(hist.prop_addr_id),
            'event_date': hist.event_date,
            'event': str(hist.event),
            'price': hist.price,
            'price_sqft': hist.price_sqft
        }
        return value
