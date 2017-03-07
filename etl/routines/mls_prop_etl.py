from ..abstr_cnx import GenericConnector


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
        before_res = self.__check_count_status_dim__()
        print("call sp_mls_status_hist_upd")
        self.cursor.execute("CALL sp_mls_status_hist_upd")
        after_res = self.__check_count_status_dim__()
        MlsPropEtl.__diff_status__(before_res, after_res)

    """Verification"""

    def __check_count_prop_incr__(self):
        self._select_count_('mls_prop_incr')

    def __check_count_status_dim__(self):
        return self.__select_all__(MlsPropEtl.__gen_status_dim_select_stmt__())

    """SQL Statements"""

    @staticmethod
    def __gen_status_dim_select_stmt__():
        return "SELECT STATUS_EVENT_ID, COUNT(*) from mls_status_dim " \
               "GROUP BY status_event_id ORDER BY status_event_id"

    @staticmethod
    def __diff_status__(before, after):

        length = len(before)

        print ("Event\t| Bfr\t| Aftr\t| Diff")
        for i in range(0, length):
            diff = after[i][1] - before[i][1]
            print(str(before[i][0]) + "\t| " + str(before[i][1]) +
                  "\t| " + str(after[i][1]) + "\t| " + str(diff))
