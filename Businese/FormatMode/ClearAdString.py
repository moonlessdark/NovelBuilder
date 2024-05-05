import re

from Businese.FormatMode.NovelString import ReadNovelString


class ClearAd:

    def __init__(self):
        self.__format_dict: dict = ReadNovelString().get_format_json()

    def clear_ad_str(self, content: str) -> str:
        """
        去除广告, 去除固定的以某个字符串开头+某个字符串结尾的广告
        :param content:
        :return:
        """
        ad_str: list = self.__format_dict.get("AdString")

        for ad_num in ad_str:
            start, end = ad_num  # 拿到广告的开头和结尾字符
            rex = start + '(.*?)' + end
            result: list = re.findall(rex, content)
            for ad_str_index in result:
                if ad_str == '':
                    continue
                else:
                    replace_str = start + ad_str_index + end
                    if '\\' in replace_str:
                        replace_str = replace_str.replace('\\', '')
                    content = content.replace(replace_str, '')
        return content

    def clear_html_code(self, content: str):
        """
        替换一些网页错误的字符串
        :param content:
        :return:
        """
        html_code_str_list: list = self.__format_dict.get("Businese")
        for code_str in html_code_str_list:
            content = content.replace(code_str, "")
        return content
