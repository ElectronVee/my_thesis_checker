import os
from flask import render_template, request
from app import app
from app.utils.format_checker import check_folder_naming, check_file_naming, check_file_versions
from app.utils.content_checker import check_file_content_keywords
from app.utils.signature_checker import check_electronic_signature, check_signature_in_pdf
from app.utils.date_checker import check_date_format, check_date_sequence
from app.utils.xml_parser import parse_validation_rules
from app.utils.report import generate_report
import pprint


@app.route('/')
def index():
    return render_template("upload.html")


@app.route('/upload', methods=["POST"])
def upload_file():
    # 获取文件夹名称和上传的文件
    folder_name = request.form.get("folder_name")
    uploaded_files = request.files.getlist("files")

    # 保存文件到指定文件夹
    saved_files = []
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for file in uploaded_files:
        if file.filename:
            filename = file.filename
            file_path = os.path.join(folder_path, filename)
            file.save(file_path)
            saved_files.append(filename)

    # 加载 XML 规则
    xml_rules_path = r"D:\pythonProject\rules1.xml"
    rules = parse_validation_rules(xml_rules_path)

    # 调用各个检查模块，汇总检查结果
    check_results = {}
    # ① 文件夹命名检查
    folder_regex = rules.get("FolderRules", {}).get("regex")
    check_results["folder_naming"] = check_folder_naming(folder_name, folder_regex)

    # ② 学生材料检查
    student_materials_results = {}
    student_files_rules = rules.get("StudentMaterials", {}).get("Files", [])
    for file_rule in student_files_rules:
        rule_id = file_rule.get("id")
        desc = file_rule.get("desc")
        pattern = file_rule.get("pattern")
        versions_required = file_rule.get("versions")

        # 根据规则匹配上传文件中符合此规则的文件
        matched = [f for f in saved_files if check_file_naming(f, pattern)]

        # 版本检查：如果要求双版本，对于查重报告（6-1和6-2）允许仅有 PDF 版，否则必须同时存在 Word 和 PDF 版
        version_ok = True
        if versions_required == "double":
            docx_files = [f for f in matched if f.lower().endswith(".docx")]
            pdf_files = [f for f in matched if f.lower().endswith(".pdf")]
            if rule_id in ["check_report_simple", "check_report_complex","format_report"]:
                # 查重报告只要求至少有 PDF 版
                version_ok = (len(pdf_files) > 0)
            else:
                version_ok = (len(docx_files) > 0 and len(pdf_files) > 0)

        # 记录该文件规则的检查结果
        student_materials_results[rule_id] = {
            "desc":desc,
            "matched_files": matched,
            "version_ok": version_ok
        }

        # 内容关键字检查
        if "extra" in file_rule:
            keywords = []
            if "论文" in file_rule.get("desc", ""):
                keywords.append("毕业设计（论文）任务书")
            content_checks = []
            for f in matched:
                file_path = os.path.join(folder_path, f)
                content_ok, content_msg = check_file_content_keywords(file_path, keywords)
                content_checks.append({"file": f, "result": content_ok, "message": content_msg})
            student_materials_results[rule_id]["content_check"] = content_checks

        # 电子签名检查
        if "signature_requirement" in file_rule:
            sig_checks = []
            for f in matched:
                file_path = os.path.join(folder_path, f)
                sig_ok, sig_msg = check_electronic_signature(file_path)
                sig_checks.append({"file": f, "result": sig_ok, "message": sig_msg})
            student_materials_results[rule_id]["signature_check"] = sig_checks

        check_results["StudentMaterials"] = student_materials_results
        # if "signature_requirement" in file_rule:
        #     sig_checks = []
        #     # 获取签名要求的角色：teacher 或 student
        #     expected_role = file_rule.get("signature_requirement")
        #     #test--待修改
        #     expected_name = "李永" if expected_role == "teacher" else "张三"
        #     # 临时目录保存提取图片
        #     pic_path = app.config['TEMP_IMAGE_FOLDER']
        #     for f in matched:
        #         file_path = os.path.join(folder_path, f)
        #         # 如果是 PDF 文件，调用新的函数检查第一页签名
        #         if f.lower().endswith(".pdf"):
        #             sig_ok, sig_msg = check_signature_in_pdf(file_path, expected_name, pic_path, role=expected_role)
        #             sig_checks.append({"file": f, "result": sig_ok, "message": sig_msg})
        #         else:
        #             # 对于非PDF文件暂不检查签名，或可以添加其它处理
        #             sig_checks.append({"file": f, "result": None, "message": "非PDF文件，未检查签名"})
        #     student_materials_results[rule_id]["signature_check"] = sig_checks

    # ③ 答辩组材料检查*
    review_materials_results = {}
    review_files_rules = rules.get("ReviewGroupMaterials", {}).get("Files", [])
    for file_rule in review_files_rules:
        rule_id = file_rule.get("id")
        pattern = file_rule.get("pattern")
        matched = [f for f in saved_files if check_file_naming(f, pattern)]
        review_materials_results[rule_id] = {"matched_files": matched, "version_ok": len(matched) > 0}
    check_results["ReviewGroupMaterials"] = review_materials_results

    # ④ 日期检查
    # 假设在学生材料检查中，规则 "defense_application" 包含教师评审表
    teacher_pdf_file = None
    if "defense_application_2" in student_materials_results:
        matched_files = student_materials_results["defense_application_2"].get("matched_files", [])
        for f in matched_files:
            if f.lower().endswith(".pdf"):
                teacher_pdf_file = os.path.join(folder_path, f)
                break

    # 如果找到了教师评审表的PDF文件，提取教师签字日期
    from app.utils.date_checker import extract_signing_date_from_pdf, check_teacher_sign_date
    if teacher_pdf_file:
        teacher_sign_date = extract_signing_date_from_pdf(teacher_pdf_file)
    else:
        teacher_sign_date = None

    # 答辩日期--?
    defense_date = "2025-06-12"

    # 检查日期格式与教师签字日期要求
    date_format_ok = check_date_format(defense_date)
    if teacher_sign_date:
        teacher_date_ok = check_teacher_sign_date(teacher_sign_date, defense_date)
    else:
        teacher_date_ok = False

    check_results["DateRules"] = {
        "teacher_sign_date": teacher_sign_date,
        "defense_date": defense_date,
        "date_format_ok": date_format_ok,
        "teacher_date_ok": teacher_date_ok
    }

    # 最终报告
    report = generate_report(folder_name, saved_files, rules, check_results)

    # 输出
    pprint.pprint(report)

    # 渲染结果模板
    return render_template("result.html", report=report)
