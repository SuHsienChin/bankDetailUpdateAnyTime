from websocket_server import WebsocketServer
import json
import tcbBank
import cathaybkSpider
import threading
import globalVar

browser = object
# tcbBankProcessFlag = 0
# cathayBankProcessFlag = 0
print('************************************')
print('*')
print('* 啟動查帳websocketServer v0.01 測試版 by 禾禾禾禾')
print('*')
print('************************************')

# Called for every client connecting (after handshake)
def new_client(client, server):
    print("有一個新的連線連接 id %d" % client['id'])
    print(f'合庫狀態：' + str(globalVar.tcbBankProcessFlag))
    print(f'國泰狀態：' + str(globalVar.cathayBankProcessFlag))
    send_data(client,json.dumps(['data', {'tcbBabkstatus': str(globalVar.tcbBankProcessFlag), 'type': 'newClient'}]))
    send_data(client, json.dumps(['data', {'catBabkstatus': str(globalVar.cathayBankProcessFlag), 'type': 'catNewClient'}]))



# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 2:
        spider_controller(json.loads(message), client)
        message = message[:200] + '..'
        #print("Client(%d) said: %s" % (client['id'], message))
        # server.send_message_to_all("Client(%d) said: %s" % (client['id'], message))


def send_data(client, message):
    server.send_message(client, message)


def spider_controller(controler, client):
    global browser
    global tcbBankProcessFlag
    controler_type = controler["type"]

    if controler_type == "合庫":
        # 合庫程式開始
        browser = tcbBank.startTcbBank()
        send_data(client, json.dumps(['data', {'tcbBabkstatus': str(globalVar.tcbBankProcessFlag), 'type': 'newClient'}]))
        print(f'合庫狀態：' + str(globalVar.tcbBankProcessFlag))
        # 將合庫的驗證圖片轉成Base64二進制，傳送到前端網頁
        picBase64 = tcbBank.encodePicToBase64('authPic.png')
        picBase64 = str(picBase64)
        picBase64 = picBase64.split("'")
        picBase64 = picBase64[1]
        returnPicBase64 = json.dumps(['data', {'picBase64': picBase64, 'type': 'changePic'}])
        print('回傳圖片二制碼')
        send_data(client, returnPicBase64)

    if controler_type == "合庫驗證碼":
        print(controler["content"])
        # 使用多執行緒
        t = threading.Thread(target=tcbBank.waitInputAuthCode, args=(controler["content"], browser, server, client))
        t.start()
        # tcbBank.waitInputAuthCode(controler["content"], browser)
        print('執行多執行緒')
        print(f'合庫狀態：' + str(globalVar.tcbBankProcessFlag))
        send_data(client, json.dumps(['data', {'tcbBabkstatus': str(globalVar.tcbBankProcessFlag), 'type': 'newClient'}]))

    if controler_type == "查詢合庫運作狀態":
        send_data(client, json.dumps(['data', {'tcbBabkstatus': str(globalVar.tcbBankProcessFlag), 'type': 'newClient'}]))

    if controler_type == "國泰啟動":
        print('國泰啟動')
        catbk = threading.Thread(target = cathaybkSpider.startCathayBank)
        catbk.start()
        #cathaybkSpider.startCathayBank()
        globalVar.cathayBankProcessFlag = 2
        print('國泰狀態')
        print(globalVar.cathayBankProcessFlag)
        send_data(client, json.dumps(['data', {'catBabkstatus': str(globalVar.cathayBankProcessFlag), 'type': 'catNewClient'}]))


    if controler_type == "查詢國泰運作狀態":
        send_data(client,
                  json.dumps(['data', {'catBabkstatus': str(globalVar.cathayBankProcessFlag), 'type': 'catNewClient'}]))
    return


PORT = 9001
server = WebsocketServer(PORT,'111.251.62.96')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
