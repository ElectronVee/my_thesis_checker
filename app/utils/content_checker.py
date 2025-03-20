import os
import fitz
from docx import Document

def extract_text_from_pdf(pdf_path):
    """提取 PDF 文件的文本"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return ""

def extract_text_from_docx(docx_path):
    """提取 DOCX 文件的文本"""
    try:
        doc = Document(docx_path)
        return "\n".join(para.text for para in doc.paragraphs)
    except Exception as e:
        return ""

def check_file_content_keywords(file_path, keywords):
    """
    检查文件内容中是否包含所有指定的关键字
    参数：
      file_path: 文件路径
      keywords: 关键字列表
    返回：
      (True, "说明") 或 (False, "缺少关键字 xxx")
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        text = extract_text_from_docx(file_path)
    for kw in keywords:
        if kw not in text:
            return False, f"缺少关键字：{kw}"
    return True, "内容符合要求"
