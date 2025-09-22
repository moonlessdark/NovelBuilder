import re

from DeskFunc.ChapterPunctuation import check_double_quotation_marks_is_paired, validate_arrays


class LineWrap:
    """
    按锁紧换行
    """

    def __init__(self):
        self.__warp_tag_left: list = ['。', '！', '!', "…", "？", '?', '；', ';']  # 左侧碰到这些字符，就可以正常换行了
        self.__warp_tag_special: list = ['"', '」']  # 左侧碰到这个字符，需要特殊判断。1:换行符中出现到这个字符之间，出现了偶数，表示可以换行。如果是个奇数，那么就不换行

    @staticmethod
    def first_line_tab(content: str or list) -> str:
        """
        首行缩进和段落插入空白行
        :param content:
        :return:
        """
        if type(content) is str:
            content: list = content.split("\n")
        content_list: list = content
        new_content_list: list = []
        for arr_index in range(len(content_list)):
            _temp_str = content_list[arr_index].strip()
            if _temp_str == "":
                continue
            elif _temp_str.find('\u3000\u3000') != 0:
                new_content_list.append('\u3000\u3000' + str(_temp_str) + '\n')
            else:
                new_content_list.append(str(_temp_str) + '\n')
        return "\n".join(new_content_list)

    @staticmethod
    def check_str_in_display_width(content: str) -> str:
        """
        处理换行，缩进模式，按照首行缩进来判断。
        :param content:
        :return:
        """
        if type(content) is str:
            content: list = content.split("\n")
        content_list: list = list(filter(lambda num: num != "", content))

        _line_str_list: list = []
        _all_content_list: list = []
        _is_passages: bool = False  # 默认是一段的话
        for x in content_list:
            x = x.replace(" ", "")
            if x.find('\u3000') == 0:
                if len(_line_str_list) != 0:
                    # 如果最新的一句话，找到的缩进符，且追加的数组中已经有内容了，说明上一句已经说完了。
                    _line_str_list.append('\n')
                    _ss_line_str: list = _line_str_list.copy()
                    _all_content_list.append(_ss_line_str)
                    _line_str_list.clear()
            _line_str_list.append(x)
        if len(_line_str_list) != 0:
            # 结束循环了，发现还有一段话没有录入，那么就加入一下
            _line_str_list.append('\n')
            _ss_line_str: list = _line_str_list.copy()
            _all_content_list.append(_ss_line_str)
            _line_str_list.clear()
        _all_content: str = ""
        for _line_str_list in _all_content_list:
            _new_line_str_list: list = _line_str_list.copy()
            _all_content += "".join(_new_line_str_list)
        return _all_content

    def newline_after_period_outside_quotes(self, text: str):
        """
        排班
        :param text:
        :return:
        """
        _content_list: list = text.split("\n")
        _f_content_list: list = []
        for _c in _content_list:
            if _c == "":
                continue
            _f_c: str = self.add_newline_after_punctuation_outside_quotes(_c)
            _f_content_list.append(_f_c)
        return "\n".join(_f_content_list)

    @staticmethod
    def merge_period_outside_quotes(text_list: str):
        """
        将错误换行的双引号合并一下
        """
        if type(text_list) is str:
            text_list: list = text_list.split('\n')
        _temp_line: str = ""
        _is_over: bool = False
        for line in text_list:
            _temp_line = _temp_line + line.strip()
            if _temp_line == "":
                continue
            _index_content_line: str = _temp_line
            _start_index_list: list = [i for i, x in enumerate(_index_content_line) if x == '「']
            _end_index_list: list = [i for i, x in enumerate(_index_content_line) if x == '」']
            if validate_arrays(_start_index_list, _end_index_list):
                _is_over = True
            else:
                _is_over = False
            if _is_over:
                _temp_line += '\n'
        return _temp_line

    @staticmethod
    def add_newline_after_period_outside_quotes(text: str):
        # 1. 找出所有在「」之间的内容，并记录它们的范围
        quote_ranges = []
        for match in re.finditer(r'「[^」]*?」', text):
            quote_ranges.append(match.span())

        # 2. 遍历所有句号的位置，并判断是否在「」之外
        result = ''
        prev_pos = 0
        for period_match in re.finditer('。', text):
            pos = period_match.start()

            # 判断当前句号是否在任何「」范围内
            inside_quotes = False
            for start, end in quote_ranges:
                if start < pos < end:
                    inside_quotes = True
                    break

            # 如果句号不在「」中，则添加换行符
            if not inside_quotes:
                result += text[prev_pos:pos + 1] + '\n'
            else:
                result += text[prev_pos:pos + 1]
            prev_pos = pos + 1
        # 添加剩余部分
        result += text[prev_pos:]
        return result

    @staticmethod
    def add_newline_after_punctuation_outside_quotes(text: str) -> str:
        """
        在指定标点（。！？；）后添加换行符，但跳过引号内的标点

        参数:
            text: 待处理文本字符串

        返回:
            处理后的文本字符串，非引号内标点后均有换行符

        示例:
            输入：'你好！这是"测试？文本"。结束；'
            输出：'你好！\n这是"测试？文本"。\n结束；\n'
        """
        # 1. 定位所有中文引号区块
        quote_blocks = [match.span() for match in re.finditer(r'「[^」]*?」', text)]

        # 2. 处理四种标点符号
        result = []
        prev_pos = 0
        for punt_match in re.finditer(r'[。！？；]', text):
            pos = punt_match.start()
            # 检查是否在引号范围内
            in_quotes = any(start < pos < end for start, end in quote_blocks)

            # 截取片段并决定是否换行
            result.append(text[prev_pos:pos + 1])
            if not in_quotes:
                result.append('\n')
            prev_pos = pos + 1

        # 3. 添加剩余文本
        result.append(text[prev_pos:])
        return ''.join(result)
