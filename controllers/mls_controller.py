from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawlers.spiders.property_page_spider import PropertyPageSpider
from crawlers.spiders.api_search_spider import ApiSearchSpider
from multiprocessing import Process
import abc, os, threading


class CrawlRunner(object):
    def __init__(self):
        settings = get_project_settings()
        settings.set('LOG_LEVEL', 'WARNING')
        settings.set('DOWNLOAD_DELAY', 0.25)
        self. process = CrawlerProcess(settings)

    @abc.abstractmethod
    def run(self):
        return


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
