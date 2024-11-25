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

    def format(self, cc: str):
        cc = self.replace_content(cc)
        n_list = np.array(cc.split('\n'))
        result_format_content_list = np.array([""])
        result_line_list = np.array([])
        for num in n_list:

            if (
                not num or
                len(re.findall('第.*章', num)) == 1 or
                "作者:" in num or
                "作者：" in num or
                len(re.findall(r'\d{4}年\d{1,2}月\d{1,2}日发表于', num)) == 1 or
                len(re.findall(r'\d{4}年\d{1,2}月\d{1,2}日首发于', num)) == 1 or
                num.find('----') >= 0 or
                num.find('未完待续') >= 0
            ):

                if len(result_line_list) != 0:
                    # 如果长度不为0，说明此时里面还有没有处理完的文字
                    result_format_content_list, result_line_list = self.np_pad(result_format_content_list,
                                                                               result_line_list)
                    # 如果当前为None,说明是换行符，可以正常换行。
                    result_format_content_list = np.vstack((result_format_content_list, result_line_list))
                    result_line_list.resize(0, refcheck=False)

                result_line_list = np.append(result_line_list, num)
                result_format_content_list, result_line_list = self.np_pad(result_format_content_list, result_line_list)

                # 如果当前为None,说明是换行符，可以正常换行。
                result_format_content_list = np.vstack((result_format_content_list, result_line_list))
                result_line_list.resize(0, refcheck=False)
            else:
                if len(num) == 0:
                    continue
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
        # print('\n'.join(result_content_list))
        return '\n'.join(result_content_list)

