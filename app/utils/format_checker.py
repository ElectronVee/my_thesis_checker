import re


def check_folder_naming(folder_name, pattern):
    """
        检查文件夹名称是否符合指定正则表达式规则。

        参数：
          folder_name: 文件夹名称字符串。
          pattern: 正则表达式模式字符串（例如 "^[\u4e00-\u9fa5]+学院-[\u4e00-\u9fa5]+.*$"）。

        返回：
          True：符合规则；False：不符合规则。
        """
    return re.match(pattern, folder_name) is not None


def check_file_naming(file_name, pattern):
    """
       检查文件名称是否符合指定的正则表达式规则。
       参数：
         file_name: 文件名称字符串。
         pattern: 文件名的正则表达式模式（例如 "^1-1-[\dA-Za-z]+-[\u4e00-\u9fa5]+-论文皮\.psd$"）。
       """
    return re.match(pattern, file_name) is not None


def check_file_versions(file_list, base_name, versions_required):
    """
    检查上传文件列表中，是否存在符合 base_name 的文件版本。
    对于双版本要求，需同时存在 .docx 和 .pdf 文件。
    file_list: 上传文件列表（文件名列表）
    base_name: 文件名公共部分（不含扩展名）
    versions_required: "double" 或 "single"
    """
    if versions_required == "double":
        has_docx = any(f.startswith(base_name) and f.lower().endswith(".docx") for f in file_list)
        has_pdf = any(f.startswith(base_name) and f.lower().endswith(".pdf") for f in file_list)
        return has_docx and has_pdf
    elif versions_required == "single":
        return any(f.startswith(base_name) for f in file_list)
    return False
