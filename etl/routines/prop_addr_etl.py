from ..abstr_cnx import GenericConnector


class PropAddrEtl(GenericConnector):

    def call_sp_prop_addr_fact_upsert(self):
        return self.cursor.execute('call sp_prop_addr_fact_upsert')

    def call_sp_prop_addr_hist_incr(self):
        return self.cursor.execute('call sp_prop_addr_hist_incr')

    def call_sp_prop_addr_hist(self):
        return self.cursor.execute('call sp_prop_addr_hist')