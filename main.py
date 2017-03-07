from controllers.mls_controller import ApiSearchRunner
from controllers.mls_controller import PropPageRunner
from controllers.realtor_controller import PropAddrHistBatchDispatcher
from etl.routines.mls_prop_etl import MlsPropEtl
from etl.dao.prop_addr_dao import PropAddrDao
from etl.routines.prop_addr_etl import PropAddrEtl
from crawlers.selnms.prop_addr_url_selnm import PropAddrUrlSelnm

import os

mls_etl_cnx = MlsPropEtl()
prop_addr_etl_cnx = PropAddrEtl()

pid = os.fork()
if pid == 0:
    print ("api_search_runner")
    api_search_runner = ApiSearchRunner()
    api_search_runner.run()
    os._exit(0)

os.waitpid(pid, 0)

mls_etl_cnx.call_sp_mls_prop_incr_insert()

print ("prop_page_runner")
prop_page_runner = PropPageRunner()
prop_page_runner.run()

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

print ("PropAddrHistBatchDispatcher.dispatch_jobs")
dispatcher = PropAddrHistBatchDispatcher()
dispatcher.dispatch_jobs()

prop_addr_etl_cnx.call_sp_prop_addr_hist_incr()
prop_addr_etl_cnx.call_sp_prop_addr_hist()
mls_etl_cnx.call_sp_mls_status_hist_upd()


mls_etl_cnx.close()
prop_addr_etl_cnx.close()