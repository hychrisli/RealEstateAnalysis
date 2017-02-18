from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


browser = webdriver.Firefox()
browser.implicitly_wait(2)
browser.get("http://www.realtor.com/")
timeout = 5

text_box = browser.find_element_by_xpath('//input[@id="searchBox"]')  # input selector
text_box.send_keys('144 W California, Sunnyvale, CA')  # enter text in input

browser.find_element_by_xpath('//button[@class="btn btn-primary js-searchButton"]').click()
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, "ldp-header-price"))
    WebDriverWait(browser, timeout).until(element_present)
except TimeoutException:
    print "Timed out waiting for page to load"

print(browser.current_url)
browser.get("http://www.realtor.com/")
