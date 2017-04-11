from controllers.abstr_controller import CrawlRunner, BatchDispatcher
from crawlers.spiders.prop_addr_hist_spider import PropAddrHistSpider
from etl.dao.prop_addr_hist_dao import PropAddrHistDao
from utility.calculate import rand_non_repeat_agent, rand_batch_size
from utility.actions import rand_wait,show_progress

import os


class PropAddrHistRunner(CrawlRunner):
    def __init__(self, agent, batch_size):
        super(PropAddrHistRunner, self).__init__(delay=5, req_per_ip=1, agent=agent)
        print ("PropAddrHistRunner pid: " + str(os.getpid()))
        print ("My user agent number: " + str(agent))
        self.batch_size = batch_size

    def run(self):
        self.process.crawl(PropAddrHistSpider, batch_size=self.batch_size)
        self.process.start()


class PropAddrHistBatchDispatcher(BatchDispatcher):

    def __init__(self):
        super(PropAddrHistBatchDispatcher, self).__init__()
        self.cnx = PropAddrHistDao()

    def dispatch_jobs(self):
        print ("PropAddrHistBatchDispatcher.dispatch_jobs")
        self.cnx.init_cleanup()
        total_num = self.cnx.get_total_num()
        done_num = 0
        print("Total number of jobs: " + str(total_num))
        agent = None

        agent = rand_non_repeat_agent(agent)
        hist_runner = PropAddrHistRunner(agent, total_num)
        hist_runner.run()

        # while total_num > done_num:
        #     agent = rand_non_repeat_agent(agent)
        #     batch_size = rand_batch_size()
        #     pid = os.fork()
        #     if pid == 0:
        #         hist_runner = PropAddrHistRunner(agent, batch_size)
        #         hist_runner.run()
        #         os._exit(0)
        #
        #     os.waitpid(pid, 0)
        #     done_num += batch_size
        #     show_progress(done_num, total_num, 1, '')
        #     rand_wait("Batch finished")
        #     print ('\n')
