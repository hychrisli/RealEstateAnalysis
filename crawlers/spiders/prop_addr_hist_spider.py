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
            # print(str(prop_addr_id) + ':' + url)
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta={'prop_addr_id': prop_addr_id,
                                       'url': url,
                                       'dont_redirect': True,
                                       'handle_httpstatus_list': [302]
                                       },
                                 headers={'referer': 'www.google.com'})

    def parse(self, response):
        prop_addr_id = response.meta['prop_addr_id']
        latest_price = self.cnx.get_latest_price(prop_addr_id)

        event = response.xpath('//div[1][@class="span4"]/p[2]/span/text()').extract_first()
        price = response.xpath('//h2[@id="propertyAddress"]/text()[normalize-space()]').extract_first()

        if (event is None) or (price is None):
            print (str(prop_addr_id) + ' | page not found: ' + response.meta['url'])
            self.cnx.add_rmv_addr_id(prop_addr_id)
        else:
            hist_event = PropAddrHistEvent()
            hist_event.prop_addr_id = prop_addr_id
            hist_event.set_event(event)
            hist_event.set_price(price)

            if (hist_event.event == 'Sold') or (hist_event.price != latest_price) :
                self.cnx.add_prop_addr_hist_event(hist_event)

            print(hist_event.to_string())

        self.cnx.mark_is_updated(prop_addr_id)

    def close(self, reason):
        self.cnx.close()
