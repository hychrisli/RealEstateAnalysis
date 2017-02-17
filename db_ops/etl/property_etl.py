from ..generic_connector import GenericConnector


class PropertyEtl(GenericConnector):

    def call_sp_property_incr_insert(self):
        sp_stmt = "CALL sp_property_incr_insert"
        self.cursor.execute(sp_stmt)

    def call_sp_prop_del_mls_excld(self):
        sp_stmt = "CALL sp_prop_del_mls_excld"
        self.cursor.execute(sp_stmt)
