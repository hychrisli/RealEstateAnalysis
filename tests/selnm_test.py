from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import time

class PropAddrUrlSelnm:
    agent = None

    PAGE_TIME_OUT = 10 # seconds
    MAX_TRY_NUM = 3

    def __init__(self):
        self.timeout = 10
        self.browser = self.__init_browser__()

    @staticmethod
    def __init_browser__():
        fp = webdriver.FirefoxProfile('/home/sparkit/Data/FirefoxProfile')
        fp.set_preference('permissions.default.image', 2)
        fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        fp.set_preference('webdriver.load.strategy', 'unstable')
        # fp.set_preference('network.cookie.cookieBehavior', 2)
        fp.set_preference('javascript.enabled', False)
        browser = webdriver.Firefox(firefox_profile=fp)
        return browser

    def run(self):
        self.__dismiss_survey__()

    def __dismiss_survey__(self):

        self.browser.get('file:///home/sparkit/Downloads/site')
        time.sleep(5)

        try:
            self.browser.find_element_by_id('acsMainInvite')
            print "\nHere comes the survey"

            try:
                self.browser.find_element_by_xpath(
                    '//div[@id="acsMainInvite"]//a[@title="No, thanks"]').click()
                print "Dismissed survey"

            except NoSuchElementException:
                print "Can't dismiss survey"

        except NoSuchElementException:
            print "\n no survey window\n"



        return self.browser.current_url


test = PropAddrUrlSelnm()
test.run()
