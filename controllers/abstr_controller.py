from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import abc


class CrawlRunner(object):
    def __init__(self, delay=1, req_per_ip=0):
        settings = get_project_settings()
        settings.set('LOG_LEVEL', 'WARNING')
        settings.set('DOWNLOAD_DELAY', delay)
        settings.set('CONCURRENT_REQUESTS_PER_IP', req_per_ip)
        settings.set('AUTOTHROTTLE_TARGET_CONCURRENCY', 0.5)
        settings.set('COOKIES_ENABLED', False)
        settings.set('USER_AGENT', 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0')
        self. process = CrawlerProcess(settings)

    @abc.abstractmethod
    def run(self):
        return
