from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from etl.dao.prop_addr_dao import PropAddrDao
from utility.actions import show_progress, rand_wait
from utility.constants import user_agents
from utility.calculate import rand_non_repeat_agent, rand_batch_end_num

import sys


class PropAddrUrlSelnm:
    agent = None

    PAGE_TIME_OUT = 10 # seconds
    MAX_TRY_NUM = 3

    def __init__(self):
        self.timeout = 10
        self.browser = None
        self.prop_cnx = PropAddrDao()

    @staticmethod
    def __init_browser__():
        fp = webdriver.FirefoxProfile('/home/sparkit/Data/FirefoxProfile')
        fp.set_preference('permissions.default.image', 2)
        fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        fp.set_preference('webdriver.load.strategy', 'unstable')
        # fp.set_preference('network.cookie.cookieBehavior', 2)
        fp.set_preference('javascript.enabled', False)
        fp.set_preference("general.useragent.override", PropAddrUrlSelnm.__gen_user_agent__())
        browser = webdriver.Firefox(firefox_profile=fp)
        browser.implicitly_wait(5)
        return browser

    def __get_addrs__(self):
        addr_lst = []
        rows = self.prop_cnx.get_addrs()
        for (mls_id, addr, city, state) in rows:
            addr_lst.append((mls_id, addr + ", " + city + ", " + state))
        return addr_lst

    def upd_urls(self):
        addr_lst = self.__get_addrs__()
        tot_num = len(addr_lst)
        batch_start_num = 0

        # Loop through batches
        while tot_num > batch_start_num:
            self.browser = self.__init_browser__()
            batch_end_num = rand_batch_end_num(batch_start_num, tot_num)
            self.__upd_url_batch__(addr_lst[batch_start_num:batch_end_num])
            self.browser.quit()

            rand_wait("Batch completed")
            show_progress(batch_end_num, tot_num, 1, '\n')
            batch_start_num = batch_end_num

    def __upd_url_batch__(self, batch):
        url_lst = []
        for (mls_id, addr) in batch:
            url = self.__find_url__(addr)
            url_lst.append((mls_id, url))
            print (url)
            rand_wait(str(mls_id) + " done")

        self.prop_cnx.upd_urls(url_lst)

    def __find_url__(self, addr):
        # self.browser.delete_all_cookies()
        num_try = 0

        while True:
            self.browser.get("https://www.realtor.com")
            num_try += 1
            try:
                element_present = EC.presence_of_element_located((By.ID, "searchBox"))
                WebDriverWait(self.browser, self.timeout).until(element_present)
                break
            except TimeoutException:
                if num_try < PropAddrUrlSelnm.MAX_TRY_NUM:
                    self.browser.get("https://www.google.com")
                    print ("Home page not available. Will refresh and try it again")
                    rand_wait("Wait to try again....")
                else:
                    print ("Can't load home page")
                    sys.exit(1)

        text_box = self.browser.find_element_by_xpath('//input[@id="searchBox"]')

        text_box.clear()
        text_box.send_keys(addr)  # enter text in input

        rand_wait("Home page loaded")

        self.browser.find_element_by_xpath('//button[@class="btn btn-primary js-searchButton"]').click()
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, "ldp-header-price"))
            WebDriverWait(self.browser, self.timeout).until(element_present)
        except TimeoutException:
            print "Timed out waiting for page to load"
            return "Not Available"

        rand_wait("Pretend Browsing", 5, 10)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

        try:
            alert = self.browser.switch_to.alert
            alert.dismiss()
            print "\nI need no survey\n"
        except NoAlertPresentException:
            pass

        return self.browser.current_url

    @staticmethod
    def __gen_user_agent__():
        PropAddrUrlSelnm.agent = rand_non_repeat_agent(PropAddrUrlSelnm.agent)
        print("User agent: " + str(PropAddrUrlSelnm.agent))
        return user_agents[PropAddrUrlSelnm.agent]
