import qrcode

data = "https://nettavisen.no" #http://www.google.com/
img = qrcode.make(data)
img.save("QRcode.png")

