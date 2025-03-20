
"""
本模块根据上传的文件夹名称、文件列表、解析的 XML 规则以及各检查模块返回的结果，
生成一个格式检查报告。报告中包含：
  - 详细的检查结果数据（各项检查结果）
  - 通过的检查项列表
  - 未通过的检查项列表及提示信息
"""


def generate_report(folder_name, saved_files, rules, check_results):
    """
    生成格式检查报告。

    参数：
      folder_name (str): 用户上传的文件夹名称。
      saved_files (list): 上传文件夹中的所有文件名列表。
      rules (dict): 由 XML 规则解析模块返回的规则字典。
      check_results (dict): 各检查模块返回的结果字典，
          例如包含 "folder_naming"、"StudentMaterials"、"ReviewGroupMaterials"、"DateRules" 等项。

    返回：
      dict: 综合报告，包含详细检查结果，以及通过和未通过项列表。
    """
    report = {}
    pass_items = []
    fail_items = []

    # 1. 文件夹命名检查
    folder_rules = rules.get("FolderRules", {})
    folder_regex = folder_rules.get("regex", "未设置")
    folder_naming_result = check_results.get("folder_naming", False)
    if folder_naming_result:
        pass_items.append(f"文件夹命名检查通过：输入 '{folder_name}' 符合正则 {folder_regex}")
    else:
        fail_items.append(f"文件夹命名检查未通过：输入 '{folder_name}' 不符合正则 {folder_regex}")
    report["folder_naming"] = {
        "expected": f"学生文件夹命名必须为 学生学号+班号+姓名",
        "actual": folder_name,
        "result": folder_naming_result
    }

    # 2. 上传文件列表
    report["uploaded_files"] = saved_files

    # 3. 学生材料检查
    student_materials_results = check_results.get("StudentMaterials", {})
    # 对每个文件规则生成检查说明
    for rule_id, result in student_materials_results.items():
        messages = []
        # 文件命名匹配情况
        if result.get("matched_files"):
            messages.append(f"匹配到文件: {result['matched_files']}")
        else:
            messages.append("未匹配到任何文件")
        # 版本检查
        if "version_ok" in result:
            if result["version_ok"]:
                messages.append("版本检查通过")
            else:
                messages.append("版本检查未通过")
        # 内容关键字检查（如果有）
        if "content_check" in result:
            for item in result["content_check"]:
                if item["result"]:
                    messages.append(f"{item['file']} 内容检查通过：{item['message']}")
                else:
                    messages.append(f"{item['file']} 内容检查未通过：{item['message']}")
        # 签名检查（如果有）
        if "signature_check" in result:
            for item in result["signature_check"]:
                if item["result"]:
                    messages.append(f"{item['file']} 签名检查通过：{item['message']}")
                else:
                    messages.append(f"{item['file']} 签名检查未通过：{item['message']}")
        # 判断此规则整体是否通过：只要有“未通过”的提示，则视为失败
        rule_status = "通过" if all("未通过" not in m for m in messages) else "未通过"
        message_str = "; ".join(messages)
        if rule_status == "通过":
            pass_items.append(f"学生材料 {rule_id}: {message_str}")
        else:
            fail_items.append(f"学生材料 {rule_id}: {message_str}")
    report["StudentMaterials"] = student_materials_results

    # 4. 答辩组材料检查
    review_materials = check_results.get("ReviewGroupMaterials", {})
    for rule_id, result in review_materials.items():
        messages = []
        if result.get("matched_files"):
            messages.append(f"匹配到文件: {result['matched_files']}")
        else:
            messages.append("未匹配到任何文件")
        if "version_ok" in result:
            if result["version_ok"]:
                messages.append("版本检查通过")
            else:
                messages.append("版本检查未通过")
        rule_status = "通过" if all("未通过" not in m for m in messages) else "未通过"
        message_str = "; ".join(messages)
        if rule_status == "通过":
            pass_items.append(f"答辩组材料 {rule_id}: {message_str}")
        else:
            fail_items.append(f"答辩组材料 {rule_id}: {message_str}")
    report["ReviewGroupMaterials"] = review_materials

    # 5. 日期检查
    date_rules = check_results.get("DateRules", {})
    if date_rules.get("date_format_ok") and date_rules.get("sequence_ok"):
        pass_items.append("日期检查通过")
    else:
        fail_items.append("日期检查未通过，请核对日期格式或顺序")
    report["DateRules"] = date_rules

    # 6. 添加通过和未通过项到报告中
    report["pass_items"] = pass_items
    report["fail_items"] = fail_items

    return report
