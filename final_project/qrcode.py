import pyzbar.pyzbar as pyzbar
from PIL import Image,ImageEnhance
import cv2
import sys
import os

file_path = "/home/cayu/Desktop"
image = "fuck.jpg"
file_name = "text.txt"
while True:
    if image in os.listdir(file_path):
        try:
            img = Image.open(file_path+"/"+image)

            barcodes = pyzbar.decode(img)
        except:
            pass
        if len(barcodes)!=0:
            print barcodes
            img.show()
            for barcode in barcodes:
                # print("fuck")
                barcodeData = barcode.data.decode("utf-8")
                print(barcodeData)
                with open(file_path+"/"+file_name, 'w') as file:
                    file.write(barcodeData)
            break