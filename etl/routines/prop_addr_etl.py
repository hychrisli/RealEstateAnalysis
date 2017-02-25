from ..abstr_cnx import GenericConnector


class PropAddrEtl(GenericConnector):

    def call_sp_prop_addr_fact_upsert(self):
        return self.cursor.execute('call sp_prop_addr_fact_upsert')
