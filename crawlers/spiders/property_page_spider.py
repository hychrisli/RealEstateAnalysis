import scrapy
import re
from etl.dao.mls_type_dao import MlsTypeDao
from utility.display import show_progress


class PropertyPageSpider(scrapy.Spider):
    name = 'property_page'

    def __init__(self):
        super(PropertyPageSpider, self).__init__()
        self.cnx = MlsTypeDao()
        self.num_urls = 0
        self.num_done_urls = 0

    def start_requests(self):
        urls = self.cnx.get_mls_url_incr()
        self.num_urls = len(urls)
        for (mls_id, url) in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'mls_id': mls_id})

    def parse(self, response):
        mls_id = response.meta['mls_id']
        # mls_id = response.xpath('//div[1][@class="span4"]/p[1]/span/text()').extract_first()
        type_year = response.xpath('//div[1][@class="span4"]/p[3]/span/text()').extract_first()
        prop_type = re.sub('\([^)]+\)', '', str(type_year)).strip()
        # print (mls_id, prop_type)
        self.cnx.update_prop_incr_with_type(mls_id, prop_type)
        self.num_done_urls += 1
        show_progress(self.num_done_urls, self.num_urls, 25, "processing " + str(mls_id))
