import re

import numpy as np
from numpy.lib.arraypad import pad


class FormatStr:

    def __init__(self):
        self.str_list: list = ["，", ",",
                               ".", "。",
                               "？", "?",
                               "！", "!",
                               "”"]

    def replace_content(self, content: str):
        """
        清理一下特殊的字符
        :param content:
        :return:
        """
        for p_str in self.str_list:
            content = content.replace("\n\n\u3000\u3000"+p_str, p_str)
        return content

    @staticmethod
    def np_pad(arr1: np.ndarray, arr2: np.ndarray):
        """
        维护一下numpy长度
        :param arr1:
        :param arr2:
        :return:
        """
        if arr1.shape[-1] > len(arr2):
            padding = arr1.shape[-1] - len(arr2)
            arr2 = pad(arr2, (0, padding), 'constant', constant_values="")

        elif arr1.shape[-1] < len(arr2):
            padding = len(arr2) - arr1.shape[-1]
            arr1 = pad(arr1, (0, padding), 'constant', constant_values="")
        return arr1, arr2

    def format_str(self, content: str):
        """
        格式化一下
        :param content:
        :return:
        """
        cc = self.replace_content(content)
        n_list = np.array(cc.split('\n'))
        result_format_content_list = np.array([""])
        result_line_list = np.array([])
        for num in n_list:
            if (
                num.find('\u3000\u3000') == 0 or
                num == "\n" or
                len(re.findall(r'第{1}[0-9]{1,2}章$', num)) == 1 or
                len(re.findall(r'第[一二三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟]{1,6}章', num)) == 1 or
                len(re.findall(r'作者[:：]{1}', num)) or
                len(re.findall(r'\d{4}年\d{1,2}月\d{1,2}日发表于', num)) == 1 or
                len(re.findall(r'\d{4}年\d{1,2}月\d{1,2}日首发于', num)) == 1 or
                len(re.findall(r'\d{4}/\d{1,2}/\d{1,2}首发于', num)) == 1 or
                len(re.findall(r'\d{4}/\d{1,2}/\d{1,2}发表于', num)) == 1 or
                len(re.findall(r'是否首发[:：]{1}', num)) == 1 or
                len(re.findall(r'字数[:：]{1}', num)) == 1 or
                num.find('----') >= 0 or
                num.find('未完待续') >= 0
            ):
                # 如果不为空并且该行的前2个字符为锁进字符，那么就说明之前的内容都是一段的
                if len(result_line_list) != 0:
                    # 如果长度不为0，说明此时里面还有没有处理完的文字
                    result_format_content_list, result_line_list = self.np_pad(result_format_content_list,
                                                                               result_line_list)
                    result_format_content_list = np.vstack((result_format_content_list, result_line_list))
                    result_line_list.resize(0, refcheck=False)
            result_line_list = np.append(result_line_list, num)
        else:
            # 处理一下最后一句
            # 维护一下数组长度
            result_format_content_list, result_line_list = self.np_pad(result_format_content_list, result_line_list)

            # 如果当前为None,说明是换行符，可以正常换行。
            result_format_content_list = np.vstack((result_format_content_list, result_line_list))
            result_line_list.resize(0, refcheck=False)
        result_content_list: list = []
        for f_line in result_format_content_list:
            result = ''.join(f_line)
            if result != "":
                result_content_list.append(result)
        return '\n'.join(result_content_list)
