import scrapy
from lxml import etree

class PropHistSpider(scrapy.Spider):
    name = "prop_hist"

    def start_requests(self):
        url = "http://www.realtor.com/realestateandhomes-detail/490-S-Bayview-Ave_Sunnyvale_CA_94086_M27263-77808"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        rows = response.xpath('//div[@id="ldp-history-price"]//tbody/tr').extract()

        for row in rows:
            cols = etree.HTML(row)

            date = cols.xpath('//td[1]/text()')[0]

            print(date)