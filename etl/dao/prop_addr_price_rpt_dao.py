from ..abstr_cnx import GenericConnector
from utility.constants import PROP_ADDR_PRICE_RPT_TAB, V_PRICE_MONTH_RPT
from utility.constants import V_AREA_IDS


class PropAddrPriceRptDao(GenericConnector):
    SQFT_PRICE_INTVL = 10.0
    IDX_AVG_PRICE_STRUCT_SQFT = 6

    # 0 means N/A. For 1 - 5, check prop_type_lkp table
    PROP_TYPE_IDS = range(0, 6)

    def __init__(self):
        super(PropAddrPriceRptDao, self).__init__()
        self.insert_stmt = PropAddrPriceRptDao.__gen_insert_stmt__()

    def load_prop_addr_price_rpt(self):
        self.__clean_table__(PROP_ADDR_PRICE_RPT_TAB)
        area_ids = self.__select_area_ids__()

        # Load default batch for the entire bay area
        self.__load_batch__()
        self.__print_status__()

        cur_county_id = 0
        cur_city_id = 0
        for (county_id, city_id, zipcode) in area_ids:

            if cur_county_id != county_id:
                self.__load_batch__(county_id)
                cur_county_id = county_id
                self.__print_status__(county_id)

            if cur_city_id != city_id:
                self.__load_batch__(cur_county_id, city_id)
                cur_city_id = city_id
                self.__print_status__(cur_county_id, city_id)

            self.__load_batch__(county_id, city_id, zipcode)
            self.__print_status__(cur_county_id, city_id, zipcode)

    def __select_area_ids__(self):
        return self.__select_all__('SELECT COUNTY_ID, CITY_ID, ZIPCODE FROM ' + V_AREA_IDS)

    def __load_batch__(self, county_id=0, city_id=0, zipcode=0):

        for prop_type_id in PropAddrPriceRptDao.PROP_TYPE_IDS:
            select_stmt = PropAddrPriceRptDao.__gen_sample_select_stmt__(county_id, city_id, zipcode, prop_type_id)
            rpt_res = self.__select_all__(select_stmt)
            sample_res = PropAddrPriceRptDao.__sample_records__(rpt_res)
            self.cursor.executemany(self.insert_stmt, sample_res)

    @staticmethod
    def __gen_insert_stmt__():
        return "INSERT INTO " + PROP_ADDR_PRICE_RPT_TAB + \
               " (COUNTY_ID, CITY_ID, ZIPCODE, PROP_TYPE_ID, RPT_DATE," \
               " AVG_PRICE, AVG_PRICE_STRUCT_SQFT, AVG_PRICE_TOT_SQFT)" \
               " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    @staticmethod
    def __sample_records__(rpt_res):
        pre_price = 0.0
        sample_res = []
        if len(rpt_res) > 1:
            for record in rpt_res[:-1]:
                avg_price_stuct_sqft = float(record[PropAddrPriceRptDao.IDX_AVG_PRICE_STRUCT_SQFT])

                if avg_price_stuct_sqft > float(pre_price) + PropAddrPriceRptDao.SQFT_PRICE_INTVL:
                    sample_res.append(record)
                    pre_price = avg_price_stuct_sqft

            sample_res.append(rpt_res[-1])
        return sample_res

    @staticmethod
    def __gen_sample_select_stmt__(county_id=0, city_id=0, zipcode=0, prop_type_id=0):

        where_clause = ""
        groupby_clause = ""

        (where_clause, groupby_clause) = PropAddrPriceRptDao.__extend_clauses__(
            where_clause, groupby_clause, "COUNTY_ID", county_id)
        (where_clause, groupby_clause) = PropAddrPriceRptDao.__extend_clauses__(
            where_clause, groupby_clause, "CITY_ID", city_id)
        (where_clause, groupby_clause) = PropAddrPriceRptDao.__extend_clauses__(
            where_clause, groupby_clause, "ZIPCODE", zipcode)
        (where_clause, groupby_clause) = PropAddrPriceRptDao.__extend_clauses__(
            where_clause, groupby_clause, "PROP_TYPE_ID", prop_type_id)

        if groupby_clause:
            groupby_clause += ", RPT_DATE"
        else:
            groupby_clause = " GROUP BY RPT_DATE"

        return PropAddrPriceRptDao.__get_sample_select_part__(county_id, city_id, zipcode, prop_type_id) \
               + where_clause + groupby_clause

    @staticmethod
    def __extend_clauses__(where_clause, groupby_clause, field, value):
        if value:
            if where_clause:
                where_clause += " AND " + field + " = " + str(value)
                groupby_clause += ", " + field
            else:
                where_clause = " WHERE " + field + " = " + str(value)
                groupby_clause = " GROUP BY " + field
        return where_clause, groupby_clause

    @staticmethod
    def __get_sample_select_part__(county_id=0, city_id=0, zipcode=0, prop_type_id=0):
        return "SELECT " + str(county_id) + " COUNTY_ID, " \
               + str(city_id) + " CITY_ID, " \
               + str(zipcode) + " ZIPCODE, " \
               + str(prop_type_id) + " PROP_TYPE_ID, RPT_DATE, " \
                                     "ROUND(SUM(AVG_PRICE * DAY_AVG_NUM) / SUM(DAY_AVG_NUM), 2) AVG_PRICE, " \
                                     "ROUND(SUM(AVG_PRICE_STRUCT_SQFT * DAY_AVG_NUM) / SUM(DAY_AVG_NUM), 2) AVG_PRICE_STRUCT_SQFT, " \
                                     "ROUND(SUM(AVG_PRICE_TOT_SQFT * DAY_AVG_NUM) / SUM(DAY_AVG_NUM), 2) AVG_PRICE_TOT_SQFT " \
                                     "FROM " + V_PRICE_MONTH_RPT + " "

    def __print_status__(self, county_id=0, city_id=0, zipcode=0):
        self.logger.info("Finished loading county_id: " + str(county_id)
                         + " | city_id: " + str(city_id) + " | zipcode: " + str(zipcode))
