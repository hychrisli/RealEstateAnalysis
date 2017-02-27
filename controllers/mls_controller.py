from controllers.abstr_controller import CrawlRunner
from crawlers.spiders.property_page_spider import PropertyPageSpider
from crawlers.spiders.api_search_spider import ApiSearchSpider

import os


class ApiSearchRunner(CrawlRunner):
    def __init__(self):
        super(ApiSearchRunner, self).__init__()
        print ("ApiSearchRunner pid: " + str(os.getpid()))

    def run(self):
        self.process.crawl(ApiSearchSpider)
        self.process.start()


class PropPageRunner(CrawlRunner):
    def __init__(self):
        super(PropPageRunner, self).__init__()
        print ("PropPageRunner pid: " + str(os.getpid()))

    def run(self):
        self.process.crawl(PropertyPageSpider)
        self.process.start()
