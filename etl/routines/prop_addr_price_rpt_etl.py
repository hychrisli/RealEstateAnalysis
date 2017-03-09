from ..abstr_cnx import GenericConnector
from utility.actions import show_progress, get_hms
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time


class PropAddrPriceRptEtl(GenericConnector):
    PROP_ADDR_PRICE_MONTH_RPT_TAB = 'prop_addr_price_month_rpt'
    PROP_ADDR_PRICE_DAY_RPT_STG_TAB = 'prop_addr_price_day_rpt_stg'
    START_DATE = datetime.strptime('2010-01-01', '%Y-%m-%d')
    END_DATE = datetime.strptime('2017-03-01', '%Y-%m-%d') # Not included
    END_MONTH = END_DATE

    def run(self):

        self.__clean_table__(PropAddrPriceRptEtl.PROP_ADDR_PRICE_MONTH_RPT_TAB)
        start_time = time.time()

        month = PropAddrPriceRptEtl.START_DATE
        tot_days = (PropAddrPriceRptEtl.END_DATE - PropAddrPriceRptEtl.START_DATE).days
        date = PropAddrPriceRptEtl.START_DATE

        while month < PropAddrPriceRptEtl.END_MONTH:
            print("Month: " + month.strftime('%Y-%m') + ' | Time elapsed: ' + get_hms(time.time() - start_time))
            self.__clean_table__(PropAddrPriceRptEtl.PROP_ADDR_PRICE_DAY_RPT_STG_TAB)
            next_month = month + relativedelta(months=+1)

            while date < next_month:
                self.__call_sp_prop_addr_price_day_rpt_stg__(date.strftime('%Y-%m-%d'))
                date += timedelta(days=1)

            done_days = (date - PropAddrPriceRptEtl.START_DATE).days + 1
            show_progress(done_days, tot_days, 1, '\n')
            self.__call_sp_prop_addr_price_month_rpt__()
            month = next_month

    def __call_sp_prop_addr_price_day_rpt_stg__(self, date_str):
        self.cursor.execute('CALL sp_prop_addr_price_day_rpt_stg(\'' + date_str + '\')')

    def __call_sp_prop_addr_price_month_rpt__(self):
        self.cursor.execute('CALL sp_prop_addr_price_month_rpt')
