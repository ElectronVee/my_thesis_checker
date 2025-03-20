import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
image = Image.open('D:\\2.jpeg')
content = pytesseract.image_to_string(image)
print(content)

# SUCCESS! :)
