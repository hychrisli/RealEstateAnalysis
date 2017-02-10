from __future__ import print_function
import scrapy
from scrapy_splash import SplashRequest
from lxml import etree


class ApiSearchSpider(scrapy.Spider):
    name = 'api_search'

    def start_requests(self):
        url = 'http://api.mlslistings.com'
        post_json = '{"display":{"pageNumber":1,"itemsPerPage":200},"cityName":"",' \
                    '"countyName":"","zipCode":"94086","mlsNumber":"","address":"",' \
                    '"beds":"","baths":"","listSalePrice":""}'
        yield SplashRequest(url, self.parse,
                            endpoint='render.json',
                            args={'wait': 0.5,
                                  'http_method': 'POST',
                                  'body': post_json})

    def parse(self, response):
        nodes = response.xpath('//div[@class="ng-scope"]').extract()
        f = open('f.html', 'w')
        #print('Number of listings: ' + str(len(nodes)))
        print(response.data, file=f)
        f.close()
        # for node in nodes:
        #     tree = etree.HTML(node)
        #     print(tree.xpath('//span[@class="longAddress ng-binding"]/text()')[0])
