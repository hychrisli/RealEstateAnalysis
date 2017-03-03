import scrapy
import time

from lxml import etree
from random import randint

from etl.entities.prop_addr_hist_event import PropAddrHistEvent
from etl.dao.prop_addr_hist_dao import PropAddrHistDao
from utility.display import show_progress


class PropAddrHistSpider(scrapy.Spider):
    name = "prop_addr_hist"

    def __init__(self):
        super(PropAddrHistSpider, self).__init__()
        self.cnx = PropAddrHistDao()
        # self.cnx.init_cleanup()
        self.num_urls = 0
        self.num_done_urls = 0

    def start_requests(self):
        urls = self.cnx.select_urls()
        self.num_urls = len(urls)

        for (prop_addr_id, url) in urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta={'prop_addr_id': prop_addr_id},
                                 headers={'referer': 'www.google.com'})

    def parse(self, response):
        # print(response.request.headers)
        rows = response.xpath('//div[@id="ldp-history-price"]//tbody/tr').extract()
        prop_addr_id = response.meta['prop_addr_id']
        self.num_done_urls += 1

        for row in rows:
            cols = etree.HTML(row)
            hist_event = PropAddrHistEvent()
            hist_event.prop_addr_id = prop_addr_id
            hist_event.set_date(cols.xpath('//td[1]/text()')[0])
            hist_event.event = cols.xpath('//td[2]/text()')[0]
            hist_event.set_price(cols.xpath('//td[3]/text()')[0])
            hist_event.set_price_sqft(cols.xpath('//td[4]/text()')[0])

            self.cnx.add_prop_addr_hist_event(hist_event)

        self.cnx.mark_is_updated(prop_addr_id)

        show_progress(self.num_done_urls, self.num_urls, 1, "processing " + str(prop_addr_id))

    def close(self, reason):
        self.cnx.close()