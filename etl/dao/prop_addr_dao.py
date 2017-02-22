from ..abstr_cnx import GenericConnector
from ..routines.addr_verf_etl import AddrVerfEtl
from pyusps.address_information import OrderedDict
from utility.display import show_progress


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

        addrs = self.__select_all__(select_stmt)
        addr_num = len(addrs)
        req_num = addr_num / PropAddrDao.REQ_SIZE
        insert_values = []

        # Break down address list into chunks of REQ_SIZE
        for i in range(0, req_num):
            start = i * PropAddrDao.REQ_SIZE
            end = (i + 1) * PropAddrDao.REQ_SIZE

            if addr_num < end:
                end = addr_num
            show_progress(start, addr_num, PropAddrDao.DISP_INTVL, "processing No." + str(start))
            (id_lst, addr_dict_lst) = self.__build_addr_dict_lst__(addrs[start:end])
            res_lst = verf.verify(addr_dict_lst)
            insert_values.extend(self.__parse_res_lst__(id_lst, res_lst))

        return self.cursor.executemany(insert_stmt, insert_values)

    def get_addrs(self):
        select_stmt = self.__gen_select_prop_addr_stmt__()
        return self.__select_all__(select_stmt)

    def upd_urls(self, addr_lst):
        upd_values = []
        upd_stmt = self.__gen_upd_url_stmt__()
        for (mls_id, url) in addr_lst:
            upd_values.append(self.__gen_upd_url_vaue__(mls_id, url))
        return self.cursor.executemany(upd_stmt, upd_values)

    @staticmethod
    def __gen_insert_prop_addr_incr_stmt__():
        return "INSERT INTO " + PropAddrDao.PROP_ADDR_INCR_TAB + \
               " (MLS_ID, AREA_ID, USPS_ADDR)" \
               " VALUES (%(mls_id)s, %(area_id)s, %(addr)s)"

    @staticmethod
    def __gen_select_mls_addr_view_stmt__():
        return "SELECT MLS_ID, AREA_ID, ADDR, CITY, STATE FROM " \
               + PropAddrDao.MLS_ADDR_VIEW

    @staticmethod
    def __gen_select_prop_addr_stmt__():
        return "SELECT incr.MLS_ID, incr.USPS_ADDR, vmls.CITY, vmls.STATE FROM " \
               + PropAddrDao.MLS_ADDR_VIEW + " AS vmls JOIN " \
               + PropAddrDao.PROP_ADDR_INCR_TAB + " AS incr ON vmls.MLS_ID = incr.MLS_ID" \
                                                  " WHERE ISNULL(incr.REALTOR_URL)"

    @staticmethod
    def __gen_upd_url_stmt__():
        return "UPDATE " + PropAddrDao.PROP_ADDR_INCR_TAB \
               + " SET REALTOR_URL = %(url)s WHERE MLS_ID = %(mls_id)s"

    @staticmethod
    def __build_addr_dict_lst__(addrs):
        addr_dict_lst = []
        id_lst = []

        for (mls_id, area_id, addr, city, state) in addrs:
            addr_dict = dict([
                ('address', addr),
                ('city', city),
                ('state', state),
            ])
            addr_dict_lst.append(addr_dict)
            id_lst.append((mls_id, area_id))
        return id_lst, addr_dict_lst

    def __parse_res_lst__(self, id_lst, res_lst):
        values = []  # Only keep the correct addresses
        for i in range(0, PropAddrDao.REQ_SIZE):
            if isinstance(res_lst[i], OrderedDict):
                values.append(self.__gen_insert_value__(id_lst[i], res_lst[i]))
        return values

    @staticmethod
    def __gen_insert_value__(ids, res):
        value = {
            'mls_id': ids[0],
            'area_id': ids[1],
            'addr': res['address']
        }
        return value

    @staticmethod
    def __gen_upd_url_vaue__(mls_id, url):
        value = {
            'mls_id': mls_id,
            'url': url
        }
        return value
