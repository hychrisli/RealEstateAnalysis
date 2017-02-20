import scrapy
from lxml import etree
from entities.prop_hist import PropHist


class PropHistSpider(scrapy.Spider):
    name = "prop_hist"

    def start_requests(self):
        url = "http://www.realtor.com/realestateandhomes-detail/490-S-Bayview-Ave_Sunnyvale_CA_94086_M27263-77808"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        rows = response.xpath('//div[@id="ldp-history-price"]//tbody/tr').extract()
        prop_hist_lst = []

        for row in rows:
            cols = etree.HTML(row)
            prop_hist = PropHist()
            prop_hist.date = cols.xpath('//td[1]/text()')[0]
            prop_hist.event = cols.xpath('//td[2]/text()')[0]
            prop_hist.set_price(cols.xpath('//td[3]/text()')[0])
            prop_hist.set_price_sqft(cols.xpath('//td[4]/text()')[0])

            prop_hist.print_hist()
            prop_hist_lst.append(prop_hist)
