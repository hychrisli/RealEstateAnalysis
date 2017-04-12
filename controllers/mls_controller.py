#!/bin/python
from controllers.abstr_controller import CrawlRunner, BatchDispatcher
from crawlers.spiders.property_page_spider import PropertyPageSpider
from crawlers.spiders.api_search_spider import ApiSearchSpider
from crawlers.spiders.api_search_probe_spider import ApiSearchProbeSpider
from utility.constants import REA_ROOT_LOGGER

import os


class ApiSearchRunner(CrawlRunner):
    def __init__(self):
        super(ApiSearchRunner, self).__init__()
        # print("ApiSearchRunner pid: " + str(os.getpid()))
        self.logger.info("ApiSearchRunner pid: " + str(os.getpid()))

    def run(self):
        self.process.crawl(ApiSearchSpider)
        self.process.start()


class PropPageRunner(CrawlRunner):
    def __init__(self):
        super(PropPageRunner, self).__init__()
        self.logger.info("PropPageRunner pid: " + str(os.getpid()))

    def run(self):
        self.process.crawl(PropertyPageSpider)
        self.process.start()


class MlsDispatcher(BatchDispatcher):

    def __init__(self, runner_class):
        super(MlsDispatcher, self).__init__()
        self.runner_class = runner_class

    def dispatch_jobs(self):
        # print ("MlsDispatcher.dispatch_jobs")
        self.logger.info("MlsDispatcher.dispatch_jobs")
        # runner = self.runner_class()
        # runner.run()

        pid = os.fork()
        if pid == 0:
            runner = self.runner_class()
            runner.run()
            os._exit(0)

        os.waitpid(pid, 0)
