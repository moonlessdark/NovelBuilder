import re

from Businese.FormatMode.NovelString import ReadNovelString, DoubleQuotationMarksIndexList


class LineWrap:
    def __init__(self):
        self.format_dict: dict = ReadNovelString().get_format_json()
        self.wrap_character: list = [x for ss in self.format_dict["NovelPunctuationSymbol"]["line_end_string"].values() for x in ss.values()]
        self.left_str_list: list = [x for x in self.format_dict["NovelPunctuationSymbol"]["talk_string"]["double_quotation_marks_left"].values()]
        self.right_str_list: list = [x for x in self.format_dict["NovelPunctuationSymbol"]["talk_string"]["double_quotation_marks_right"].values()]

    @staticmethod
    def wrap_line_by_double_quotation_mark_by_str(content_str: str) -> list:
        """
        按照前后双引号，句号双引号(开始符)换行
        例如：xxx”“xxx,
             xxx」「xxx,
             xxx。“xxx
        :param content_str:
        :return:
        """
        content_str = content_str.replace("\u3000", "")
        format_str: list = ['”“', '」「', '。“']
        for key_str in format_str:
            content_str = re.sub(key_str, key_str[0] + '\n' + key_str[1], content_str)
        content_list = content_str.split("\n")
        return content_list

    @staticmethod
    def split_line_by_warp_str(content: str | list) -> list:
        """
        按照换行符进行数组切割
        :return:
        """
        content_list = []
        if type(content) == str:
            content = list[content]
        for line in content:
            line_list: list = line.split("\n")
            content_list.extend(line_list)
        return content_list if len(content_list) > 0 else content

    def merge_line(self, content_list: list[str]) -> list:
        """
        将数组合并一下
        :param content_list:
        :return:
        """
        merge_content: list[str] = []
        temp_line: str = ""
        for line_str in content_list:
            if line_str != "":
                if self.check_str_is_line(line_str):
                    merge_content.append(line_str)
                    temp_line: str = ""
                else:
                    temp_line = temp_line + line_str
        if temp_line != "":
            """
            如果最后一行了，但是没有在循环里合并，那么就合并进来把
            """
            merge_content.append(temp_line)
        return merge_content

    def check_str_is_line(self, content: str) -> bool:
        """
        检查这是否是完整的一句话。
        需要满足以下条件：
        1、是否以 句号，感叹号，分号，问号结尾，且双引号是成对的(必须符合开始结束的规则)或者为0。
        :param content: 正文
        :return:
        """
        if any(wrap_str in content[-1:] for wrap_str in self.wrap_character):
            """
            如果结尾出现了表示可以结束的符号(句号，问号，感叹号，分号，结束双引号)
            """
            if self.check_double_quotes_error_index(content) == 0:
                return True
        return False

    def check_double_quotes_error_index(self, content: str) -> int:
        """
        检查双引号，如果有异常，就返回开始的双引号的index
        :param content:
        :return: 0 开始符数量等于结束符数量。  >0的数字表示从哪个开始符开始有异常
        """
        left_list = self.get_double_quotes_left_right_str(content).left_marks_index_list
        right_list = self.get_double_quotes_left_right_str(content).right_marks_index_list
        merge_list = left_list + right_list
        merge_list.sort()
        inter_list = iter(merge_list)  # 加载为迭代器对象
        temp_left_list: list = []
        temp_right_list: list = []
        temp_left_index: int = 0  # 用于记录可能是有问题的index
        is_check_end: bool = False
        while is_check_end is False:
            """
            1、正常的双引号，应该是开始符后紧接着结束符
            2、有些特殊的说话，开始符号后依旧是开始符，但后面会紧着2个结束符
            """
            next_str_index: inter_list = next(inter_list, 0)  # 从迭代器里取值
            if temp_left_index == 0:
                temp_left_index = next_str_index
            if next_str_index == 0:
                """
                迭代器已经结束,即将结束循环
                """
                is_check_end = True
            if is_check_end is False:
                next_str = content[next_str_index]  # 拿出这个字符
                temp_left_list.append(next_str) if next_str in self.left_str_list else temp_right_list.append(next_str)

                if len(temp_left_list) == len(temp_right_list):
                    """
                    如果左表等于右表，表示双引号齐全
                    """
                    temp_left_list: list = []
                    temp_right_list: list = []
                    temp_left_index = 0
                else:
                    """
                    如果左表 != 右表，那么此时需要分情况判断了
                    """
                    if len(temp_left_list) - len(temp_right_list) == 1:
                        """
                        情况1: 左表比右表多一个字符，表示结束的符号还没循环到，这是正常的
                        """
                        continue
                    elif len(temp_left_list) > 1 and len(temp_right_list) == 0:
                        """
                        情况2: 左表连续右开始双引号，而右表始终为空，表示作者在写嵌套的双引号。
                        例如：
                            一台红色计程车内，三个男人紧盯着雨雾中锈迹斑斑的大铁门，不舍眨眼。
                            “系本台消息，今夜热带气旋“爱伦”即将抵港，10号风球已发出强烈警告…滋滋滋……皇家香港气象台……滋滋……”
                            “红鸡”副驾驶座位上，一名圆寸头的冷峻男人拿起车窗前横放的健牌香烟，用手一抖，香烟稳稳被嘴叼-住，按了几下火机，才点燃，修长的双眸掠过一抹急躁。
                        """
                        continue
                    else:
                        return temp_left_index
        return 0

    def get_double_quotes_left_right_str(self, content: str) -> DoubleQuotationMarksIndexList:
        """
        获取所有开始结束符号的下标
        :param content: 代处理的内容
        :return: 开始符的下标数组，结束符的下标数组
        """
        left_index_list: list = []
        right_index_list: list = []
        for start_str, end_str in zip(self.left_str_list, self.right_str_list):
            left_list = [sub_str.start() for sub_str in re.finditer(start_str, content)]  # 查询开始字符串所有的index
            right_list = [sub_str.start() for sub_str in re.finditer(end_str, content)]  # 查询结束字符串所有的index
            left_index_list.extend(left_list)
            right_index_list.extend(right_list)
        left_index_list.sort()
        right_index_list.sort()
        check_index_double_quotation_marks = DoubleQuotationMarksIndexList(left_index_list, right_index_list)
        return check_index_double_quotation_marks

    def check_novel_error_mark_str(self, content: str) -> str:
        """
        检查小说的双引号是否正常,返回不正常的内容
        :param content:
        :return:
        """
        result_index = self.check_double_quotes_error_index(content)
        if result_index > 0:
            re_str = content[result_index: result_index + 20]
            if "\n" in re_str:
                re_str_right = re_str[:re_str.find('\n')]
                re_str_left = re_str[re_str.find('\n'):]
                re_str = re_str_left if len(re_str_left) > len(re_str_right) else re_str_right
            return re_str.replace("\n", "").replace(" ", "")
        return ""

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
            content = content + i_str + '\n'
        return content
