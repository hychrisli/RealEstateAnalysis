from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from etl.dao.prop_addr_dao import PropAddrDao


class PropAddrUrlSelnm:

    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)
        self.timeout = 10
        self.prop_cnx = PropAddrDao()

    def __get_addrs__(self):
        addr_lst = []
        rows = self.prop_cnx.get_addrs()
        for (mls_id, addr, city, state) in rows:
            addr_lst.append((mls_id, addr + ", " + city + ", " + state))
        return addr_lst

    def upd_urls(self):
        addr_lst = self.__get_addrs__()
        url_lst = []
        for (mls_id, addr) in  addr_lst:
            url = self.__find_url__(addr)
            url_lst.append((mls_id, url))
            print (url)
        self.browser.quit()
        self.prop_cnx.upd_urls(url_lst)

    def __find_url__(self, addr):
        self.browser.get("http://www.realtor.com/")
        text_box = self.browser.find_element_by_xpath('//input[@id="searchBox"]')  # input selector
        text_box.send_keys(addr)  # enter text in input

        self.browser.find_element_by_xpath('//button[@class="btn btn-primary js-searchButton"]').click()
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, "ldp-header-price"))
            WebDriverWait(self.browser, self.timeout).until(element_present)
        except TimeoutException:
            print "Timed out waiting for page to load"

        return self.browser.current_url

