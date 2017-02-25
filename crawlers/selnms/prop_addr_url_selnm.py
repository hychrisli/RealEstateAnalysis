from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from etl.dao.prop_addr_dao import PropAddrDao
from utility.display import show_progress
import time
from random import randint

class PropAddrUrlSelnm:

    def __init__(self):
        self.browser = self.__init_browser__()
        self.timeout = 10
        self.prop_cnx = PropAddrDao()

    @staticmethod
    def __init_browser__():
        # fp = webdriver.FirefoxProfile('/home/sparkit/Data/FirefoxProfile')
        # fp.set_preference('permissions.default.image', 2)
        # fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        # fp.set_preference('webdriver.load.strategy', 'unstable')
        # fp.set_preference('javascript.enabled', False)
        # browser = webdriver.Firefox(firefox_profile=fp)
        browser = webdriver.PhantomJS()
        browser.implicitly_wait(1)
        return browser

    def __get_addrs__(self):
        addr_lst = []
        rows = self.prop_cnx.get_addrs()
        for (mls_id, addr, city, state) in rows:
            addr_lst.append((mls_id, addr + ", " + city + ", " + state))
        return addr_lst

    def upd_urls(self):
        addr_lst = self.__get_addrs__()
        url_lst = []

        tot_num = len(addr_lst)
        cur_num = 0
        intvl = 25

        for (mls_id, addr) in addr_lst:
            url = self.__find_url__(addr)
            url_lst.append((mls_id, url))
            print (url)

            cur_num += 1
            upd_flag = show_progress(cur_num, tot_num, intvl, "\n\n\n")

            wait_time = randint(15, 40)
            print ("No." + str(cur_num) + " waiting... " + str(wait_time) + "s")
            time.sleep(wait_time)

            if upd_flag:
                self.prop_cnx.upd_urls(url_lst)
                url_lst = []
                self.browser.quit()
                self.browser = self.__init_browser__()

        self.browser.quit()

    def __find_url__(self, addr):
        self.browser.delete_all_cookies()
        self.browser.get("http://www.realtor.com/")
        text_box = self.browser.find_element_by_xpath('//input[@id="searchBox"]')  # input selector
        text_box.clear()
        text_box.send_keys(addr)  # enter text in input
        wait_time = randint(15, 30)
        print ("Home page waiting ... " + str(wait_time) + "s")
        time.sleep(wait_time)
        self.browser.find_element_by_xpath('//button[@class="btn btn-primary js-searchButton"]').click()
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, "ldp-header-price"))
            WebDriverWait(self.browser, self.timeout).until(element_present)
        except TimeoutException:
            print "Timed out waiting for page to load"
            return "Not Available"

        return self.browser.current_url

