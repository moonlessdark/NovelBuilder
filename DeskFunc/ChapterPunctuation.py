
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
    # if quote_stack:
    #     # 提示第一个未闭合的“的位置 你TM这个怂卵
    #     print(f'缺少匹配的 ” ，第一个未闭合的“位置：{quote_stack[0]}--{text[quote_stack[0]-10: quote_stack[0]+10]}')
    #     return quote_stack[0]
    return -1



# 示例用法
if __name__ == '__main__':
    content: str = '这是一个。“测“试””。用来。查找“引。“号”的位置。”。知。道。吗。'

