import os
from app.utils.content_checker import extract_text_from_pdf, extract_text_from_docx
import re
import fitz  # PyMuPDF
try:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    from PIL import Image
except ImportError:
    pytesseract = None


def check_electronic_signature(file_path, keywords=["签名", "电子签"]):
    """
    检查文件中是否包含电子签名
    首先通过文本提取，若未发现且 OCR 可用，再尝试 OCR
    返回：(True, "说明") 或 (False, "说明")
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        text = extract_text_from_docx(file_path)
    for kw in keywords:
        if kw in text:
            return True, "文本中检测到电子签"
    # 若文本中未发现，尝试 OCR（假设文件是图像或已转换为图像）
    if pytesseract is not None:
        try:
            image = Image.open(file_path)
            ocr_text = pytesseract.image_to_string(image, lang='chi_sim')
            for kw in keywords:
                if kw in ocr_text:
                    return True, "OCR 识别中检测到电子签"
        except Exception:
            pass
    return False, "未检测到电子签"


def extract_signature_images_from_first_page(pdf_path, pic_path):
    """
    从 PDF 文件第一页中提取图片，并保存到 pic_path 目录中。
    返回提取的图片文件路径列表
    """
    images = []
    try:
        doc = fitz.open(pdf_path)
        first_page = doc[0]
        # 获取第一页中所有图片信息
        xref_list = []
        for img in first_page.get_images(full=True):
            xref_list.append(img[0])
        imgcount = 0
        for xref in xref_list:
            pix = fitz.Pixmap(doc, xref)
            imgcount += 1
            new_name = os.path.basename(pdf_path).replace('.pdf', '') + f"_img_first_{imgcount}.png"
            full_path = os.path.join(pic_path, new_name)
            if pix.n < 5:
                pix.save(full_path)
            else:
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.save(full_path)
                pix0 = None
            pix = None
            images.append(full_path)
    except Exception as e:
        print("提取第一页图片失败：", e)
    return images


def check_signature_in_pdf(pdf_path, expected_name, pic_path, role="teacher"):
    """
    检查PDF文件第一页中是否包含签名图片，并使用OCR识别签名中的姓名是否符合预期。
    参数：
      pdf_path: PDF文件路径
      expected_name: 预期签名的姓名（教师或学生姓名）
      pic_path: 临时保存图片的目录
      role: "teacher" 或 "student"；如果为 None，则默认设为 "签名"
    返回：
      (found, message)
    """
    # 如果 role 为 None，提供默认值
    if role is None:
        role = "签名"

    # 确保pic_path目录存在
    if not os.path.exists(pic_path):
        os.makedirs(pic_path)

    images = extract_signature_images_from_first_page(pdf_path, pic_path)
    if not images:
        return False, f"未在PDF第一页提取到任何{role}签名图片"

    for image_path in images:
        try:
            img = Image.open(image_path)
            ocr_text = pytesseract.image_to_string(img, lang='chi_sim')
            # 检查OCR识别结果中是否包含预期姓名
            if expected_name in ocr_text:
                display_role = role.capitalize() if role else "签名"
                return True, f"{display_role}签名正确：识别到 '{expected_name}'"
        except Exception as e:
            print("OCR识别出错：", e)
    return False, f"在第一页签名图片中未识别到预期的{role}姓名：{expected_name}"