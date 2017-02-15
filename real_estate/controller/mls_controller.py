from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals, log
from scrapy.xlib.pydispatch import dispatcher
from ..spiders.api_search_spider import ApiSearchSpider
from ..mysql.property_dao import PropertyConnector
from ..mysql.zipcode_dao import ZipcodeConnector


class CrawlRunner:
    def __init__(self):
        self.running_crawlers = []
        dispatcher.connect(self.spider_closing, signal=signals.spider_closed)
        self.settings = get_project_settings()
        self.settings.set('LOG_LEVEL', 'ERROR')
        self.process = CrawlerProcess(self.settings)

    def spider_closing(self, spider):
        log.msg("Spider closed: %s" % spider, level=log.INFO)
        self.running_crawlers.remove(spider)
        if not self.running_crawlers:
            self.process.stop()

    def run(self):
        prop_cnx = PropertyConnector()
        prop_cnx.init_cleanup()
        prop_cnx.close()

        # zipcodes = ['93907', '93901', '93908']
        zip_cnx = ZipcodeConnector()
        zipcodes = zip_cnx.get_zipcode_lst()
        zip_cnx.close()
        # count = 0

        for (zipcode, ) in zipcodes:
            spider = ApiSearchSpider(zipcode)
            self.running_crawlers.append(spider)

            # self.process.crawl(ApiSearchSpider, zipcode=zipcode)
            self.process.crawl(spider, zipcode=zipcode)
            self.process.start()
            # count += 1
            # if count > 10:
            #     break



