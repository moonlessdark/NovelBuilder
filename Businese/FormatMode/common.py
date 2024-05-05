# encoding: utf-8
import re

from PySide6.QtCore import Signal

from Resource.rexp_template import Template


class FormatCommon:
    """
    处理格式的方法
    """

    def __init__(self, sin_out: Signal = None, sin_out_status_bar: Signal = None):
        """
        全局模式和单行模式公用的一些方法
        """
        self.ad_str_tuple: tuple = Template.ad_str.value
        self.wrap_character_by_line: list[str] = Template.wrap_character_by_line.value
        self.wrap_character_by_end_double_quotes: list[str] = Template.wrap_character_by_end_double_quotes.value
        self.talk_str: list[str] = Template.talk_str.value
        self.talk_str_by_end_double_quotes: list[str] = Template.talk_str_by_end_double_quotes.value
        self.change_str: dict = Template.change_str.value
        self.sin_out = sin_out
        self.sin_out_status_bar = sin_out_status_bar

    @staticmethod
    def print_pyside_log(signal: Signal, content: str):
        """
        打印pyqt5的log
        :param signal: 打印日志的对象
        :param content: 打印的日志信息
        :return:
        """
        signal.emit(content)

    def clear_ad_str(self, content: str) -> str:
        """
        去除广告, 去除固定的以某个字符串开头+某个字符串结尾的广告
        :param content:
        :return:
        """
        for ad_num in self.ad_str_tuple:
            start, end = ad_num  # 拿到广告的开头和结尾字符
            rex = start + '(.*?)' + end
            result: list = re.findall(rex, content)
            if len(result) == 0:
                # 如果没有匹配到广告,那就继续循环
                continue
            for ad_str in range(len(result)):
                if ad_str == '':
                    continue
                else:
                    replace_str = start + str(result[ad_str]) + end
                    if '\\' in replace_str:
                        replace_str = replace_str.replace('\\', '')
                    content = content.replace(replace_str, '')
        return content

    def format_end_2_start_double_quotation_mark(self, content: str, text_title_name: str = "",
                                                 is_fix_quotation_mark=True) -> list:
        """
        检查双引号和开始双引号之间  例如， “xxxx”<换行>"xxxx"
        :param is_fix_quotation_mark: 是否尝试修复文本中的异常双引号
        :param text_title_name: 文章名称，用于打印检查到异常双引号号时的信息print信息
        :param content: 文章正文
        :return:
        """
        content = self.clear_ad_str(content)
        content = self.change_word(content)
        if is_fix_quotation_mark:
            content = self.check_double_quotes(content=content, text_title_name=text_title_name)
            if content == "":
                return []
        a = re.findall("”“", content)
        b = []
        if len(a) > 0:
            content = re.sub('”“', '”\\n“', content)
            content = re.sub('。“', '。\n“', content)
            content_list = content.split("\n")
            for ss in range(len(content_list)):
                if content_list[ss] != "":
                    b.append(content_list[ss])
            return b
        else:
            return [content]

    @staticmethod
    def fix_double_quotes_check(content: str):
        """
        尝试修复异常的双引号
        :param content: 正文内容
        :return:
        """
        start_str = '“'  # 开始双引号
        end_str = '”'  # 结束双引号

        left_list = [substr.start() for substr in re.finditer(start_str, content)]  # 查询开始字符串所有的index
        right_list = [substr.start() for substr in re.finditer(end_str, content)]  # 查询结束字符串所有的index
        temp_list: list = left_list  # 拼接一下
        temp_list.extend(right_list)
        temp_list.sort()  # 按照从小到大排序

        for i in range(len(temp_list) - 1):
            if len(temp_list) == i + 1:
                # 如果此时已经循环到最后一个了，
                break
            if i % 2 != 0:
                continue
            left = temp_list[i]
            right = temp_list[i + 1]
            if content[left] == start_str and content[right] == end_str:
                """
                第一个字符串是开始，第二个字符串是结束
                """
                continue
            else:
                if content[left] != start_str:
                    string_list = list(content)
                    string_list[left] = start_str
                    content = ''.join(string_list)
                if content[right] != end_str:
                    string_list = list(content)
                    string_list[right] = end_str
                    content = ''.join(string_list)
        return content

    def check_double_quotes(self, content: str, text_title_name: str = "", is_fix_double_quotes: bool = True) -> str:
        """
        检查双引号是否正确
        :param is_fix_double_quotes: 是否尝试修复异常双引号
        :param content: 正文内容
        :param text_title_name: 文本标题，用于出错时打印信息
        :return: 如果返回 ""，就表明双引号数量异常
        """
        left_list, right_list = self.check_double_quotes_left_right_str(content)
        sort_list: list = left_list if len(left_list) < len(right_list) else right_list  # 看看哪个数组更短
        if len(left_list) != len(right_list):
            for i in range(len(sort_list) - 1):
                if left_list[i] < right_list[i] < left_list[i + 1]:  # 再检查一次，确认所有的字符排序都是正常的。
                    continue
                elif left_list[i + 1] - left_list[i] == 1 and right_list[i + 1] - right_list[i] == 1:
                    # 这是一种特殊情况，对话中出现了一些特殊的名词，作者用双引号括起来了。
                    continue
                else:
                    tips_str: str = content[left_list[i]:left_list[i] + 20]
                    tips_str = tips_str if tips_str[-2:] == "\n" else tips_str + "\n"
                    if self.check_double_quotes_total_num is False:
                        # 左右双引号的数量异常，即开始的双引号数量不等于结束的双引号数量
                        is_fix_double_quotes = False
                    if is_fix_double_quotes:
                        self.print_pyside_log(self.sin_out,
                                              "该章节" + text_title_name + "从内容:\n" + tips_str + "开始出现双引号异常情况。\n正在尝试修复")
                        return self.fix_double_quotes_check(content)
                    self.print_pyside_log(self.sin_out,
                                          "该章节" + text_title_name + "从内容:\n" + tips_str + "开始出现双引号异常情况。\n请手动处理")
                    return ""
        return content

    def check_double_quotes_total_num(self, content: str) -> bool:
        """
        检查双引号的数量是否是偶数
        偶数标识有修复的可能
        :param content: 内容
        :return: False表示双引号是奇数，True表示是偶数
        """
        left_list, right_list = self.check_double_quotes_left_right_str(content)
        total_num: int = len(left_list) + len(right_list)
        if total_num % 2 != 0:
            # 说明不是偶数，出现了多余的双引号
            return False
        return True

    def check_double_quotes_error_index(self, content: str) -> int:
        """
        检查双引号，如果有异常，就返回开始的双引号的index
        :param content:
        :return: 0 开始符数量等于结束符数量。  >0的数字表示从哪个开始符开始有异常
        """
        left_list, right_list = self.check_double_quotes_left_right_str(content)
        sort_list: list = left_list if len(left_list) < len(right_list) else right_list  # 看看哪个数组更短
        if len(left_list) != len(right_list):
            for i in range(len(sort_list) - 1):
                if left_list[i] < right_list[i] < left_list[i + 1]:  # 再检查一次，确认所有的字符排序都是正常的。
                    continue
                else:
                    return left_list[i]
        return 0

    @staticmethod
    def check_double_quotes_left_right_str(content: str) -> tuple[list[int], list[int]]:
        """
        检查双引号是否齐全
        :param content: 代处理的内容
        :return:
        """
        if "“" in content:
            start_str = '“'  # 开始双引号
            end_str = '”'  # 结束双引号
        elif "」" in content:
            start_str = '「'  # 开始双引号
            end_str = '」'  # 结束双引号
        else:
            start_str = '“'  # 开始双引号
            end_str = '”'  # 结束双引号
        left_list = [substr.start() for substr in re.finditer(start_str, content)]  # 查询开始字符串所有的index
        right_list = [substr.start() for substr in re.finditer(end_str, content)]  # 查询结束字符串所有的index
        return left_list, right_list

    # def wrap_by_punctuation_mark_line(self,  content: str) -> str:
    #     """
    #     根据最后一个字符判断是否是需要换行的字符
    #     """
    #     change_line_str: list[str] = self.wrap_character_by_line  # 句号之类的，如果碰到这个标点符号，就换行
    #     content_format = ""
    #     content = [content] if type(content) is str else content
    #     for line_str in content:
    #         if line_str != "":
    #             content_list = []
    #             for change_line_i in change_line_str:
    #                 # 遍历一下需要换行的字符
    #                 line_change = re.sub(change_line_i, change_line_i + '\n', line_str)
    #                 content_list: list = line_change.split("\n")  # 先把原文本进行换行分割数组
    #             for n in range(len(content_list)):
    #                 if content_list[n][0:1] != "”":
    #                     # 如果该行的第一个字符不是结束双引号
    #                     content_format = content_format + '\n' + content_list[n]
    #                 else:
    #                     content_format = content_format + content_list[n]
    #     content_format = content if content_format == "" else content_format
    #     return content_format

    @staticmethod
    def check_str_is_line(content: str) -> bool:
        """
        检查这是否是完整的一句话
        :param content: 正文
        :return:
        """
        wrap_character = Template.wrap_character_by_line.value
        if content.count("“") == content.count("”"):  # 有完整的开始双引号和结束双引号
            if content.count("“") > 0:
                start_str_index: list = [substr.start() for substr in re.finditer('“', content)]
                end_str_index: list = [substr.start() for substr in re.finditer('”', content)]
                for i in range(len(start_str_index)):
                    if int(start_str_index[i]) > int(end_str_index[i]):
                        """
                        如果出现了结束符的下标小于开始符，说明换行符异常。需要进一步检测
                        """
                        return False
                if any(wrap_str in content[-1:] for wrap_str in wrap_character):
                    """
                    如果结尾出现了表示可以结束的符号
                    """
                    if content[:start_str_index[0]] == "" and content[end_str_index[0] + 1:] == "":
                        """
                        如果双引号的左侧和右侧都是空，表示这句话没说完
                        """
                        return False
                    return True
            else:
                # 说明这里面没有双引号
                return True
        return False

    @staticmethod
    def line_feed_format(content_list: list or str) -> list:
        """
        对每一行的文本进行处理，检查双引号后面是否跟着不需要换行的字符, 单行模式使用
        :param content_list: 正文, 类型可以 list也可以传 str
        :return:
        """
        result_list = []
        content_list = [content_list] if type(content_list) == str else content_list
        for ii in range(len(content_list)):
            lines = content_list[ii]
            if lines.count("“") == lines.count("”"):  # 有完整的开始双引号和结束双引号。当然也可能没有，那就是  0 == 0
                if lines.count("“") > 0:
                    start_str_index: list = [substr.start() for substr in re.finditer('“', lines)]
                    end_str_index: list = [substr.start() for substr in re.finditer('”', lines)]
                    lines_temp: str = ""  # 用于存放换行后的字符
                    for i in range(len(start_str_index)):
                        # 开始检查
                        is_find = False
                        star_index = start_str_index[i + 1] if i < int(len(start_str_index) - 1) else -1
                        for end_str in Template.talk_str_by_end_double_quotes.value:
                            if star_index == -1:
                                # -1 表示在当前的结束双引号后没有开始双引号了，这是最后一句话类。
                                if lines[end_str_index[i]:].find(end_str) == 1:
                                    # 表示找到了，那么就不能换行
                                    is_find = True
                            else:
                                if lines[end_str_index[i]:star_index].find(end_str) == 1:
                                    # 表示找到了，那么就不能换行
                                    is_find = True
                        if lines[:1] == "“" and lines.count("“") == 1:
                            # 如果是以双引号开头的，并且这一行只有一组双引号，那么就在中间不换行了。应该这大概率是说话的词语在双引号之后。
                            lines_temp = lines + '\n'
                        elif is_find is False:
                            # 说明还是没找到
                            if i == 0:
                                # 说明是开始循环第一遍
                                lines_temp = lines_temp + lines[:end_str_index[
                                                                     i] + 1] + '\n' if star_index != -1 else lines_temp + lines[
                                                                                                                          :
                                                                                                                          end_str_index[
                                                                                                                              i] + 1] + '\n' + lines[
                                                                                                                                               end_str_index[
                                                                                                                                                   i] + 1:]
                            elif star_index == -1:
                                # 说明循环到了最后面
                                lines_temp = lines_temp + lines[
                                                          end_str_index[i - 1] + 1:end_str_index[i] + 1] + '\n' + lines[
                                                                                                                  end_str_index[
                                                                                                                      i] + 1:]
                            else:
                                lines_temp = lines_temp + lines[end_str_index[i - 1] + 1:end_str_index[i] + 1] + '\n'
                        else:
                            # 说明找到了啊，那就不换行了
                            if i == 0:
                                # 说明是开始循环第一遍
                                lines_temp = lines_temp + lines[:end_str_index[
                                                                     i] + 1] if star_index != -1 else lines_temp + lines
                            elif star_index == -1:
                                # 说明循环到了最后面
                                lines_temp = lines_temp + lines[end_str_index[i - 1] + 1:end_str_index[i] + 1] + lines[
                                                                                                                 end_str_index[
                                                                                                                     i] + 1:]
                            else:
                                lines_temp = lines_temp + lines[end_str_index[i - 1] + 1:end_str_index[i] + 1]
                    if lines_temp != "":
                        for li in lines_temp.split('\n'):
                            if li != "":
                                result_list.append(li)
                    else:
                        result_list.append(lines)
                else:
                    # 说明没有双引号,那这句话就不要判断了
                    result_list.append(lines)
            else:
                result_list.append(lines)
        return result_list

    @staticmethod
    def format_merge_list(content_list: list) -> str:
        """
        将数组合并
        :param content_list:
        :return:
        """
        content: str = ""
        for i_str in content_list:
            if " " in i_str:
                i_str = i_str.replace(" ", "")
            content = content + i_str + '\n\r'
        return content

    @staticmethod
    def check_any_element(content: str, iterable: list[str]) -> str:
        """
        检查文本中是否存在某个字符
        """
        for i_str in iterable:
            if i_str in content:
                return i_str
        return ""

    def check_end_element(self, content: str, iterable: list[str]) -> bool:
        """
        检查某个字符是否处于文本内容的结尾处
        """
        check_str: str = self.check_any_element(content, iterable)
        if (len(content) - len(check_str)) - content.rfind(check_str) == 0:
            return True
        return False

    def check_start_element(self, content: str, iterable: list[str]) -> bool:
        """
        检查某个字符是否处于文本内容的开始处
        """
        check_str: str = self.check_any_element(content, iterable)
        if content.find(check_str) == 0:
            return True
        return False

    def split_str_by_end_str_for_line(self, content: str):
        """
        根据结束双引号切一次
        """

    @staticmethod
    def split_str_in_line(content: str, check_str: str, left_list: list[int], right_list: list[int]) -> str:
        """
        检查该字符是否在双引号之中。如果不在就换行
        请确保传入的content最多只有一句对话
        """
        left_num: int = 0 if len(left_list) == 0 else left_list[-1]
        right_num: int = 0 if len(right_list) == 0 else right_list[-1]
        if left_num == 0:
            if right_num == 0:
                # 没有开始符也没有结束符合。那就全部换行
                content = content.replace(check_str, check_str + '\n')
        else:
            if right_num > 0:
                # 有开始符和结束符，那就需要来判断一下了。
                check_str_list_num: list[int] = [substr.start() for substr in
                                                 re.finditer(check_str, content)]  # 查询开始字符串所有的index
                for i in range(len(check_str_list_num)):
                    check_str_list: list[int] = [substr.start() for substr in re.finditer(check_str, content)]
                    right_last_num = content.rfind('”')
                    if check_str_list[i] < right_last_num:
                        content = re.sub(content[:check_str_list[i] + 1], content[:check_str_list[i] + 1] + '\n',
                                         content)
        return content

    @staticmethod
    def split_by_line_feed(content: list) -> list:
        """
        按照换行符进行数组切割
        :return:
        """
        content_list = []
        for line in range(len(content)):
            content_list_all = content[line].split("\n")
            for i in range(len(content_list_all)):
                if content_list_all[i] != "":
                    content_list.append(content_list_all[i])
        return content_list if len(content) > 0 else [content]

    def split_by_end_str(self, content: list) -> list:
        """
        按照代表结束的标点符合再切一次
        """
        content_str = ""
        for line in content:
            left_list, right_list = self.check_double_quotes_left_right_str(line)
            for end_str in self.wrap_character_by_line:
                if end_str in line:
                    line = self.split_str_in_line(line, end_str, left_list, right_list)
                    if self.check_end_element(line, [end_str]):
                        # 如果这个字符已经是最后一个了，那么就不换行了
                        continue
                    line = line.replace(end_str, end_str + '\n')
            content_str = content_str + line + '\n'
        if content_str != "":
            return content_str.split('\n')
        return content

    def format_end_str(self, content_list: list) -> list:
        """
        检查每一行的结束是否有结束符号
        :param content_list:
        :return:
        """
        start_wrap_character = self.wrap_character_by_line
        result_list: list = []
        temp_str: str = ""  # 用于存放临时字符的
        for line in content_list:
            if any(wrap_str in line[-1:] for wrap_str in start_wrap_character):
                if self.check_str_is_line(temp_str + line):
                    r_list = FormatCommon().line_feed_format(temp_str + line)
                    for s in range(len(r_list)):
                        result_list.append(r_list[s])
                        temp_str = ""
                else:
                    temp_str = temp_str + line
            else:
                temp_str = temp_str + line
        if temp_str != "":
            # 避免出现漏网之鱼
            result_list.append(temp_str)
        return result_list

    def change_word(self, content: str) -> str:
        """
        替换异常、错误字符。纠正字符
        """
        for key in self.change_str:
            if key in content:
                content = content.replace(key, self.change_str[key])
        return content

    def format_end_2_start_double_quotation_mark_by_list(self, content_list: list[str]):
        r_list: list = []
        for cc in content_list:
            rs = self.format_end_2_start_double_quotation_mark(content=cc)
            r_list.extend(rs)
        return r_list


