# pdf解析
import fitz

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def get_page_count(pdf_path):
    doc = fitz.open(pdf_path)
    return len(doc)

