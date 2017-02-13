import scrapy
from lxml import etree
from ..mysql.zipcode_dao import MySqlConnector
# This is a spider for
# http://www.mlslistings.com/browse-listings#/


class ZipCodeSpider(scrapy.Spider):
    name = "zipcode"

    def __init__(self):
        super(ZipCodeSpider, self).__init__()
        self.connector = MySqlConnector()

    def start_requests(self):
        url = 'http://www.mlslistings.com/browse-listings#/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        nodes = response.xpath('//ul[@class="BrowseMenu"]/li/a').extract()

        # links = response.xpath('//ul[@class="BrowseMenu"]/li/a/@href').extract()
        if not nodes:
            return
        else:
            for node in nodes:
                tree = etree.HTML(node)
                name = tree.xpath('//a/text()')[0]
                href = tree.xpath('//a/@href')[0]
                if 'Southern' not in href:
                    print(name)
                    print(href)
                    self.connector.add_county(name)
                    # yield scrapy.Request(url=href, callback=self.parse)
        # self.connector.close()


    def parse_county_page(self, response):
        return

    def parse_city_page(self):
        return




