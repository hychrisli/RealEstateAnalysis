from ..abstr_cnx import GenericConnector
from utility.actions import show_progress, get_hms
from utility.constants import PROP_ADDR_PRICE_MONTH_RPT_TAB, PROP_ADDR_PRICE_DAY_RPT_STG_TAB
from utility.constants import V_AREA_IDS
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time


class PropAddrPriceRptEtl(GenericConnector):

    START_DATE = datetime.strptime('2010-01-01', '%Y-%m-%d')
    END_DATE = datetime.strptime('2017-03-01', '%Y-%m-%d') # Not included
    END_MONTH = END_DATE

    def run(self):

        self.__clean_table__(PROP_ADDR_PRICE_MONTH_RPT_TAB)
        start_time = time.time()

        month = PropAddrPriceRptEtl.START_DATE
        tot_days = (PropAddrPriceRptEtl.END_DATE - PropAddrPriceRptEtl.START_DATE).days
        date = PropAddrPriceRptEtl.START_DATE

        while month < PropAddrPriceRptEtl.END_MONTH:
            print("Month: " + month.strftime('%Y-%m') + ' | Time elapsed: ' + get_hms(time.time() - start_time))
            self.__clean_table__(PROP_ADDR_PRICE_DAY_RPT_STG_TAB)
            next_month = month + relativedelta(months=+1)

            while date < next_month:
                self.__call_sp_prop_addr_price_day_rpt_stg__(date.strftime('%Y-%m-%d'))
                date += timedelta(days=1)

            done_days = (date - PropAddrPriceRptEtl.START_DATE).days + 1
            show_progress(done_days, tot_days, 1, '\n')
            self.__call_sp_prop_addr_price_month_rpt__()
            month = next_month

    def sample_hist_price(self):
        area_ids = self.__select_area_ids__()
        cur_county_id = 0
        rpt_res = self.__select_all__(PropAddrPriceRptEtl.__gen_sample_select_stmt__())
        print(rpt_res)
        # for (county_id, city_id, zipcode) in area_ids:

    def __call_sp_prop_addr_price_day_rpt_stg__(self, date_str):
        self.cursor.execute('CALL sp_prop_addr_price_day_rpt_stg(\'' + date_str + '\')')

    def __call_sp_prop_addr_price_month_rpt__(self):
        self.cursor.execute('CALL sp_prop_addr_price_month_rpt')

    def __select_area_ids__(self):
        return self.__select_all__('SELECT COUNTY_ID, CITY_ID, ZIPCODE FROM ' + V_AREA_IDS)

    @staticmethod
    def __gen_sample_select_stmt__(county_id=0, city_id=0, zipcode=0, prop_type_id=0):

        where_clause = ""
        groupby_clause = ""

        (where_clause, groupby_clause) = PropAddrPriceRptEtl.__extend_clauses__(
            where_clause, groupby_clause, "COUNTY_ID", county_id)
        (where_clause, groupby_clause) = PropAddrPriceRptEtl.__extend_clauses__(
            where_clause, groupby_clause, "CITY_ID", city_id)
        (where_clause, groupby_clause) = PropAddrPriceRptEtl.__extend_clauses__(
            where_clause, groupby_clause, "ZIPCODE", zipcode)
        (where_clause, groupby_clause) = PropAddrPriceRptEtl.__extend_clauses__(
            where_clause, groupby_clause, "PROP_TYPE_ID", prop_type_id)

        if groupby_clause:
            groupby_clause += ", RPT_DATE"
        else:
            groupby_clause = " GROUP BY RPT_DATE"

        return PropAddrPriceRptEtl.__get_sample_select_part__(county_id, city_id, zipcode, prop_type_id) \
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
               "FROM " + PROP_ADDR_PRICE_MONTH_RPT_TAB + " "