class WrapLine(FormatCommon):
    """
    简单模式使用，单行检测是否需要换行
    """

    def format_str_by_end_str_for_line(self, content: list or str) -> list:
        """
        单行模式，处理是否需要换行。只会判断是否需要和下一行合并，不会对当前对行进行换行。
        若不需要换行就与下一行合并。
        该方法只会进行简单的判断，要求待处理的内容本身没有太大的格式问题。
        :param content: 需要处理的内容
        :return:
        """
        result_list: list = []
        result_list_s: list = []
        temp_str: str = ""  # 临时存储一下字符
        content_list: list = [content] if type(content) == str else content
        for line_num in range(len(content_list)):
            lines: str = temp_str + content_list[line_num]  # 先获取一下内容
            lines = lines.strip()  # 清楚一下前后空格
            left_list, right_list = self.check_double_quotes_left_right_str(lines)
            if lines == "":
                continue
            if any(wrap_str in lines[-1:] for wrap_str in self.wrap_character_by_line) and lines.count(
                    "“") == lines.count("”"):
                # 如果该行的最后一个字符是结束符，且该行有完整成对的的双引号，那说明这句话是OK的
                if self.check_end_element(lines, self.wrap_character_by_line) and self.check_start_element(lines,
                                                                                                           self.wrap_character_by_line):
                    # 如果这里这里只有一个标点符合，那就和上一句合并
                    result_list[-1] = result_list[-1] + lines
                    result_list_s[-1] = result_list_s[-1] + lines
                    temp_str = ""
                    continue
                if self.check_start_element(lines, self.talk_str_by_end_double_quotes) and self.check_start_element(
                        result_list[-1], ['”']):
                    # 如果这一句的开头是表示不需要结束的字符和上一句的结尾是双引号的结束符。那就和上一句合并
                    result_list[-1] = result_list[-1] + lines
                    result_list_s[-1] = result_list_s[-1] + lines
                    temp_str = ""
                    continue
                if self.check_str_is_line(lines) is True:
                    result_list.append(lines)
                    result_list_s.append(lines)
                    temp_str = ""
                    continue
                if len(left_list) == 0:
                    result_list.append(lines)
                    result_list_s.append(lines)
                    temp_str = ""
                    continue
                else:
                    if left_list[-1] < right_list[-1] and len(left_list) > 1:
                        # 如果最后一个开始双引号的下标小于结束双引号，那么这句话就OK了
                        result_list.append(lines)
                        result_list_s.append(lines)
                        temp_str = ""
                        continue
            temp_str = lines
        return self.format_end_2_start_double_quotation_mark_by_list(result_list)
