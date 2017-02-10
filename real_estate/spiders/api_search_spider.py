import scrapy
import json
from scrapy_splash import SplashRequest


class ApiSearchSpider(scrapy.Spider):
    name = 'api_search'

    def start_requests(self):
        url = 'http://api.mlslistings.com/api/widgetsearch'
        post_json = '{"display":{"pageNumber":1,"itemsPerPage":200},"cityName":"",' \
                    '"countyName":"","zipCode":"94086","mlsNumber":"","address":"",' \
                    '"beds":"","baths":"","listSalePrice":""}'
        header = {'Accept': 'application/json, text/plain, */*',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'en-US,en;q=0.5',
                  'Connection': 'keep-alive',
                  'Content-Length': '166',
                  'Content-Type': 'application/json;charset=utf-8',
                  'Host': 'api.mlslistings.com',
                  'Referer': 'http://api.mlslistings.com/',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
                  'X-Requested-With': 'XMLHttpRequest'}

        yield SplashRequest(url, self.parse,
                            headers=header,
                            args={'wait': 0.5,
                                  'http_method': 'POST',
                                  'body': post_json})

    def parse(self, response):
        body = response.body
        html_selectors_before = '<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">'
        html_selectors_after = '</pre></body></html>'
        res_str = body.replace(html_selectors_before, '').replace(html_selectors_after, '')
        res_json = json.loads(res_str)
        res_lst = res_json['propertySearchResults']

        for item in res_lst:
            print (item['MLSNumber'] + ' : ' + item['filteredAddress'])
