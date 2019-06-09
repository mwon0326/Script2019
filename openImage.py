from tkinter import*
from io import BytesIO
import urllib
import urllib.request
from PIL import Image,ImageTk
import json

def openImage(name):
    data = open("image.json", "r", encoding='UTF8').read()
    url_list = json.loads(data)

    url = url_list[name]

    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    im = Image.open(BytesIO(raw_data))
    return im