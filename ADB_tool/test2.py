
from PIL import Image


img = r'C:\Users\lida\Desktop\ADB工具-Linux截图（DA）\2.png'

img = Image.open(img)

img1 = img.rotate(90, expand=1)

img1.show()
