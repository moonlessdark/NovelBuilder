
from PySide6.QtCore import Signal


def process_text_outside_quotes(text: str) -> str:
    """
    处理不在“和”之间的所有句号“。”，替换为“。\n”
    :param text: 输入文本
    :return: 处理后的文本
    """
    result = []
    quote_stack = []  # 使用栈结构处理嵌套引号
    buffer = []

    for i, char in enumerate(text):
        if char == '“':
            quote_stack.append(i)  # 入栈：进入引号块
            buffer.append(char)
        elif char == '”':
            if quote_stack:
                quote_stack.pop()  # 出栈：退出引号块
            else:
                raise ValueError(f'多余出现的“””，位置：{i}')
            buffer.append(char)
        elif char == '。' and not quote_stack:
            # 如果当前句号不在任何引号中，则替换为 。\n
            result.extend(buffer)
            result.append('。\n')
            buffer = []
        else:
            buffer.append(char)

    # 添加剩余字符
    result.extend(buffer)

    return ''.join(result)


def check_quotes_match(text: str) -> int:
    """
    检查文本中的“和”是否成对匹配，支持嵌套。
    如果不匹配，提示第一个不匹配的符号位置。
    :param text: 输入文本
    """

    quote_stack = []  # 栈用于跟踪“的位置
    for i, char in enumerate(text):
        if char == '“':
            quote_stack.append(i)  # 入栈：记录“的位置
        elif char == '”':
            if quote_stack:
                quote_stack.pop()  # 出栈：匹配到一个”
            else:
                # print(f'多余出现的” ，位置：{i}——{text[i-10: i+10]}')
                return i
    if len(quote_stack) > 2:
        # 如果连续出现3个嵌套的 “” 符号，那也太怪了，大概是又问题的。
        return quote_stack[0]
    return -1


def check_the_last_character_is_dialogue_character(content: str):
    """
    这句话的最后一行，是个 : 符号，并且如果下一个字符是双引号中的开始符号，表示这句话还没有说完。
    :param content:
    :return:
    """
    if type(content) is str:
        content: list = content.split("\n")

    first_char_index: int = 0  # 下标

    # 预先计算每行的长度（包括换行符）
    line_lengths = [len(line) + 1 for line in content]

    for line_index in range(len(content) - 1):
        _index_content_line: str = content[line_index]
        _next_content_line: str = content[line_index + 1]

        # 检查当前行是否包含冒号且下一行以引号开头
        if ':' in _index_content_line and _next_content_line.lstrip().startswith(('“', '”')):
            return first_char_index

        # 更新下一行首字符的索引位置
        first_char_index += line_lengths[line_index]

    return -1


def check_first_str_is_double_quotation_marks(content: str):
    """
    检查是否存在双引号中没有内容
    :param content:
    :return:
    """
    for i, char in enumerate(content):
        if char == '“”':
            return i
    return -1


def check_double_quotation_marks_is_paired(content: str) -> int:
    """
    这一行文字里，开始和结束的双引号是否只有一个。
    出现了开始符号就必须有结束符号。且开始符号和结束符号必须是成队的。
    :param content:
    :return:
    """
    if type(content) is str:
        content: list = content.split("\n")

    first_char_index: int = 0  # 下标

    # 预先计算每行的长度（包括换行符）
    line_lengths = [len(line) + 1 for line in content]

    for line_index in range(len(content) - 1):
        _index_content_line: str = content[line_index].strip()
        _start_index_list: list = [i for i, x in enumerate(_index_content_line) if x == '“']
        _end_index_list: list = [i for i, x in enumerate(_index_content_line) if x == '”']
        # 检查当前行是否包含冒号且下一行以引号开头
        if len(_start_index_list) != len(_end_index_list):
            # 如果开始符号的数量和结束符号的数量不一致，表示肯定有问题
            return first_char_index
        else:
            if not __validate_arrays(_start_index_list, _end_index_list):
                # 如果开始符号的下一个字符不是结束符号，表示肯定有问题,以下数组满足条件
                # [2, 5], [3, 7]
                # [3, 5], [7, 9]
                return first_char_index
        # 更新下一行首字符的索引位置
        first_char_index += line_lengths[line_index]
    return -1


def __validate_arrays(arr_a, arr_b) -> bool:
    """
    校验两个数组的元素关系：
    1. 同下标下a数组元素必须小于b数组元素
    2. 同一数组内元素必须严格递增
    """
    # 基础校验
    if len(arr_a) != len(arr_b) or len(arr_a) < 2:
        return False

    # 校验数组内严格递增
    def is_strictly_increasing(arr):
        return all(x < y for x, y in zip(arr, arr[1:]))

    # 校验跨数组关系和内部顺序
    return (all(a < b for a, b in zip(arr_a, arr_b)) and
            is_strictly_increasing(arr_a) and
            is_strictly_increasing(arr_b))


def check_double_quotation_marks(content: str) -> int:
    """
    检查文字中的双引号是否正常、是成对的
    :param content:
    :return:
    """
    _first_str_index_list: list = []

    _first_str_index: int = check_quotes_match(content)
    _first_str_index_list.append(_first_str_index)

    if type(content) is str:
        content: list = content.split("\n")

    func_list = [check_the_last_character_is_dialogue_character,
                 check_first_str_is_double_quotation_marks,
                 check_double_quotation_marks_is_paired]

    for func in func_list:
        _x: int = func(content)
        if _x not in _first_str_index_list:
            _first_str_index_list.append(_x)
    _first_str_index_list.sort()
    return _first_str_index_list[0]


# 示例用法
if __name__ == '__main__':
    content: str = '这是一个。“测“试””。用来。查找“引。“号”的位置。”。知。道。吗。'

