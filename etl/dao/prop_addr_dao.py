from ..abstr_cnx import GenericConnector
from ..routines.addr_verf_etl import AddrVerfEtl
from ..entities.prop_addr_incr_lst import PropAddrIncrLst
from utility.actions import show_progress


class PropAddrDao(GenericConnector):
    MLS_ADDR_VIEW = 'v_mls_addr'
    PROP_ADDR_INCR_TAB = 'prop_addr_incr'
    REQ_SIZE = 5
    DISP_INTVL = 20

    def init_cleanup(self):
        self.__clean_table__(PropAddrDao.PROP_ADDR_INCR_TAB)

    def add_addrs(self):

        verf = AddrVerfEtl()
        insert_stmt = self.__gen_insert_prop_addr_incr_stmt__()
        select_stmt = self.__gen_select_mls_addr_view_stmt__()

        sel_rows = self.__select_all__(select_stmt)
        row_num = len(sel_rows)
        req_num = row_num / PropAddrDao.REQ_SIZE
        insert_values = []

        # Break down address list into chunks of REQ_SIZE
        for i in range(0, req_num):
            prop_addr_incr_lst = PropAddrIncrLst()
            start = i * PropAddrDao.REQ_SIZE
            end = (i + 1) * PropAddrDao.REQ_SIZE

            if row_num < end:
                end = row_num
            show_progress(start, row_num, PropAddrDao.DISP_INTVL, "processing No." + str(start))
            prop_addr_incr_lst.parse(sel_rows[start:end])
            insert_values.extend(prop_addr_incr_lst.get_incr_inserts())

        return self.cursor.executemany(insert_stmt, insert_values)

    @staticmethod
    def __gen_insert_prop_addr_incr_stmt__():
        return "INSERT INTO " + PropAddrDao.PROP_ADDR_INCR_TAB + \
               " (MLS_ID, AREA_ID, USPS_ADDR, REALTOR_URL)" \
               " VALUES (%(mls_id)s, %(area_id)s, %(addr)s, %(url)s)"

    @staticmethod
    def __gen_select_mls_addr_view_stmt__():
        return "SELECT MLS_ID, AREA_ID, ADDR, CITY, STATE, URL FROM " \
               + PropAddrDao.MLS_ADDR_VIEW
