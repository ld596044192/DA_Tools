from PIL import Image, ImageSequence

import os

gifPath = r'C:\Users\lida\Desktop\123.gif'

oriGif = Image.open(gifPath)

lifeTime = oriGif.info['duration']

imgList = []

imgNew = []

for i in ImageSequence.Iterator(oriGif):
    print(i.copy())

    imgList.append(i.copy())

for index, f in enumerate(imgList):
    f.save("C:\\Users\\lida\\Desktop\\gif\\%d.png" % index)

    img = Image.open("C:\\Users\\lida\\Desktop\\gif\\%d.png" % index)

    img.thumbnail((111, 101), Image.ANTIALIAS)

    imgNew.append(img)

imgNew[0].save("C:\\Users\\lida\\Desktop\\new.gif", 'gif', save_all=True, append_images=imgNew[1:], loop=0,

               duration=lifeTime)