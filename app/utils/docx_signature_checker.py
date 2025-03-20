import zipfile
import os
import tempfile
import pytesseract
from PIL import Image
from OCR_test import OCR_lmj
import re
import matplotlib.pyplot as plt


def extract_images_from_docx(docx_path):
    """
    从 DOCX 文件中提取所有嵌入的图像文件，并返回图像文件的临时存放路径列表。
    DOCX 文件实际上是一个ZIP文件，其中图片存放在 "word/media" 目录下。
    """
    image_files = []
    try:
        with zipfile.ZipFile(docx_path, 'r') as z:
            for file in z.namelist():
                if file.startswith("word/media/"):
                    # 创建一个临时目录来存放提取的图像
                    temp_dir = tempfile.mkdtemp()
                    z.extract(file, temp_dir)
                    image_files.append(os.path.join(temp_dir, file))
    except Exception as e:
        print("提取 DOCX 图像失败:", e)
    return image_files


# def ocr_image(image_path):
#     """
#     对指定图像文件进行 OCR 识别，返回识别出的文本。
#     使用 pytesseract。
#     """
#     try:
#         image = Image.open(image_path)
#         print(f"OCR识别图像 {image_path}")
#         # 转换为灰度图
#         image = image.convert('L')
#         # 应用二值化处理：设置阈值为 150
#         image = image.point(lambda x: 0 if x < 150 else 255, '1')
#         image = image.filter(ImageFilter.MedianFilter())
#         text = pytesseract.image_to_string(image, lang='chi_sim+eng')
#         if text:
#             print("识别成功，输出内容：")
#             print(text)
#         else:
#             print("识别成功，但未检测到文本。")
#         return text
#     except Exception as e:
#         print(f"OCR识别图像 {image_path} 失败: {e}")
#         return ""


def check_signature_in_docx(docx_path, expected_names):
    """
    检查 DOCX 文件中是否存在手写签名，并验证签名中的名字是否正确。
    签名图像假设在文档第一页中嵌入，但由于位置不固定，这里只提取所有图像进行 OCR，
    并判断 OCR 结果中是否包含预期的名字。

    参数：
      docx_path: DOCX 文件路径。
      expected_names: 预期出现的姓名列表

    返回：
      tuple: (found_signature, recognized_text, matched_name)
             found_signature: True 如果找到了签名且匹配预期名字，否则 False
             recognized_text: OCR 识别出的文本（可能包含多个结果）
             matched_name: 如果匹配到预期名字，返回该名字；否则为 None
    """
    images = extract_images_from_docx(docx_path)
    all_recognized_texts = []
    for image_file in images:
        # recognized_text = OCR_lmj(image_file).strip().replace(" ", "").upper()
        recognized_text = re.sub(r'\s+', '', OCR_lmj(image_file)).upper()
        if len(recognized_text) < 1:
            continue
        all_recognized_texts.append(recognized_text)

        for name in expected_names:
            clean_name = name.strip().replace(" ", "").upper()
            if clean_name == recognized_text:
                return True, recognized_text, name

    # 如果没有完全匹配，则返回所有识别结果供参考
    return False, "; ".join(all_recognized_texts), None


# test
if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    docx_file = r"D:\pythonProject\test\Doc1.docx"
    expected_names = ["123","你好"]

    found, text, matched = check_signature_in_docx(docx_file, expected_names)
    img_files = extract_images_from_docx(docx_file)

    if img_files:
        # 打开第一张提取到的图像
        img = Image.open(img_files[0])
        plt.imshow(img)
        plt.axis('off')
        plt.title("提取到的图像")
        plt.show()
    else:
        print("未提取到图像。")

    if found:
        print("找到签名！")
        print("OCR识别文本：", text)
        print("匹配到预期姓名：", matched)
    else:
        print("未能检测到有效签名。")
        print("OCR识别到的文本（供参考）：", text if text else "无任何文本识别结果")

