from ..generic_connector import GenericConnector


class PropertyFactEtl(GenericConnector):

    def load_new_mls_ids(self):
        insert_stmt = "INSERT INTO property_fact ()"