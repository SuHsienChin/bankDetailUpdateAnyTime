try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'



def convert_img(img,threshold):
    img = img.convert("L") # 處理灰度
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
                return img

def binarizing(img, threshold):
    """傳入image物件進行灰度、二值處理"""
    img = img.convert("L")  # 轉灰度
    pixdata = img.load()
    w, h = img.size
    # 遍歷所有畫素，大於閾值的爲黑色
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img

def depoint(img):
    """傳入二值化後的圖片進行降噪"""
    pixdata = img.load()
    w, h = img.size
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            count = 0
            if pixdata[x, y - 1] > 245:  # 上
                count = count + 1
            if pixdata[x, y + 1] > 245:  # 下
                count = count + 1
            if pixdata[x - 1, y] > 245:  # 左
                count = count + 1
            if pixdata[x + 1, y] > 245:  # 右
                count = count + 1
            if pixdata[x - 1, y - 1] > 245:  # 左上
                count = count + 1
            if pixdata[x - 1, y + 1] > 245:  # 左下
                count = count + 1
            if pixdata[x + 1, y - 1] > 245:  # 右上
                count = count + 1
            if pixdata[x + 1, y + 1] > 245:  # 右下
                count = count + 1
            if count > 4:
                pixdata[x, y] = 255
    return img

captcha = Image.open("graphicAuth2.png")
result = binarizing(captcha,115)
# result = depoint(result)
result.show()
authCode = pytesseract.image_to_string(result)
print(authCode)





# result = pytesseract.image_to_string(captcha)
# print(result)

