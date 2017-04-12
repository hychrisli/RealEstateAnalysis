#!/bin/python
import json
import logging
import scrapy
from scrapy_splash import SplashRequest

from etl.dao.mls_prop_dao import MlsPropDao
from etl.dao.zipcode_dao import ZipcodeDao
from etl.entities.real_property import RealProperty

logger = logging.getLogger('REA.MLS.API_SEARCH')


class ApiSearchSpider(scrapy.Spider):
    name = 'api_search'

    def __init__(self):
        super(ApiSearchSpider, self).__init__()
        self.connector = MlsPropDao()
        self.connector.init_cleanup()

    def start_requests(self):
        url = 'http://api.mlslistings.com/api/widgetsearch'
        header = ApiSearchSpider.__gen_header__()
        # zipcodes = ['93907', '93901', '93908']

        zip_cnx = ZipcodeDao()
        zipcodes = zip_cnx.get_zipcode_lst()
        zip_cnx.close()

        for (zipcode,) in zipcodes:
            post_json = ApiSearchSpider.__gen_post_json__(zipcode)
            # logger.info("Processing " + zipcode)
            yield SplashRequest(url, self.parse,
                                headers=header,
                                args={'wait': 1,
                                      'http_method': 'POST',
                                      'body': post_json},
                                meta={'zipcode': zipcode})

    def parse(self, response):
        zipcode = response.meta['zipcode']
        logger.info("Processing " + zipcode)
        body = response.body
        html_selectors_before = '<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">'
        html_selectors_after = '</pre></body></html>'
        res_str = body.replace(html_selectors_before, '').replace(html_selectors_after, '')
        res_json = json.loads(res_str)
        res_lst = res_json['propertySearchResults']
        property_lst = []

        if not res_lst:
            return

        for item in res_lst:
            prop = RealProperty(item)
            # prop.print_details()
            property_lst.append(prop)

        self.connector.add_properties(property_lst)

    @staticmethod
    def __gen_header__():
        return {'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Content-Length': '166',
                'Content-Type': 'application/json;charset=utf-8',
                'Host': 'api.mlslistings.com',
                'Referer': 'http://api.mlslistings.com/',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
                'X-Requested-With': 'XMLHttpRequest'}

    @staticmethod
    def __gen_post_json__(zipcode):
        return '{"display":{"pageNumber":1,"itemsPerPage":400},"cityName":"",' \
               '"countyName":"","zipCode":"' + zipcode + '","mlsNumber":"","address":"",' \
               '"beds":"","baths":"","listSalePrice":""}'
