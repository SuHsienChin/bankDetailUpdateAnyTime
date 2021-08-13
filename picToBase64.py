import base64
import tkinter
from tkinter import messagebox

with open("123.png","rb") as f:
    # b64encode是编码，b64decode是解码
    base64_data = base64.b64encode(f.read())
    # base64.b64decode(base64data)

    messagebox.showinfo(base64_data)