import os
import sys

import chardet


class FileOpt:
    """
    文件操作
    """

    @staticmethod
    def read_file_path(folder_path: str):
        """
        获取文件路径
        :param folder_path: txt存放的文件夹
        :return:
        """
        file_list = os.listdir(folder_path)
        file_list.sort(key=lambda fn: os.path.getmtime(folder_path + '/' + fn))
        return file_list

    @staticmethod
    def read_novel_file(file_path) -> str:
        """
        读取text文件
        :param file_path: txt文件的路径
        :return:
        """
        with open(file_path, "rb") as f:
            content = f.read()
        content_encode = chardet.detect(content)  # 推断一下文本内容的编码格式
        if "gb" in content_encode.get("encoding") or "GB" in content_encode.get("encoding"):
            with open(file_path, encoding="gb18030", errors="ignore") as file:
                read_content = file.read()
        elif "Windows" in content_encode.get("encoding"):
            read_content = content.decode("windows-1252")
        else:
            with open(file_path, encoding="utf-8") as file:
                read_content = file.read()
        # read_content = ClearAd().clear_html_code(html.unescape(read_content))
        return read_content

    @staticmethod
    def save_txt(content, text_path: str, text_name: str):
        text_path = text_path + '/' if '/' != text_path[-1:] else text_path
        text_name = str(text_name)
        text_name = text_name + ".txt" if ".txt" not in text_name else text_name
        if len(content) > 0:
            if type(content) == list:
                content_str = ""
                for i in range(len(content)):
                    if content[i] != "":
                        content_str = content_str + content[i] + "\r\n"
                with open(text_path + text_name, "w+", encoding="utf-8") as f:
                    f.write(content_str)
            else:
                with open(text_path + text_name, "w+", encoding="utf-8") as f:
                    f.write(content)
    @staticmethod
    def read_file(file_path: str) -> bytes:
        """
        读取文件
        :param file_path:
        :return:
        """
        with open(file_path, "rb") as f:
            content = f.read()
        return content


class PathUtil:
    """
    本模块为获取项目根路径的类，为资源文件的读写提供路径帮助
    感谢 https://www.jianshu.com/p/f7def9c58287
    """

    def __init__(self):
        # 判断调试模式
        debug_vars = dict((a, b) for a, b in os.environ.items()
                          if a.find('IPYTHONENABLE') >= 0)
        # 根据不同场景获取根目录
        if debug_vars.get("IPYTHONENABLE") == "True":
            """当前为debug运行时"""
            # self.rootPath = sys.path[2]
            self.rootPath = "./"
        elif getattr(sys, 'frozen', False):
            """当前为exe运行时"""
            self.rootPath = os.getcwd() + '/_internal/'
        else:
            """正常执行"""
            self.rootPath = sys.path[1]
        # 替换斜杠
        self.rootPath = self.rootPath.replace("\\", "/") if self.rootPath is not None else None

    def get_path_from_resources(self, file_name):
        """按照文件名拼接资源文件路径"""
        file_path = "%s/Resources/%s" % (self.rootPath, file_name)
        return file_path

    # 生成资源文件目录访问路径
    @staticmethod
    def resource_path(relative_path):
        if getattr(sys, 'frozen', False):  # 是否Bundle Resource
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath("")
        return os.path.join(base_path, relative_path)
