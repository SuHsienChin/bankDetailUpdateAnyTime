from selenium import webdriver
from selenium.webdriver.chrome.options import Options

try:
    from PIL import Image
except ImportError:
    import Image

import base64
import time

# 使用google試算表
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

import globalVar
import json

# from PIL import Image

def startTcbBank():
    try:
        globalVar.tcbBankProcessFlag = 1 # 啟動中
        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        browser = webdriver.Chrome(options=chrome_options)
        print('************************************')
        print('*')
        print('* 合庫查帳明細程式 v0.01 測試版 by 禾禾禾禾')
        print('*')
        print('************************************')

        browser.get("https://cobank.tcb-bank.com.tw/TCB.TWNB.IDV.WEB/")

        link = browser.find_elements_by_class_name("squre_btn")
        link[0].click()

        browser.switch_to.window(browser.window_handles[1])

        browser.switch_to.frame("iframe")

        idInput = browser.find_element_by_name("viewFragment1:form1:shadedCustomerId")
        idInput.send_keys("90792003")

        userIdInput = browser.find_element_by_id("viewFragment1:form1:userId")
        userIdInput.send_keys("abpay1")

        passwordInput = browser.find_element_by_id("viewFragment1:form1:clearPassword")
        passwordInput.send_keys("qazwsx147")

        browser.find_element_by_xpath(".//*[@id='viewFragment1:form1:selectQuick']/option[3]").click()

        # 取得圖型驗證的圖，並顯示出來
        browser.save_screenshot('authPic.png')
        authPic = browser.find_element_by_id("viewFragment1:form1:graphicImg")
        authPicLeft = authPic.location['x']
        authPicRight = authPic.location['x'] + authPic.size['width']
        authPicTop = authPic.location['y']
        authPicBottom = authPic.location['y'] + authPic.size['height'] + 25

        img = Image.open('authPic.png')
        img = img.crop((authPicLeft, authPicRight, authPicTop, authPicBottom))
        img.save('authPic.png')
        return browser
    except:
        globalVar.tcbBankProcessFlag = 3  # 伺服器執行錯誤，重新執行
        return


def encodePicToBase64(picName):
    base64_data = ''
    with open("authPic.png", "rb") as f:
        # b64encode是编码，b64decode是解码
        base64_data = base64.b64encode(f.read())
    return base64_data


def waitInputAuthCode(authCode, browser, server, client):
    # input(authCode)
    # authCode = input("輸入圖型驗證碼：")
    try:
        globalVar.tcbBankProcessFlag = 2  # 正在更新資料
        authInput = browser.find_element_by_id('viewFragment1:form1:gCode')
        authInput.send_keys(authCode)

        time.sleep(1)

        loginLink = browser.find_element_by_id("viewFragment1:form1:btnLogin")
        loginLink.click()

        time.sleep(15)

        while 1:
            print('資料更新中' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            # server.send_message(client, json.dumps(['data', {'tcbBabkstatus': '2', 'type':'newClient'}]))
            detailQueryBtn = browser.find_element_by_id("viewFragment1:form1:btnQuery")
            detailQueryBtn.click()
            time.sleep(5)

            table = browser.find_element_by_xpath("//*[@id='viewFragment1:form1:result']")
            trs = table.find_elements_by_tag_name('tr')

            # -------
            # 以下是連到google試算表，把資料寫入
            #
            # -------

            Json = "synthetic-hall-226120-a48b5e640b39.json"  # Json 的單引號內容請改成妳剛剛下載的那個金鑰
            Url = ['https://spreadsheets.google.com/feeds']

            Connect = SAC.from_json_keyfile_name(Json, Url)
            GoogleSheets = gspread.authorize(Connect)

            Sheet = GoogleSheets.open_by_key('1YrXFibvZs-wS4DX0IGqTtSNnn7VQudLZgeE9dRt1Gaw')  # 這裡請輸入妳自己的試算表代號
            Sheets = Sheet.sheet1

            Sheets.clear()

            dataTitle = ["序號", "交易日期", "交易行庫", "提款金額", "存款金額", "餘額", "支票號碼"]
            Sheets.append_row(dataTitle)

            for i in range(1, 30):
                tds = trs[i].find_elements_by_tag_name('td')
                datas = []
                for td in tds:
                    datas.append(td.text)
                Sheets.append_row(datas)
            time.sleep(30)
    except:
        globalVar.tcbBankProcessFlag = 3  # 伺服器執行錯誤，重新執行
        # server.send_message(client, json.dumps(['data', {'tcbBabkstatus': '3', 'type': 'newClient'}]))
        return globalVar.tcbBankProcessFlag
