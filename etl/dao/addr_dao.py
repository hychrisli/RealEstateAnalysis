from ..abstr_cnx import GenericConnector
from ..routines.addr_verf_etl import AddrVerfEtl
from pyusps.address_information import OrderedDict


class AddrDao(GenericConnector):
    MLS_ADDR_VIEW = 'v_mls_addr'
    ADDR_PROP_TAB = 'prop_addr_fact'
    REQ_SIZE = 5

    def init_cleanup(self):
        self.__clean_table__(AddrDao.ADDR_PROP_TAB)

    def add_addrs(self):

        verf = AddrVerfEtl()
        insert_stmt = "INSERT INTO " + AddrDao.ADDR_PROP_TAB + \
                      " (MLS_ID, AREA_ID, USPS_ADDR) VALUES (%(mls_id)s, %(area_id)s, %(addr)s)"
        select_stmt = "SELECT MLS_ID, AREA_ID, ADDR, CITY, STATE FROM " + AddrDao.MLS_ADDR_VIEW

        addrs = self.__select_all__(select_stmt)
        addr_num = len(addrs)
        req_num = addr_num / AddrDao.REQ_SIZE
        insert_values = []

        for i in range(0, req_num):
            start = i * AddrDao.REQ_SIZE
            end = (i + 1) * AddrDao.REQ_SIZE

            if addr_num < end:
                end = addr_num

            print (start)
            (id_lst, addr_dict_lst) = self.__build_addr_dict_lst__(addrs[start:end])
            res_lst = verf.verify(addr_dict_lst)
            insert_values.extend(self.__parse_res_lst__(id_lst, res_lst))

        return self.cursor.executemany(insert_stmt, insert_values)

    def __build_addr_dict_lst__(self, addrs):
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
        values = []
        for i in range(0, AddrDao.REQ_SIZE):
            if isinstance(res_lst[i], OrderedDict):
                values.append(self.__gen_insert_value_(id_lst[i], res_lst[i]))
        return values


    def __gen_insert_value_(self, ids, res):
        value = {
            'mls_id': ids[0],
            'area_id': ids[1],
            'addr': res['address']
        }
        return value
