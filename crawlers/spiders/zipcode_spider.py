import scrapy
from lxml import etree

from db_ops.mysql_dao.zipcode_dao import ZipcodeConnector


# This is a spider for
# http://www.mlslistings.com/browse-listings#/


class ZipCodeSpider(scrapy.Spider):
    name = "zipcode"

    def __init__(self):
        super(ZipCodeSpider, self).__init__()
        self.connector = ZipcodeConnector()
        self.connector.init_cleanup()

    def start_requests(self):
        url = 'http://www.mlslistings.com/browse-listings#/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        nodes = self.__extract_nodes__(response)
        for node in nodes:
            (county, href) = self.__extract_name_href__(node)
            if 'Southern' not in county:
                if 'Central Valley' in county:
                    yield scrapy.Request(url=href, callback=self.parse)
                else:
                    self.connector.add_county(county)
                    yield scrapy.Request(url=href, callback=self.parse_county_page)

    def parse_county_page(self, response):
        nodes = ZipCodeSpider.__extract_nodes__(response)
        county = ZipCodeSpider.__extract_region__(response)
        county_id = self.connector.find_county_id(county)
        # print ("\nCOUNTY: " + county + " ID: " + str(county_id))
        for node in nodes:
            (city, href) = self.__extract_name_href__(node)
            self.connector.add_city(county_id, city)
            yield scrapy.Request(url=href, callback=self.parse_city_page)

    def parse_city_page(self, response):
        nodes = ZipCodeSpider.__extract_nodes__(response)
        city = ZipCodeSpider.__extract_region__(response)
        city_id = self.connector.find_city_id(city)
        # print("\nCITY: " + city + "ID: " + str(city_id))
        for node in nodes:
            (zipcode, href) = self.__extract_name_href__(node)
            self.connector.add_zipcode(city_id, zipcode)

    @staticmethod
    def __extract_nodes__(response):
        return response.xpath('//ul[@class="BrowseMenu"]/li/a').extract()

    @staticmethod
    def __extract_name_href__(node):
        tree = etree.HTML(node)
        name = tree.xpath('//a/text()')[0]
        href = tree.xpath('//a/@href')[0]
        return name, href

    @staticmethod
    def __extract_region__(response):
        return response.xpath('//section[@class="NB_skin_content"]/h1/text()').extract_first()