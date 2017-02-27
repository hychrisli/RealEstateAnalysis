import scrapy
from lxml import etree

from etl.entities.prop_addr_hist import PropAddrHist
from etl.dao.prop_addr_hist_dao import PropAddrHistDao


class PropHistSpider(scrapy.Spider):
    name = "prop_hist"

    def __init__(self):
        super(PropHistSpider, self).__init__()
        self.cnx = PropAddrHistDao()
        self.cnx.init_cleanup()

    def start_requests(self):
        url = "http://www.realtor.com/realestateandhomes-detail/490-S-Bayview-Ave_Sunnyvale_CA_94086_M27263-77808"
        prop_addr_id = 1
        yield scrapy.Request(url=url, callback=self.parse, meta={'prop_addr_id': prop_addr_id})

    def parse(self, response):
        rows = response.xpath('//div[@id="ldp-history-price"]//tbody/tr').extract()
        prop_addr_id = response.meta['prop_addr_id']
        prop_hist_lst = []

        for row in rows:
            cols = etree.HTML(row)
            prop_hist = PropAddrHist()
            prop_hist.prop_addr_id = prop_addr_id
            prop_hist.set_date(cols.xpath('//td[1]/text()')[0])
            prop_hist.event = cols.xpath('//td[2]/text()')[0]
            prop_hist.set_price(cols.xpath('//td[3]/text()')[0])
            prop_hist.set_price_sqft(cols.xpath('//td[4]/text()')[0])

            prop_hist.print_hist()

            self.cnx.add_prop_addr_hist(prop_hist)

            prop_hist_lst.append(prop_hist)
