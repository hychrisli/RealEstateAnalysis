from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import abc


class CrawlRunner(object):
    def __init__(self, delay=1):
        settings = get_project_settings()
        settings.set('LOG_LEVEL', 'WARNING')
        settings.set('DOWNLOAD_DELAY', delay)
        self. process = CrawlerProcess(settings)

    @abc.abstractmethod
    def run(self):
        return
