from ..generic_connector import GenericConnector


class MlsTypeDao(GenericConnector):
    INCR_TAB= 'property_incr'
    TYPE_TAB = 'prop_type_lkp'
    COMMERCIAL_KEY_WORDS = ['109', 'commercial', 'comm.', 'agriculture',
                            'business', 'farm', 'retail']
    MULTI_UNIT_KEY_WORDS = ['unit', 'fourplex', 'triplex', 'duplex']

    def __init__(self):
        super(MlsTypeDao, self).__init__()
        self.type_lst = self.get_prop_types()
        self.type_dict = self.__create_type_dict__()

    def get_mls_url_incr(self):
        select_stmt = "SELECT URL FROM " + MlsTypeDao.INCR_TAB
        return self.__select_all__(select_stmt)

    def update_prop_incr_with_type(self, mls_id, prop_type):

        type_id = self.__map_prop_type__(prop_type)
        # print ( str(type_id) + " : " + str(prop_type) )
        upd_stmt = ("UPDATE " + MlsTypeDao.INCR_TAB +
                    " SET PROP_TYPE_ID = %(type_id)s "
                    " WHERE MLS_ID = %(mls_id)s")
        value = {'mls_id': str(mls_id),
                 'type_id': type_id}
        return self.__single_upsert__(upd_stmt, value)

    def get_prop_types(self):
        select_stmt = "SELECT TYPE_ID, TYPE FROM " + MlsTypeDao.TYPE_TAB
        return self.__select_all__(select_stmt)

    def __create_type_dict__(self):
        type_dict = {}
        for (type_id, prop_type) in self.type_lst:
            type_dict[prop_type] = int(type_id)
        return type_dict

    def __map_prop_type__(self, prop_type):

        if not prop_type:
            return None

        type_name = prop_type.lower()

        if 'none' in type_name:
            return None
        elif any(word in type_name for word in MlsTypeDao.COMMERCIAL_KEY_WORDS):
            return self.type_dict['Commercial']
        elif ' rent' in type_name:
            return self.type_dict['Rent']
        elif ' land' in type_name or ' lot' in type_name:
            return self.type_dict['Land / Lot']
        elif 'mobile' in type_name or 'modular' in type_name:
            return self.type_dict['Mobile']
        elif any(word in type_name for word in MlsTypeDao.MULTI_UNIT_KEY_WORDS):
            return self.type_dict['Multi-Unit']
        elif 'condominium' in type_name:
            return self.type_dict['Condo']
        elif 'townhouse' in type_name:
            return self.type_dict['Townhouse']
        elif 'family' in type_name:
            return self.type_dict['Single Family']
        else:
            print (" Special Type: " + prop_type)
            return None
