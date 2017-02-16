from ..generic_connector import GenericConnector


class MlsStgDao(GenericConnector):

    def init_cleanup(self):
        self.__clean_table__("TYPE_STG")

    def get_mls_url_incr(self):
        select_stmt = "SELECT URL FROM v_mls_url_incr"
        self.cursor.execute(select_stmt)
        return self.cursor.fetchall()

    def add_prop_type(self, mls_id, prop_type):
        insert_stmt = ("INSERT INTO TYPE_STG (MLS_ID, TYPE) "
                       "VALUES ( %(mls_id)s, %(type)s )")
        value = {'mls_id': str(mls_id),
                 'type': str(prop_type)}
        return self.__exec_single_insert__(insert_stmt, value)