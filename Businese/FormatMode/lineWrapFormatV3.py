"""
非段落换行处理逻辑：
1、检测每个换行符的next字符是否是句号，分号，感叹号，疑问号，结束符的双引号，单引号。如果是的话表示这句话没有说完。 返回False。
2、如果不满足条件1，那么检测换行符last字符是否是 句号，分号，感叹号，疑问号，结束符的双引号，单引号。 如果是的话表示 这句话已经说完了，返回True
"""
import re

from Businese.FormatMode.str_display_width import gbkwordslen
from collections import Counter


class LineWrapV3:

    def __init__(self):
        self.__warp_tag_left: list = ['。', '！', '!', "…", "？", '?', '；', ';']  # 左侧碰到这些字符，就可以正常换行了
        self.__warp_tag_special: list = ['"', '”']  # 左侧碰到这个字符，需要特殊判断。1:换行符中出现到这个字符之间，出现了偶数，表示可以换行。如果是个奇数，那么就不换行

    def check_str_is_line(self, content: str) -> list:
        """

        :param content: 完整的，还没有处理过的文本内容
        :return:
        """

        def replace_char_at_index(s, index, new_char):
            """
            替换字符串s中指定index下标的字符为new_char。
            """
            return s[:index] + new_char + s[index + 1:]

        format_content = content.replace("\u3000", "")
        format_content = format_content.replace(" ", "")
        format_str: list = ['”“', '」「', '。“', '""']
        for key_str in format_str:
            format_content = re.sub(key_str, key_str[0] + '\n' + key_str[1], format_content)
        end_index = []  # 已经是正确的换行符下标
        while 1:
            str_list = [sub_str.start() for sub_str in re.finditer('\n', format_content)]
            for str_arr in str_list:
                if str_arr in end_index:
                    continue
                if str_arr == len(format_content) - 1:
                    """
                    已经是最后一个字符
                    """
                    end_index.append(str_arr)
                    break
                if str_arr == 0:
                    """
                    第一个字符
                    """
                    end_index.append(str_arr)
                    continue
                if any(wrap_str == format_content[str_arr + 1] for wrap_str in self.__warp_tag_left):
                    """
                    如果下一个字符出现了表示可以结束的符号(句号，问号，感叹号，分号，结束双引号),那么就是没结束
                    """
                    format_content = replace_char_at_index(format_content, str_arr, "")
                elif any(wrap_str == format_content[str_arr - 1] for wrap_str in self.__warp_tag_left) or any(wrap_str == format_content[str_arr - 1] for wrap_str in self.__warp_tag_special):
                    """
                    如果上一个字符出现了表示对话结束的符号，那么就表示话说完了
                    """
                    end_index.append(str_arr)
                    continue
                else:
                    format_content = replace_char_at_index(format_content, str_arr, "")
                break
            if 0 < len(end_index) == len(str_list):
                break
        format_content: str = format_content.replace("\n\n", "\n")
        return format_content.split('\n')

    @staticmethod
    def first_line_tab(content: str or list) -> str:
        """
        首行缩进和段落插入空白行
        :param content:
        :return:
        """
        if type(content) == str:
            content: list = content.split("\n")
        content_list: list = content
        new_content_list: list = []
        for arr_index in range(len(content_list)):
            _temp_str = content_list[arr_index].strip()
            if _temp_str == "":
                continue
            elif '\u3000\u3000' not in _temp_str:
                new_content_list.append('\u3000\u3000' + str(_temp_str) + '\n')
        return "\n".join(new_content_list)

    @staticmethod
    def plus_str_format(content: str) -> str:
        """
        打个补丁先
        检查所有结束双引号的前面是不是一个 换行符，如果是的话，那么就处理一下
        :param content:
        :return:
        """
        __f_str_list: list = ['”', '」']
        __f_c: str = content
        for _f_str in __f_str_list:
            __f_c: str = __f_c.replace('\n'+"     "+_f_str, _f_str)
        return __f_c

    @staticmethod
    def plus_str_remove_spaces_between_quotes(text: str) -> str:
        """
        补丁2
        使用正则表达式匹配双引号(中文模式)之间的换行符，并将换行符剔除掉
        :param text:
        :return:
        """
        # res_f: str = re.sub(r'(“[^”]*?\n[^”]*?”)', r'\1\2', text)

        # res_f: str = re.sub(r'(“[^"]*)\n([^"]*”)', r'\1\2', text)
        def find_newlines_between_quotes(text):
            # 正则表达式匹配双引号之间的换行符
            newlines_between_quotes = re.findall(r'(“[^”]*?)\n([^”]*?”)', text)
            return newlines_between_quotes

        newlines = find_newlines_between_quotes(text)
        for newline in newlines:
            novel_str_list: list = text.split(str("\n".join(newline)))
            left_str = novel_str_list[0]
            right_str = novel_str_list[1]
            text = left_str + str("".join(newline)).replace("\n", "") + right_str
            # print("____>>>>>>" + str("".join(newline)))
        return text

    def check_str_in_display_width(self, content: str) -> str:
        """
        按照屏幕显示宽度来判断要不是移除换行符
        这个方法逻辑简单很多
        :param content:
        :return:
        """
        if type(content) == str:
            content: list = content.split("\n")
        content_list: list = list(filter(lambda num: num != "", content))
        _line_str_display_width: list = []
        for str_w in content_list:
            _line_str_display_width.append(gbkwordslen(str_w))
        # 大部份的宽度是这个值，在这个值附近偏移量5之内的换行符，都可以去掉
        # most_line_width: int = Counter(_line_str_display_width).most_common(1)[0][0]
        # 但是根据真实情况，应该拿最大的长度比较合理
        max_line_width: int = max(_line_str_display_width)
        new_content: str = ""
        for str_width, str_line in zip(_line_str_display_width, content_list):
            if not max_line_width - 7 <= str_width <= max_line_width:
                # 在这个值附近偏移量5之内的换行符，都可以去掉
                str_line = str_line.strip() + '\n'
            else:
                # 如果在这个范围内，但是又以为句号结尾。那么就当这句话说完了
                if str_line.strip()[-1:] in self.__warp_tag_left + self.__warp_tag_special:
                    str_line = str_line.strip() + '\n'
                else:
                    str_line = str_line.strip()
            new_content += str_line
        if new_content == "":
            new_content = content
        return new_content

    @staticmethod
    def check_str_in_display_width_v2(content: str) -> str:
        """
        处理换行，缩进模式，按照首行缩进来判断。
        :param content:
        :return:
        """
        if type(content) == str:
            content: list = content.split("\n")
        content_list: list = list(filter(lambda num: num != "", content))

        _line_str_list: list = []
        _all_content_list: list = []
        _is_passages: bool = False  # 默认是一段的话
        for x in content_list:
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
