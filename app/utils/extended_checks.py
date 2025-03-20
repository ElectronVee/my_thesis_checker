from app.utils.pdf_parser import get_page_count, extract_text

def check_page_count(pdf_path, min_pages, max_pages):
    """
    检查 PDF 文件的页数是否在指定范围内。
    """
    num_pages = get_page_count(pdf_path)
    return int(min_pages) <= num_pages <= int(max_pages)

def check_first_page_content(pdf_path, must_contain):
    """
    检查 PDF 第一页是否包含指定的关键字。
    """
    import fitz
    doc = fitz.open(pdf_path)
    first_page_text = doc[0].get_text()
    return must_contain in first_page_text

# DOCX 表单完整性检查函数
