from websocket_server import WebsocketServer
import json
import tcbBank



# Called for every client connecting (after handshake)
def new_client(client, server):
    print("有一個新的連線連接 id %d" % client['id'])
    # server.send_message_to_all("Hey all, a new client has joined us")


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
    controler_type = controler["type"]
    if controler_type == "合庫":
        # 合庫程式開始
        browser = tcbBank.startTcbBank()

        # 將合庫的驗證圖片轉成Base64二進制，傳送到前端網頁
        picBase64 = tcbBank.encodePicToBase64('authPic.png')
        picBase64 = str(picBase64)
        picBase64 = picBase64.split("'")
        picBase64 = picBase64[1]
        returnPicBase64 = json.dumps(['data', {'picBase64': picBase64, 'type': 'changePic'}])
        print('回傳圖片二制碼')
        send_data(client, returnPicBase64)

        # if controler_type == "合庫驗證碼":
        #     print(controler["content"])
        #
        # tcbBank.waitInputAuthCode(controler["content"], browser)


    if controler_type == "國泰":
        print('國泰')
    return


PORT = 9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
