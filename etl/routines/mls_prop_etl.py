from ..abstr_cnx import GenericConnector


class MlsPropEtl(GenericConnector):

    def call_sp_mls_prop_incr_insert(self):
        return self.cursor.execute("CALL sp_mls_prop_incr_insert")

    def call_sp_prop_del_mls_excld(self):
        return self.cursor.execute("CALL sp_prop_del_mls_excld")

    def call_sp_mls_prop_fact_insert(self):
        return self.cursor.execute("CALL sp_mls_prop_fact_insert")

    def call_sp_mls_prop_dim_upd(self):
        return self.cursor.execute("CALL sp_mls_prop_dim_upd")

    def call_sp_mls_status_hist_upd(self):
        return self.cursor.execute("CALL sp_mls_status_hist_upd")
