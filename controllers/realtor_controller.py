from controllers.abstr_controller import CrawlRunner
from crawlers.spiders.prop_addr_hist_spider import PropAddrHistSpider


class PropAddrHistRunner(CrawlRunner):
    def __init__(self, agent):
        super(PropAddrHistRunner, self).__init__(delay=30, req_per_ip=1, agent=agent)
        print ("My user agent number: " + str(agent))

    def run(self):
        self.process.crawl(PropAddrHistSpider)
        self.process.start()
