import dataclasses
import json
import os

from Businese.file_opt import PathUtil, FileOpt


@dataclasses.dataclass
class WebSiteNovelTempXpathDataClass:
    """
    加载小说爬虫的xpath
    """
    novel_content_xpath: str
    next_page_name_xpath: str
    next_page_url_xpath: str
    novel_page_name_xpath: str
    novel_title_xpath: str


@dataclasses.dataclass
class WebSiteComicTempXpathDataClass:
    """
    加载小说爬虫的xpath
    """
    comic_content_xpath: str
    next_page_url_xpath: str


@dataclasses.dataclass
class DoubleQuotationMarksIndexList:
    left_marks_index_list: list
    right_marks_index_list: list


class ReadNovelString:

    def __init__(self):
        self.__format_dict = None
        self.__website_dict = None

        path_util = PathUtil()
        file_opt = FileOpt()

        self.format_dict_path: str = path_util.get_path_from_resources("format_novel_dict.json")
        self.website_dict_path: str = path_util.get_path_from_resources("website_novel_dict.json")

        if os.path.exists(self.format_dict_path) and os.path.isfile(self.format_dict_path):
            format_dict_str: bytes = file_opt.read_file(self.format_dict_path)
            self.__format_dict: dict = dict(json.loads(format_dict_str))
        if os.path.exists(self.website_dict_path) and os.path.isfile(self.website_dict_path):
            website_dict_str: bytes = file_opt.read_file(self.website_dict_path)
            self.__website_dict: dict = dict(json.loads(website_dict_str))

    def get_website_json(self) -> dict:
        """
        获取网页爬虫对象
        :return:
        """
        return self.__website_dict

    def get_format_json(self) -> dict:
        """
        获取格式化对象
        :return:
        """
        return self.__format_dict


class ReadComicString:

    def __init__(self):
        self.__website_dict = None

        path_util = PathUtil()
        file_opt = FileOpt()

        self.website_dict_path: str = path_util.get_path_from_resources("website_comic_dict.json")

        if os.path.exists(self.website_dict_path) and os.path.isfile(self.website_dict_path):
            website_dict_str: bytes = file_opt.read_file(self.website_dict_path)
            self.__website_dict: dict = dict(json.loads(website_dict_str))

    def get_website_json(self) -> dict:
        """
        获取网页爬虫对象
        :return:
        """
        return self.__website_dict
