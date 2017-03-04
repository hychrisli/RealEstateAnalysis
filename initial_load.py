from controllers.realtor_controller import PropAddrHistBatchDispatcher
from etl.dao.prop_addr_dao import PropAddrDao
from etl.routines.prop_addr_etl import PropAddrEtl
from crawlers.selnms.prop_addr_url_selnm import PropAddrUrlSelnm
from controllers.realtor_controller import PropAddrHistRunner
from utility.calculate import random_non_repeating
import os
import time
from datetime import datetime
from random import randint


dispatcher = PropAddrHistBatchDispatcher()
dispatcher.dispatch_jobs()


# print ("PropAddrUrlSelnm.upd_urls")
# url_selnm = PropAddrUrlSelnm()
# url_selnm.upd_urls()
#
# print ("call sp_prop_addr_fact_upsert")
# prop_addr_etl_cnx = PropAddrEtl()
# prop_addr_etl_cnx.call_sp_prop_addr_fact_upsert()


# hist_runner = PropAddrHistRunner()
# hist_runner.run()

# url_selnm = PropAddrUrlSelnm()
# url_selnm.upd_urls()

# 2017-02-21
# addr_cnx = PropAddrDao()
# addr_cnx.init_cleanup()
# addr_cnx.add_addrs()
