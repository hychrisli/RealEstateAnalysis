from ..abstr_cnx import GenericConnector
from utility.actions import show_progress
from datetime import datetime, timedelta


class PropAddrPriceRptEtl(GenericConnector):
    PROP_ADDR_PRICE_RPT_TAB = 'prop_addr_price_rpt'

    def run(self):
        self.__init_clean__()
        start_date = datetime.strptime('2015-01-01', '%Y-%m-%d')
        end_date = datetime.today() - + timedelta(days=7)
        tot_days = (end_date - start_date).days + 1
        date = start_date
        while date <= end_date:
            self.__call_sp_prop_addr_price_rpt__(date.strftime('%Y-%m-%d'))
            done_days = (date - start_date).days + 1
            show_progress(done_days, tot_days, 15, 'Processed: ' + date.strftime('%Y-%m-%d') + '\n')
            date += timedelta(days=1)

    def __init_clean__(self):
        self.__clean_table__(PropAddrPriceRptEtl.PROP_ADDR_PRICE_RPT_TAB)

    def __call_sp_prop_addr_price_rpt__(self, date_str):
        self.cursor.execute('CALL sp_prop_addr_price_rpt(\'' + date_str + '\')')
