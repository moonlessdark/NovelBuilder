import re


class formatContent:
    """
    对一些异常换行的数据进行重新拼接为数组
    """

    is_break = False

    @staticmethod
    def format_str_by_list(string_list: list, split_str: str, content: str):
        result = []
        list_left = ""
        list_right = ""
        for i in range(len(string_list)):
            if len(result) == 0:
                """
                先处理左边的
                """
                a = "\n" + split_str
                if a not in content:
                    list_left = list_left + string_list[i]
                    result.append(list_left)
                elif a in content:
                    list_left = list_left + string_list[i] + split_str
                    if list_left.count(split_str) - list_left.count("\n" + split_str) == 1:
                        list_left.removesuffix(split_str)  # 从str的末尾切除掉 split_str
                        result.append(list_left)
            elif len(result) == 1:
                """
                再处理右边的
                """
                if 0 < i < len(string_list) - 1:
                    list_right = list_right + string_list[i] + split_str
                elif i == len(string_list) - 1:
                    list_right = list_right + string_list[i]
                    result.append(list_right)
                    break
        return result

    def remake_content_list(self, split_str: str, content: str):
        """
        重新拼接数组，一分为2，该方法用于有个相同的匹配结果时
        :param split_str:
        :param content:
        :return:
        """
        left_str_content = ""
        content_list_temp = content.split("\n")
        for i in range(len(content_list_temp) - 1):
            left_str_content = left_str_content + content_list_temp[i] + '\n'
        right_str_content_temp = content_list_temp[-1]

        # 重新把右侧的拼接好
        right_str_content_temp_list = right_str_content_temp.split(split_str)
        left_str_content = left_str_content + right_str_content_temp_list[0]
        right_str_content_temp_str = ""

        if len(right_str_content_temp_list) > 2:
            for s in range(len(right_str_content_temp_list)):
                if s == 0:
                    left_str_content = left_str_content + right_str_content_temp_list[s] + split_str
                elif s == 1:
                    left_str_content = left_str_content + right_str_content_temp_list[s]
                elif s > 1:
                    right_str_content_temp_str = right_str_content_temp_str + split_str + right_str_content_temp_list[s]
        return [left_str_content, right_str_content_temp_str]

    def check_split_str_result(self, split_string, content):
        """
        检查待处理的文本中有多少个指定的字符
        :param split_string: 需要检查的字符
        :param content: 文本内容
        :return:
        """
        split_right_content = content.split(split_string)
        right_str = ""
        for i in range(len(split_right_content)):
            if i == 1:
                right_str = split_right_content[i]
            elif i > 1:
                right_str = right_str + split_string + split_right_content[i]
        return right_str

    @staticmethod
    def clear_wrap_text(content):
        """
        清除所有的换行符
        :param content: 文本内存，utf-8格式
        :return:
        """
        pattern = re.compile('[\r\n\u2028\u2029\s]')
        return re.sub(pattern, '', content, 0)
