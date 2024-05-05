"""
非段落换行处理逻辑：
1、检测每个换行符的next字符是否是句号，分号，感叹号，疑问号，结束符的双引号，单引号。如果是的话表示这句话没有说完。 返回False。
2、如果不满足条件1，那么检测换行符last字符是否是 句号，分号，感叹号，疑问号，结束符的双引号，单引号。 如果是的话表示 这句话已经说完了，返回True
"""
import re

from Businese.FormatMode.LineWrapFormat import LineWrap


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
        return self.first_line_tab(format_content)

    @staticmethod
    def first_line_tab(content: str or list) -> list:
        """
        首行缩进
        :param content:
        :return:
        """
        if type(content) == str:
            content: list = content.split("\n")
        content_list: list = content
        for arr_index in range(len(content_list)):
            if '\u3000' not in content_list[arr_index]:
                content_list[arr_index] = '\u3000\u3000' + str(content_list[arr_index])
        return content_list
