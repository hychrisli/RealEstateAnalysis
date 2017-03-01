from etl.dao.prop_addr_dao import PropAddrDao
from crawlers.selnms.prop_addr_url_selnm import PropAddrUrlSelnm
from controllers.realtor_controller import PropAddrHistRunner
from utility.calculate import random_non_repeating
import os
import time
from datetime import datetime
from random import randint

old = None
while True:
    agent = random_non_repeating(0, 10, old)
    pid = os.fork()
    if pid == 0:
        print ("Timestamp: " + str(datetime.now()))
        hist_runner = PropAddrHistRunner(agent)
        hist_runner.run()
        os._exit(0)

    old = agent
    os.waitpid(pid, 0)
    wait = (agent + 1) * randint(2, 6)
    print ("Wait for another round: " + str(wait) + 's\n')
    time.sleep(wait)

# hist_runner = PropAddrHistRunner()
# hist_runner.run()

# url_selnm = PropAddrUrlSelnm()
# url_selnm.upd_urls()

# 2017-02-21
# addr_cnx = PropAddrDao()
# addr_cnx.init_cleanup()
# addr_cnx.add_addrs()
