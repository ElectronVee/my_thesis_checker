import os
import unittest
from app.utils.format_checker import check_file_naming, check_file_versions
from app.utils.content_checker import check_file_content_keywords


class TestStudentMaterials(unittest.TestCase):
    def setUp(self):
        # 模拟上传文件列表（文件名列表）
        self.saved_files = [
            "1-2-12345678张三-论文.docx",
            "1-2-12345678张三-论文.pdf"
        ]
        # 模拟文件夹路径
        self.folder_path = "test_upload"
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        # 创建模拟的 DOCX 文件或 PDF 文件（这里仅测试命名与版本检查）
        for file_name in self.saved_files:
            with open(os.path.join(self.folder_path, file_name), "w", encoding="utf-8") as f:
                # 对于论文文件，写入关键字
                if "论文" in file_name:
                    f.write("这是毕业设计（论文）任务书的内容测试。")
                else:
                    f.write("测试文件内容。")

    def tearDown(self):
        # 清理测试文件夹
        for f in os.listdir(self.folder_path):
            os.remove(os.path.join(self.folder_path, f))
        os.rmdir(self.folder_path)

    def test_file_naming(self):
        # 测试文件命名是否符合规则
        pattern = r"^1-2-\d{8}[\u4e00-\u9fa5]+-论文\.(docx|pdf)$"
        for file_name in self.saved_files:
            self.assertTrue(check_file_naming(file_name, pattern))

    def test_version_check(self):
        # 对于论文文件，要求双版本存在
        # 使用文件名前缀（除扩展名部分）检查是否同时有 docx 和 pdf
        base_name = "1-2-12345678张三-论文"
        version_ok = check_file_versions(self.saved_files, base_name, "double")
        self.assertTrue(version_ok)

    # def test_content_check(self):
    #     # 测试论文文件内容是否包含关键字"毕业设计（论文）任务书"
    #     file_path = os.path.join(self.folder_path, "1-2-12345678张三-论文.docx")
    #     result, msg = check_file_content_keywords(file_path, ["毕业设计（论文）任务书"])
    #     self.assertTrue(result, msg)


if __name__ == '__main__':
    unittest.main()
