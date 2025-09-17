import os
import chardet

from PySide6 import QtGui
from PySide6.QtWidgets import QFileDialog

from DeskFunc.ChapterPunctuation import check_quotes_match
from DeskPage.MainPage import QMainElement
from DeskConnect.func_qth import ManualFormat
from Utils.ActionToolBarEnum import ToolBarEnum


class ConnectFunc(QMainElement):

    def __init__(self):
        super().__init__()

        self.qth_format = ManualFormat()
        # 信号槽
        self.qth_format.sin_out.connect(self.print_content)  # 打印处理后的内容
        self.tool_bar.actionTriggered[QtGui.QAction].connect(self.tool_bar_func)
        self.qth_format.sin_out_select_error_str.connect(self.highlight_text)

        # 打开本地文件时的路径
        self.local_file_path: str = ""

    def tool_bar_func(self, option):
        """
        工具栏方法
        :param option 操作名称
        :return:
        """
        if option.text() == ToolBarEnum.open_file.value:
            """
            打开文件
            """
            self.__format_manual_show_item_clicked_novel_content()
        elif option.text() == ToolBarEnum.save_file.value:
            """
            保存文件
            """
            self.__format_manual_save_item_clicked_novel_content()
        else:
            """
            繁简互换,换行，清除广告
            """
            novel_content: str = self.get_content()
            self.qth_format.get_param(option.text(), novel_content)
            self.qth_format.start()

    def __format_manual_save_item_clicked_novel_content(self):
        """
        保存已处理的小说
        :return:
        """
        _content: str = self.get_content()
        if _content == "":
            self.print_information("没有需要保存的内容!")

        elif self.local_file_path == "":
            # 没有打开过文件，执行另存为到逻辑
            self.format_manual_save_other_path()
        else:
            with open(self.local_file_path, "w") as file:
                file.write(_content)
            self.print_information("文件内容已更新!")

    def format_manual_save_other_path(self):
        """
        文件另存为
        :return:
        """
        _content: str = self.get_content()
        filename, _ = QFileDialog.getSaveFileName(None, "文件另存为", "", "All Files (*)")
        if filename != "":
            if ".txt" not in filename:
                filename = filename + '.txt'
            with open(filename, "w+", encoding="utf-8") as f:
                f.write(_content)
            self.print_information("文件已经保存")
        else:
            self.print_information("取消保存文件")

    def __format_manual_show_item_clicked_novel_content(self):
        """
        显示选中的小说
        :return:
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*);;文本文件 (*.txt)")
        if file_name != "":
            self.local_file_path = file_name

            with open(self.local_file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']

            with open(self.local_file_path, 'r', encoding=encoding, errors='replace') as file:
                content: str = file.read()
                # check_quotes_match(content)
                self.print_content(content)
        self.novel_edit_print.moveCursor(QtGui.QTextCursor.MoveOperation.Start)  # 光标移动到第一个位置
        _print_str: str = file_name.split("/")[-1]
        self.setWindowTitle(f"当前打开: {_print_str}")
