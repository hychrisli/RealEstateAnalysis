from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawlers.spiders.property_page_spider import PropertyPageSpider


class CrawlRunner:
    def __init__(self):
        settings = get_project_settings()
        settings.set('LOG_LEVEL', 'WARNING')
        settings.set('DOWNLOAD_DELAY', 0.25)
        self. process = CrawlerProcess(settings)

    def run(self):
        self.process.crawl(PropertyPageSpider)
        self.process.start()
