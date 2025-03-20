import re
import fitz
from datetime import datetime, timedelta


def check_date_format(date_str):
    """检查日期格式是否符合 YYYY-MM-DD 格式"""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return re.match(pattern, date_str) is not None


def check_date_sequence(date_str1, date_str2):
    """检查 date_str1 是否早于或等于 date_str2"""
    fmt = "%Y-%m-%d"
    try:
        d1 = datetime.strptime(date_str1, fmt)
        d2 = datetime.strptime(date_str2, fmt)
        return d1 <= d2
    except Exception:
        return False


def extract_signing_date_from_pdf(pdf_path):
    """
    从PDF文件的最后一页中提取签字日期（假设格式为 YYYY-MM-DD）
    """
    try:
        doc = fitz.open(pdf_path)
        last_page = doc[-1]
        text = last_page.get_text()
        # 匹配日期格式，假设日期格式为 YYYY-MM-DD
        match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
        if match:
            return match.group(1)
    except Exception as e:
        print("读取PDF文件失败:", e)
    return None


def check_teacher_sign_date(teacher_sign_date_str, defense_date_str):
    """
    检查教师签字日期是否至少比答辩日期提前7天
    """
    try:
        fmt = "%Y-%m-%d"
        teacher_date = datetime.strptime(teacher_sign_date_str, fmt)
        defense_date = datetime.strptime(defense_date_str, fmt)
        return teacher_date <= defense_date - timedelta(days=7)
    except Exception as e:
        print("日期比较错误:", e)
    return False