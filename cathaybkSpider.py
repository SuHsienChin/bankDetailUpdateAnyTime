from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 使用google試算表
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
import globalVar


# 一直等待某元素可見，超時10秒
def is_visible(locator, browser, timeout=10):
    try:
        ui.WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

# 一直等待某個元素消失，默認超時10秒
def is_not_visible(locator, browser, timeout=10):
    try:
        ui.WebDriverWait(browser, timeout).until_not(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

def startCathayBank():
    print('************************************')
    print('*')
    print('* 國泰查帳明細程式 v0.03 測試版 by 禾禾禾禾')
    print('*')
    print('************************************')
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_window_size(1300, 800)
    try:
        browser.get("https://cathaybk.com.tw/MyBank")

        idInput = browser.find_element_by_id("CustID")
        idInput.send_keys("F228552023")

        userInput = browser.find_element_by_id("UserIdKeyin")
        userInput.send_keys("allen74")

        passwordInput = browser.find_element_by_id("passwordKeyin")
        passwordInput.send_keys("abad923107")

        loginBtn = browser.find_element_by_id("CUBLoginFormSubmit")
        loginBtn.click()

        is_visible('//*[@id="TD-AccBox"]',browser)

        detailLink = browser.find_element_by_xpath(
            '/html/body/div[1]/div[3]/section/div[1]/section[1]/div[2]/div/div[1]/div/div[1]/div[2]/ul[1]/div[1]/li/div/div[1]/div/a')
        detailLink.click()

        # /html/body/div[6]/div[3]/section/div[7]/section/div/div/div[1]/div/div[2]/div/table/tbody
        # is_visible('//*[@id="idddda899dd56ed8-clone"]')
        is_visible('/html/body/div[6]/div[3]/section/div[7]/section/div/div/div[1]/div/div[2]/div/table/tbody',browser)
        # 跑查詢明細並更新到試算表
        detailQueryLoop(browser)
    except:
        print("程式發生錯誤，重新執行查詢")
        globalVar.cathayBankProcessFlag = 3  # 伺服器執行錯誤，重新執行
# 跑查詢明細並更新到試算表
def detailQueryLoop(browser):
    while 1:
        try:
            globalVar.cathayBankProcessFlag = 2 # 更新中
            trueFlag = 1
            while trueFlag == 1:
                pageBody = browser.find_element_by_id('body-wrapper')
                if pageBody.get_attribute('class') != 'loading':
                    trueFlag = 0
                    time.sleep(0.5)
            is_visible('/html/body/div[6]/div[3]/section/div[7]/section/div/div/div[1]/div/div[2]/div/table/tbody',browser)
            print('資料更新中' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            # table = browser.find_element_by_id("contentTab_AcctInq_B0103")
            table = browser.find_element_by_xpath(
                '/html/body/div[6]/div[3]/section/div[7]/section/div/div/div[1]/div/div[2]/div/table/tbody')
            trs = table.find_elements_by_tag_name('tr')

            Json = 'tcbbank-322210-c9fd6710f5d3.json'  # Json 的單引號內容請改成妳剛剛下載的那個金鑰
            Url = ['https://spreadsheets.google.com/feeds']

            Connect = SAC.from_json_keyfile_name(Json, Url)
            GoogleSheets = gspread.authorize(Connect)

            Sheet = GoogleSheets.open_by_key('1kyBcJZt4l0zWDsm2CE9XYig0FmCbfsRAHjGuTYReOeU')  # 這裡請輸入妳自己的試算表代號
            Sheets = Sheet.sheet1

            Sheets.clear()

            dataTitle = ["交易日期", "提出", "存入", "餘額", "說明", "交易資訊", "備註"]
            Sheets.append_row(dataTitle)

            for i in range(0, 30):
                tds = trs[i].find_elements_by_tag_name('td')
                datas = []
                for td in tds:
                    datas.append(td.text)
                Sheets.append_row(datas)
            time.sleep(30)
            # 查詢按鈕
            browser.refresh()
        except:
            print('發生錯誤')
            globalVar.cathayBankProcessFlag = 3  # 伺服器執行錯誤，重新執行
            return



