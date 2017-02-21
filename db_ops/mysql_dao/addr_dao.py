from ..generic_connector import GenericConnector
from ..etl.addr_verf_etl import AddrVerfEtl
from pyusps.address_information import OrderedDict

class AddrDao(GenericConnector):
    MLS_ADDR_VIEW = 'v_mls_addr'
    ADDR_PROP_TAB = 'addr_prop_fact'
    REQ_SIZE = 5

    def init_cleanup(self):
        self.__clean_table__(AddrDao.ADDR_PROP_TAB)

    def add_addrs(self):

        verf = AddrVerfEtl()

        select_stmt = "SELECT MLS_ID, AREA_ID, ADDR, CITY, STATE FROM " + AddrDao.MLS_ADDR_VIEW
        addrs = self.__select_all__(select_stmt)
        (id_lst, addr_dict_lst) = self.__build_addr_dict_lst__(addrs)
        res_lst = verf.verify(addr_dict_lst)
        self.__parse_res_lst__(id_lst, res_lst)

    def __build_addr_dict_lst__(self, addrs):
        addr_dict_lst = []
        id_lst = []

        for (mls_id, area_id, addr, city, state) in addrs[0:AddrDao.REQ_SIZE]:
            addr_dict = dict([
                ('address', addr),
                ('city', city),
                ('state', state),
            ])
            addr_dict_lst.append(addr_dict)
            id_lst.append((mls_id, area_id))
        return id_lst, addr_dict_lst

    def __parse_res_lst__(self, id_lst, res_lst):

        for i in range(0, AddrDao.REQ_SIZE):
            if isinstance(res_lst[i], ValueError):
                print (res_lst[i])
            elif isinstance(res_lst[i], OrderedDict):
                print (res_lst[i])
                value = self.__gen_insert_value_(id_lst[i], res_lst[i])
                print (value)

    def __gen_insert_value_(self, ids, res):
        value = {
            'mls_id': ids[0],
            'area_id': ids[1],
            'addr': res['address']
        }
        return value
