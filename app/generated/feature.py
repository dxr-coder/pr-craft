```python
def parse_txt(file_path, encoding='utf-8', line_parser=None):
    """解析txt文件，返回行列表。

    Args:
        file_path (str): 文件路径
        encoding (str): 文件编码，默认 UTF-8
        line_parser (callable, optional): 可选的行解析函数，接收一行字符串（不含换行符），
                                          返回解析后的对象。若为 None，则返回原始字符串行。

    Returns:
        list: 包含解析后的行对象的列表

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 文件解码失败
    """
    results = []
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            for line in f:
                stripped = line.rstrip('\n\r')   # 去除行尾换行符
                if line_parser:
                    try:
                        parsed = line_parser(stripped)
                    except Exception:
                        # 可根据需要记录日志或跳过，此处选择跳过异常行
                        continue
                else:
                    parsed = stripped
                results.append(parsed)
    except FileNotFoundError:
        raise
    except UnicodeDecodeError:
        raise ValueError(f"Cannot decode file with encoding {encoding}")
    return results
```