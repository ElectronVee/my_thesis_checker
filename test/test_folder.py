import unittest
from app.utils.format_checker import check_folder_naming


class TestFolderNaming(unittest.TestCase):
    def setUp(self):
        # 定义正确的正则表达式，学生学号8位，班号6位，姓名至少1个中文字符
        self.regex = r"^\d{8}-\d{6}-[\u4e00-\u9fa5]+$"

    def test_valid_folder_name(self):
        # 正确的文件夹名称
        folder_name = "12345678-123456-张三"
        self.assertTrue(check_folder_naming(folder_name, self.regex))

    def test_invalid_folder_name_missing_dash(self):
        # 缺少中划线，格式不符合要求
        folder_name = "12345678123456李四"
        self.assertFalse(check_folder_naming(folder_name, self.regex))

    def test_invalid_folder_name_wrong_student_number(self):
        # 学生学号不是8位
        folder_name = "1234567-123456-张三"
        self.assertFalse(check_folder_naming(folder_name, self.regex))

    def test_invalid_folder_name_wrong_class_number(self):
        # 班号不是6位
        folder_name = "12345678-12345-张三"
        self.assertFalse(check_folder_naming(folder_name, self.regex))

    def test_invalid_folder_name_non_chinese_name(self):
        # 姓名部分不是中文（或者为空）
        folder_name = "12345678-123456-ZhangSan"
        self.assertFalse(check_folder_naming(folder_name, self.regex))


if __name__ == '__main__':
    unittest.main()
