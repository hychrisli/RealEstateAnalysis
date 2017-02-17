from ..generic_connector import GenericConnector


class PropertyEtl(GenericConnector):

    def call_sp_property_incr_insert(self):
        return self.cursor.execute("CALL sp_property_incr_insert")

    def call_sp_prop_del_mls_excld(self):
        return self.cursor.execute("CALL sp_prop_del_mls_excld")

    def call_sp_property_fact_insert(self):
        return self.cursor.execute("CALL sp_property_fact_insert")

    def call_sp_property_dim_upd(self):
        return self.cursor.execute("CALL sp_property_dim_upd")