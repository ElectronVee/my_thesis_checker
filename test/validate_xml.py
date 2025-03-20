import xml.etree.ElementTree as ET

def validate_xml(file_path):
    """
    尝试解析 XML 文件
    """
    try:
        # 尝试解析 XML 文件
        tree = ET.parse(file_path)
        # 获取根节点，若没有异常说明文件格式正确
        root = tree.getroot()
        print("XML 文件格式正确!")
        print("根节点标签为:", root.tag)
        return tree
    except ET.ParseError as e:
        # 捕获解析异常，输出错误信息
        print("XML 文件格式错误:")
        print(e)
        return None

if __name__ == "__main__":
    # 指定要验证的 XML 文件路径（请确保文件存在且路径正确）
    xml_file = "../rules1.xml"
    tree = validate_xml(xml_file)
    # 若需要进一步处理，确保 tree 不为 None
    if tree:
        # 在此可以继续处理 XML 数据
        pass
