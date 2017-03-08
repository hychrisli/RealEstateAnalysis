from controllers.mls_controller import ApiSearchRunner, PropPageRunner, MlsDispatcher
from controllers.realtor_controller import PropAddrHistBatchDispatcher
from etl.routines.mls_prop_etl import MlsPropEtl
from etl.dao.prop_addr_dao import PropAddrDao
from etl.routines.prop_addr_etl import PropAddrEtl
from crawlers.selnms.prop_addr_url_selnm import PropAddrUrlSelnm

""" Initialize Connections """

mls_etl_cnx = MlsPropEtl()
prop_addr_etl_cnx = PropAddrEtl()


""" API Search spider within a child process """
api_search_dispatcher = MlsDispatcher(ApiSearchRunner)
api_search_dispatcher.dispatch_jobs()

""" Populate mls_prop_incr table """
mls_etl_cnx.call_sp_mls_prop_incr_insert()

""" Property page spider within a child process """
prop_page_dispatcher = MlsDispatcher(PropPageRunner)
prop_page_dispatcher.dispatch_jobs()

""" MLS ETL stored procedures"""
mls_etl_cnx.call_sp_prop_del_mls_excld()
mls_etl_cnx.call_sp_mls_prop_fact_insert()
mls_etl_cnx.call_sp_mls_prop_dim_upd()

print ("PropAddrDao.add_addrs")
addr_cnx = PropAddrDao()
addr_cnx.init_cleanup()
addr_cnx.add_addrs()

print ("PropAddrUrlSelnm.upd_urls")
url_selnm = PropAddrUrlSelnm()
url_selnm.upd_urls()

prop_addr_etl_cnx.call_sp_prop_addr_fact_upsert()

""" Property address history spider within child processes """
prop_addr_hist_dispatcher = PropAddrHistBatchDispatcher()
prop_addr_hist_dispatcher.dispatch_jobs()

prop_addr_etl_cnx.call_sp_prop_addr_hist_incr()
prop_addr_etl_cnx.call_sp_prop_addr_hist_uniq_incr()
prop_addr_etl_cnx.call_sp_prop_addr_hist()
mls_etl_cnx.call_sp_mls_status_hist_upd()
mls_etl_cnx.call_sp_mls_price_rpt()

mls_etl_cnx.close()
prop_addr_etl_cnx.close()