import scrapy
from scrapy.selector import Selector

from lxml import etree
from random import randint

from etl.entities.prop_addr_hist_event import PropAddrHistEvent
from etl.dao.prop_addr_hist_dao import PropAddrHistDao
from utility.actions import show_progress,except_response


class PropAddrHistSpider(scrapy.Spider):
    name = "prop_addr_hist"

    def __init__(self, batch_size):
        super(PropAddrHistSpider, self).__init__()
        self.cnx = PropAddrHistDao()
        self.batch_size = batch_size

    def start_requests(self):
        urls = self.cnx.select_url_batch(self.batch_size)

        for (prop_addr_id, url) in urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta={'prop_addr_id': prop_addr_id},
                                 headers={'referer': 'www.google.com'})

    def parse(self, response):
        input_tag = Selector(response).xpath("//input").extract_first()
        if not input_tag:
            except_response("No Input found in page. User may be locked")

        rows = response.xpath('//div[@id="ldp-history-price"]//tbody/tr').extract()
        prop_addr_id = response.meta['prop_addr_id']
        latest_date = self.cnx.get_latest_date(prop_addr_id)
        print ("processing " + str(prop_addr_id))

        for row in rows:
            cols = etree.HTML(row)
            hist_event = PropAddrHistEvent()
            hist_event.prop_addr_id = prop_addr_id
            # print(cols.xpath('//td/text()'))
            hist_event.set_date(cols.xpath('//td[1]/text()')[0])
            hist_event.event = cols.xpath('//td[2]/text()')[0]
            hist_event.set_price(cols.xpath('//td[3]/text()')[0])
            hist_event.set_price_sqft(cols.xpath('//td[4]/text()')[0])
            if latest_date is not None and hist_event.event_date < latest_date:
                break
            self.cnx.add_prop_addr_hist_event(hist_event)

        self.cnx.mark_is_updated(prop_addr_id)

    def close(self, reason):
        self.cnx.close()
