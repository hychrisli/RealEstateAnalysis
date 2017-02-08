import scrapy
import re
# This is a spider for
# http://www.mlslistings.com/browse-listings#/


class MlsSpider(scrapy.Spider):
    name = "zipcode"

    def start_requests(self):
        url = 'http://www.mlslistings.com/browse-listings#/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.xpath('//ul[@class="BrowseMenu"]/li/a/@href').extract()

        if not links:
            return
        else:
            for href in links:
                if 'Southern' not in href:
                    print(href)
                    # yield scrapy.Request(url=href, callback=self.parse)


    def parse_county_page(self, response):
        return

    def parse_city_page(self):
        return




