import xml.etree.ElementTree as ET
import pprint


def parse_validation_rules(xml_path):
    """
    解析扩展后的 XML 规则，返回一个包含所有规则的字典。
      1. FolderRules：文件夹命名规则（<FolderNaming>）
      2. StudentMaterials：学生材料要求，包含 Files 节点及签名检查要求
      3. ReviewGroupMaterials：答辩组材料要求
      4. DateRules：日期格式和顺序要求（包含 DateFormat 和 Chronological）
      5. VersionRequirements：文件版本要求（例如，除部分文件外必须双版本）
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    rules = {}

    # 1. 解析 FolderRules
    folder_rules = {}
    folder_naming_elem = root.find("FolderRules/FolderNaming")
    if folder_naming_elem is not None:
        folder_rules["desc"] = folder_naming_elem.get("desc")
        regex_elem = folder_naming_elem.find("Regex")
        if regex_elem is not None and regex_elem.text:
            folder_rules["regex"] = regex_elem.text.strip()
    rules["FolderRules"] = folder_rules

    # 2. 解析 StudentMaterials
    student_materials = {}
    student_files = []
    files_elem = root.find("StudentMaterials/Files")
    if files_elem is not None:
        for file_elem in files_elem.findall("File"):
            file_rule = {
                "id": file_elem.get("id"),
                "desc": file_elem.get("desc"),
                "versions": file_elem.get("versions")
            }
            pattern_elem = file_elem.find("Pattern")
            if pattern_elem is not None and pattern_elem.text:
                file_rule["pattern"] = pattern_elem.text.strip()
            extra_elem = file_elem.find("Extra")
            if extra_elem is not None and extra_elem.text:
                file_rule["extra"] = extra_elem.text.strip()
            note_elem = file_elem.find("Note")
            if note_elem is not None and note_elem.text:
                file_rule["note"] = note_elem.text.strip()
            sig_req_elem = file_elem.find("SignatureRequirement")
            if sig_req_elem is not None and sig_req_elem.text:
                # file_rule["signature_requirement"] = sig_req_elem.text.strip()
                file_rule["signature_requirement"] = sig_req_elem.get("role")  # 将 role 保存为 "teacher" 或 "student"
            repeat_elem = file_elem.find("Repeat")
            if repeat_elem is not None and repeat_elem.text:
                file_rule["repeat"] = repeat_elem.text.strip()
            student_files.append(file_rule)
    student_materials["Files"] = student_files
    # 签名检查要求
    sig_check_elem = root.find("StudentMaterials/SignatureCheck")
    if sig_check_elem is not None:
        exclude = sig_check_elem.get("exclude")
        student_materials["SignatureCheck"] = {
            "default": sig_check_elem.get("default"),
            "exclude": [s.strip() for s in exclude.split(",")] if exclude else []
        }
    rules["StudentMaterials"] = student_materials

    # 3. 解析 ReviewGroupMaterials
    review_group = {}
    review_files = []
    review_files_elem = root.find("ReviewGroupMaterials/Files")
    if review_files_elem is not None:
        for file_elem in review_files_elem.findall("File"):
            file_rule = {
                "id": file_elem.get("id"),
                "desc": file_elem.get("desc"),
                "versions": file_elem.get("versions")
            }
            pattern_elem = file_elem.find("Pattern")
            if pattern_elem is not None and pattern_elem.text:
                file_rule["pattern"] = pattern_elem.text.strip()
            repeat_elem = file_elem.find("Repeat")
            if repeat_elem is not None and repeat_elem.text:
                file_rule["repeat"] = repeat_elem.text.strip()
            review_files.append(file_rule)
    review_group["Files"] = review_files
    rules["ReviewGroupMaterials"] = review_group

    # 4. 解析 DateRules
    date_rules = {}
    date_format_elem = root.find("DateRules/DateFormat")
    if date_format_elem is not None:
        date_rules["date_format_regex"] = date_format_elem.get("regex")
    chronological = []
    chronological_elem = root.find("DateRules/Chronological")
    if chronological_elem is not None:
        for field_elem in chronological_elem.findall("Field"):
            field_rule = {"name": field_elem.get("name")}
            # 可选属性：minOffset, after, before
            if field_elem.get("minOffset"):
                field_rule["minOffset"] = field_elem.get("minOffset")
            if field_elem.get("after"):
                field_rule["after"] = field_elem.get("after")
            if field_elem.get("before"):
                field_rule["before"] = field_elem.get("before")
            chronological.append(field_rule)
    date_rules["Chronological"] = chronological
    rules["DateRules"] = date_rules

    # 5. 解析 VersionRequirements
    version_requirements = []
    for rule_elem in root.findall("VersionRequirements/Rule"):
        version_rule = {
            "id": rule_elem.get("id"),
            "desc": rule_elem.get("desc")
        }
        exclude_elem = rule_elem.find("Exclude")
        if exclude_elem is not None:
            excluded_files = [f_elem.text.strip() for f_elem in exclude_elem.findall("File") if f_elem.text]
            version_rule["exclude"] = excluded_files
        version_requirements.append(version_rule)
    rules["VersionRequirements"] = version_requirements

    return rules


if __name__ == "__main__":
    xml_path = "../../rules1.xml"
    rules = parse_validation_rules(xml_path)
    pprint.pprint(rules)
