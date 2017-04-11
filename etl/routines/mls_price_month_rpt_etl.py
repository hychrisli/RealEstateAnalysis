from ..abstr_cnx import GenericConnector
from utility.constants import MLS_PRICE_MONTH_RPT_TAB
from datetime import date
from dateutil.relativedelta import relativedelta
from etl.dao.prop_addr_price_rpt_dao import PropAddrPriceRptDao


class MlsPriceMonthRptEtl(GenericConnector):

    def call_sp_mls_price_month_rpt(self):
        latest_date = self.__get_latest_date__()

        if latest_date is None:
            latest_date = date.today() - relativedelta(months=3)

        if date.today() - relativedelta(months=2) >= latest_date:
            print ("call sp_mls_price_month_rpt")
            self.cursor.execute("CALL sp_mls_price_month_rpt")

            prop_rpt_cnx = PropAddrPriceRptDao()
            prop_rpt_cnx.load_prop_addr_price_rpt()
            prop_rpt_cnx.close()

    def __get_latest_date__(self):
        select_stmt = 'SELECT MAX(RPT_DATE) FROM ' + MLS_PRICE_MONTH_RPT_TAB
        return self._select_single_value_(select_stmt)
