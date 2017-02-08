import scrapy
from scrapy_splash import SplashRequest


class ListingSpider(scrapy.Spider):
    name = "listing"
    start_urls = ["http://www.mlslistings.com/search/keyword/95008/openhouse/false/listingstatus/1/propertyclass/1"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='render.html',
                args={'wait': 0.5},
            )

    def parse(self, response):
        items = response.xpath('//span[@class="mobileAddress ng-binding"]/text()').extract()
        print(items)