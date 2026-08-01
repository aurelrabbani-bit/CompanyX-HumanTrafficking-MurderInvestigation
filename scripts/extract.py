from stegano import lsb
secret = lsb.reveal("HiddenMessage.bmp")
print(secret)