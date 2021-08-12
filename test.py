from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
browser = webdriver.Chrome(options=chrome_options)
browser.set_window_size(1300, 800)
import time

# 使用google試算表
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui


browser.get("http://localhost:63342/tcbBankSpider/table.html?_ijt=ml69dcu0ovistrf5ss5p3r5rus")
# print(browser.page_source)

pageBody = browser.find_element_by_id('body-wrapper')

#print(pageBody.text)
print(pageBody.get_attribute('class'))
browser.close()