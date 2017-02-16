from ..generic_connector import GenericConnector


class ZipcodeDao(GenericConnector):

    def init_cleanup(self):
        self.__clean_table__("ZIPCODE")
        self.__clean_table__("CITY")
        self.__clean_table__("COUNTY")

    def add_county(self, county):

        insert_stmt = "INSERT INTO COUNTY (NAME) VALUES ( %(county)s )"
        value = {'county':  str(county)}
        return self.__exec_single_insert__(insert_stmt, value)

    def add_city(self, county_id, city):
        insert_stmt = ("INSERT INTO CITY (NAME, COUNTY_ID) "
                       "VALUES ( %(city)s, %(county_id)s )")
        value = {'city': str(city),
                 'county_id': county_id}
        return self.__exec_single_insert__(insert_stmt, value)

    def add_zipcode(self, city_id, zipcode):
        insert_stmt = ("INSERT INTO ZIPCODE (ZIPCODE, CITY_ID) "
                       "VALUES ( %(zipcode)s, %(city_id)s )")
        value = {'zipcode': str(zipcode),
                 'city_id': city_id}
        return self.__exec_single_insert__(insert_stmt, value)

    def find_county_id(self, county):
        select_stmt = "SELECT COUNTY_ID FROM COUNTY WHERE LOWER(NAME) = %(county)s"
        value = {'county': str(county).lower()}
        return self.__exec_single_select__(select_stmt, value)

    def find_city_id(self, city):
        select_stmt = "SELECT CITY_ID FROM CITY WHERE LOWER(NAME) = %(city)s"
        value = {'city': str(city).lower()}
        return self.__exec_single_select__(select_stmt, value)

    def get_zipcode_lst(self):
        select_stmt = "SELECT DISTINCT ZIPCODE FROM ZIPCODE"
        self.cursor.execute(select_stmt)
        return self.cursor.fetchall()

    def __exec_single_select__(self, select_stmt, value):
        self.cursor.execute(select_stmt, value)
        return self.cursor.fetchone()[0]
