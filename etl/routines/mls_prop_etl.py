from ..abstr_cnx import GenericConnector
from utility.constants import MLS_DAILY_RPT_TAB


class MlsPropEtl(GenericConnector):

    def call_sp_mls_prop_incr_insert(self):

        print ("call sp_mls_prop_incr_insert")
        self.cursor.execute("CALL sp_mls_prop_incr_insert")
        self.__check_count_prop_incr__()

    def call_sp_prop_del_mls_excld(self):
        print ("call sp_prop_del_mls_excld")
        self.cursor.execute("CALL sp_prop_del_mls_excld")

    def call_sp_mls_prop_fact_insert(self):
        print ("call sp_mls_prop_fact_insert")
        self.cursor.execute("CALL sp_mls_prop_fact_insert")

    def call_sp_mls_prop_dim_upd(self):
        print ("call sp_mls_prop_dim_upd")
        self.cursor.execute("CALL sp_mls_prop_dim_upd")

    def call_sp_mls_status_hist_upd(self):
        print("call sp_mls_status_hist_upd")
        self.cursor.execute("CALL sp_mls_status_hist_upd")

    def call_sp_mls_price_rpt(self):
        self._select_count_('mls_price_rpt')
        print("call sp_mls_price_rpt")
        self.cursor.execute("CALL sp_mls_price_rpt")
        self._select_count_('mls_price_rpt')

    def call_sp_mls_daily_rpt(self):
        print("call sp_" + MLS_DAILY_RPT_TAB)
        self.cursor.execute("CALL sp_" + MLS_DAILY_RPT_TAB)
        self._select_count_(MLS_DAILY_RPT_TAB)

    """Verification"""

    def __check_count_prop_incr__(self):
        self._select_count_('mls_prop_incr')

    def check_count_status_dim(self):
        return self.__select_all__(MlsPropEtl.__gen_status_dim_select_stmt__())

    def __check_count_mls_price_rpt(self):
        self._select_count_('mls_price_rpt')

    """SQL Statements"""

    @staticmethod
    def __gen_status_dim_select_stmt__():
        return "SELECT STATUS_EVENT_ID, COUNT(*) from mls_status_dim " \
               "GROUP BY status_event_id ORDER BY status_event_id"

    @staticmethod
    def diff_status(before, after):

        length = len(before)

        print ("Event\t| Bfr\t| Aftr\t| Diff")
        for i in range(0, length):
            diff = after[i][1] - before[i][1]
            print(str(before[i][0]) + "\t| " + str(before[i][1]) +
                  "\t| " + str(after[i][1]) + "\t| " + str(diff))
