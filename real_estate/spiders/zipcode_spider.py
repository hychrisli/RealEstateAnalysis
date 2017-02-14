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
        nodes = self.__extract_nodes__(response)
        county = response.xpath('//section[@class="NB_skin_content"]/h1/text()').extract_first()
        county_id = self.connector.find_county_id(county)
        print ("\nCOUNTY: " + county + " ID: " + str(county_id))
        for node in nodes:
            (city, href) = self.__extract_name_href__(node)
            self.connector.add_city(county_id, city)

    def parse_city_page(self):
        return

    def __extract_nodes__(self, response):
        return response.xpath('//ul[@class="BrowseMenu"]/li/a').extract()

    def __extract_name_href__(self, node):
        tree = etree.HTML(node)
        name = tree.xpath('//a/text()')[0]
        href = tree.xpath('//a/@href')[0]
        return (name, href)
