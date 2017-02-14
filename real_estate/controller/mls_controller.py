from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ..spiders.api_search_spider import ApiSearchSpider
from ..mysql.property_dao import PropertyConnector


def run_crawler():
    settings = get_project_settings()
    settings.set('LOG_LEVEL', 'INFO')
    mysql_cnx = PropertyConnector()
    mysql_cnx.init_cleanup()
    zipcodes = ['93907', '93901', '93908']
    process = CrawlerProcess(settings)
    for zipcode in zipcodes:
        process.crawl(ApiSearchSpider, zipcode=zipcode)
    process.start()