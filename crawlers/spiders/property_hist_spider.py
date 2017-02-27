import scrapy
from lxml import etree

from etl.entities.prop_addr_hist_event import PropAddrHistEvent
from etl.dao.prop_addr_hist_dao import PropAddrHistDao


class PropHistSpider(scrapy.Spider):
    name = "prop_hist"

    def __init__(self):
        super(PropHistSpider, self).__init__()
        self.cnx = PropAddrHistDao()
        self.cnx.init_cleanup()

    def start_requests(self):
        urls = self.cnx.select_urls()
        for (prop_addr_id, url) in urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta={'prop_addr_id': prop_addr_id})

    def parse(self, response):
        rows = response.xpath('//div[@id="ldp-history-price"]//tbody/tr').extract()
        prop_addr_id = response.meta['prop_addr_id']
        prop_addr_hist = []

        for row in rows:
            cols = etree.HTML(row)
            hist_event = PropAddrHistEvent()
            hist_event.prop_addr_id = prop_addr_id
            hist_event.set_date(cols.xpath('//td[1]/text()')[0])
            hist_event.event = cols.xpath('//td[2]/text()')[0]
            hist_event.set_price(cols.xpath('//td[3]/text()')[0])
            hist_event.set_price_sqft(cols.xpath('//td[4]/text()')[0])

            hist_event.print_hist()
            prop_addr_hist.append(hist_event)

        self.cnx.add_prop_addr_hist(prop_addr_hist)
