import math
from ..generic_connector import GenericConnector


class PropertyConnector(GenericConnector):

    def init_cleanup(self):
        self.__clean_table__("PROPERTY_STG")

    def __clean_table__(self, table):
        delete_stmt = "DELETE FROM " + table
        reset_stmt = "ALTER TABLE " + table + " AUTO_INCREMENT = 1"
        self.cursor.execute(delete_stmt)
        self.cursor.execute(reset_stmt)

    def add_properties(self, property_lst):
        insert_stmt = "INSERT INTO PROPERTY_STG " \
                      "(MLS_ID, ZIPCODE, CITY, ADDR, BEDS, FULL_BATHS, PART_BATHS, STRUCT_SQFT, " \
                      "LOT_SIZE, LOT_SIZE_UNIT, YEAR_BUILT, LIST_PRICE, LIST_STATUS, URL) " \
                      "VALUES " \
                      "( %(mls_id)s, %(zipcode)s, %(city)s, %(addr)s, %(beds)s, %(full_baths)s, " \
                      "%(part_baths)s, %(struct_sqft)s, %(lot_size)s, %(lot_size_unit)s, %(year_built)s, " \
                      "%(list_price)s, %(list_status)s, %(url)s)"
        values = []
        for prop in property_lst:
            # try:
            #     self.cursor.execute(insert_stmt, PropertyConnector.__gen_insert_value__(prop))
            # except Exception as e:
            #     prop.print_details()
            #     print (e)
            values.append(PropertyConnector.__gen_insert_value__(prop))

        self.cursor.executemany(insert_stmt, values)

    @staticmethod
    def __gen_insert_value__(prop):
        value = {'mls_id': prop.mls_id,
                 'zipcode': prop.zipcode,
                 'city': prop.city,
                 'addr': prop.addr,
                 'beds': prop.beds,
                 'full_baths': prop.full_baths,
                 'part_baths': prop.part_baths,
                 'struct_sqft': PropertyConnector.__handle_nan__(prop.struct_sqft),
                 'lot_size': PropertyConnector.__handle_nan__(prop.lot_size),
                 'lot_size_unit': prop.lot_size_unit,
                 'year_built': prop.year_built,
                 'list_price': PropertyConnector.__handle_nan__(prop.list_price),
                 'list_status': prop.list_status,
                 'url': prop.url
                 }
        return value

    @staticmethod
    def __handle_nan__(num_float):
        if math.isnan(num_float):
            return None
        return num_float
