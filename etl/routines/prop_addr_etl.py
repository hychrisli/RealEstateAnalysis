from ..abstr_cnx import GenericConnector


class PropAddrEtl(GenericConnector):
    """Prop Address ETL """

    """Stored Procedures"""

    def call_sp_prop_addr_fact_upsert(self):
        self.logger.info("call sp_prop_addr_fact_upsert")
        self.cursor.execute('call sp_prop_addr_fact_upsert')

    def call_sp_prop_addr_hist_incr(self):
        self.logger.info("call sp_prop_addr_hist_incr")
        self.cursor.execute('call sp_prop_addr_hist_incr')
        self.__check_count_hist_rej_stg__()
        self.__check_count_hist_stg__()
        self.__check_count_hist_incr__()

    def call_sp_prop_addr_hist_uniq_incr(self):
        self.logger.info("call sp_prop_addr_hist_uniq_incr")
        self.cursor.execute('call sp_prop_addr_hist_uniq_incr')
        self.__check_count_hist_uniq_incr__()

    def call_sp_prop_addr_hist(self):
        cnt = self.__check_hist__()
        self.logger.info("call sp_prop_addr_hist")
        self.cursor.execute('call sp_prop_addr_hist')
        diff = self.__check_hist__() - cnt
        self.logger.info("Table: prop_addr_hist | New Records: " + str(diff))

    """Verification Section"""

    def __check_count_hist_rej_stg__(self):
        self._select_count_('prop_addr_hist_rej_stg')

    def __check_count_hist_stg__(self):
        self._select_count_('prop_addr_hist_stg')

    def __check_count_hist_incr__(self):
        self._select_count_('prop_addr_hist_incr')

    def __check_count_hist_uniq_incr__(self):
        self._select_count_('prop_addr_hist_uniq_incr')

    def __check_hist__(self):
        (max_sk, cnt) = self._select_single_row_(PropAddrEtl.__gen_hist_stmt__())
        self.logger.info("Table: prop_addr_hist | Max(HIST_SK): " +
                         str(max_sk) + " | Count: " + str(cnt))
        return cnt

    """SQL Statements"""

    @staticmethod
    def __gen_hist_stmt__():
        return "SELECT MAX(HIST_SK), COUNT(*) FROM prop_addr_hist"
