from controllers.mls_controller import ApiSearchRunner, PropPageRunner, MlsDispatcher
from controllers.realtor_controller import PropAddrHistBatchDispatcher
from etl.routines.mls_prop_etl import MlsPropEtl
from etl.dao.prop_addr_dao import PropAddrDao
from etl.dao.prop_addr_price_rpt_dao import PropAddrPriceRpt
from etl.routines.prop_addr_etl import PropAddrEtl
from etl.routines.prop_addr_price_rpt_etl import PropAddrPriceRptEtl
from crawlers.selnms.prop_addr_url_selnm import PropAddrUrlSelnm


""" API Search spider within a child process """
api_search_dispatcher = MlsDispatcher(ApiSearchRunner)
api_search_dispatcher.dispatch_jobs()

""" Populate mls_prop_incr table """
mls_etl_cnx = MlsPropEtl()
before_res = mls_etl_cnx.check_count_status_dim()
mls_etl_cnx.call_sp_mls_prop_incr_insert()
mls_etl_cnx.close()

""" Property page spider within a child process """
prop_page_dispatcher = MlsDispatcher(PropPageRunner)
prop_page_dispatcher.dispatch_jobs()

""" MLS ETL stored procedures"""
mls_etl_cnx = MlsPropEtl()
mls_etl_cnx.call_sp_prop_del_mls_excld()
mls_etl_cnx.call_sp_mls_prop_fact_insert()
mls_etl_cnx.call_sp_mls_prop_dim_upd()
mls_etl_cnx.close()

print ("PropAddrDao.add_addrs")
addr_cnx = PropAddrDao()
addr_cnx.init_cleanup()
addr_cnx.add_addrs()
addr_cnx.close()

prop_addr_etl_cnx = PropAddrEtl()
prop_addr_etl_cnx.call_sp_prop_addr_fact_upsert()
prop_addr_etl_cnx.close()

""" Property address history spider within child processes """
prop_addr_hist_dispatcher = PropAddrHistBatchDispatcher()
prop_addr_hist_dispatcher.dispatch_jobs()

prop_addr_etl_cnx = PropAddrEtl()
prop_addr_etl_cnx.call_sp_prop_addr_hist_incr()
prop_addr_etl_cnx.call_sp_prop_addr_hist_uniq_incr()
prop_addr_etl_cnx.call_sp_prop_addr_hist()
prop_addr_etl_cnx.close()

mls_etl_cnx = MlsPropEtl()
mls_etl_cnx.call_sp_mls_status_hist_upd()
mls_etl_cnx.call_sp_mls_price_rpt()
mls_etl_cnx.call_sp_mls_daily_rpt()
after_res = mls_etl_cnx.check_count_status_dim()
mls_etl_cnx.diff_status(before_res, after_res)
mls_etl_cnx.close()

""" Property Address Price Report"""
prop_month_rpt_cnx = PropAddrPriceRptEtl()
prop_month_rpt_cnx.run()
prop_month_rpt_cnx.close()

prop_rpt_cnx = PropAddrPriceRpt()
prop_rpt_cnx.load_prop_addr_price_rpt()
prop_rpt_cnx.close()
