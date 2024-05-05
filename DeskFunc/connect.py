import os

from PySide6 import QtGui, QtCore
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QFileDialog, QMessageBox

from DeskPage.NovelFormatGUI import QMainElement
from Utils.dataClass import ToolBarEnum

from DeskFunc.Qth import ReadNovel as ReadNovelQth, ManualFormat as ManualFormatQth


class MainFunc(QMainElement):

    def __init__(self):
        super().__init__()
        self.file_items_dict = {}  # 选中的文件列表

        self.read_novel_qth = ReadNovelQth()
        self.manual_format_qth = ManualFormatQth()

        """
        菜单栏关联方法
        """
        # 连接QAction对象的触发事件和触发打开文件方法
        self.menu_action_file_open.triggered.connect(self.__load_text_list)
        self.menu_action_file_save.triggered.connect(self.__format_manual_save_item_clicked_novel_content)

        self.menu_action_file_edit.triggered.connect(self.load_dock_select_replace)

        """
        工具栏关联方法
        """
        # 连接工具栏中QAction对象的触发事件和触发工具栏方法
        self.tool_bar.actionTriggered[QtGui.QAction].connect(self.tool_bar_func)
        """
        按钮触发
        """
        # 选中小说并显示内容
        self.manual_file_item_list.itemClicked.connect(self.__format_manual_show_item_clicked_novel_content)
        self.manual_button_select_text.clicked.connect(self.manual_select_str)
        self.manual_button_replace_text.clicked.connect(self.manual_replace_str)
        self.manual_button_replace_text_all.clicked.connect(self.manual_replace_str_all)

        """
        Qth连接
        """
        self.read_novel_qth.sin_out.connect(self.print_content)
        self.read_novel_qth.sin_work_status.connect(self.show_message_to_status_bar)
        self.read_novel_qth.sin_work_status_loading.connect(self.setup_loading_label)
        self.manual_format_qth.sin_out.connect(self.print_content)
        self.manual_format_qth.sin_out_information.connect(self.print_novel_error_information)
        self.manual_format_qth.sin_out_select_error_str.connect(self.manual_select_str)
        self.manual_format_qth.sin_work_status_loading.connect(self.setup_loading_label)

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
            self.__load_text_list()
        elif option.text() == ToolBarEnum.save_file.value:
            """
            保存文件
            """
            self.__format_manual_save_item_clicked_novel_content()
        else:
            """
            繁简互换,换行，清除广告
            """
            novel_content: str = self.novel_edit_print.toPlainText()
            self.manual_format_qth.get_param(option.text(), novel_content)
            self.manual_format_qth.start()

    def __load_text_list(self):
        """
        加载小说列表
        :return:
        """
        def get_download_path():
            """
            Returns the default downloads path for linux or windows
            source:https://www.cnpython.com/qa/59995
            """
            if os.name == 'nt':
                import winreg
                sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
                downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as keys:
                    location = winreg.QueryValueEx(keys, downloads_guid)[0]
                    self.down_novel_save_path = location
            else:
                self.down_novel_save_path = os.path.join(os.path.expanduser('~'), 'downloads')
            return self.down_novel_save_path

        file_items_tuple: tuple[list[str], str] = QFileDialog.getOpenFileNames(self, caption="请选择需要处理的文件",
                                                                               dir=get_download_path(),
                                                                               selectedFilter="Text Files (*.txt);"
                                                                                              "XML Files (*.xml)")
        file_items = file_items_tuple[0]
        if len(file_items) > 0:
            self.file_items_dict = {}
            self.manual_file_item_list.clear()
            for i in file_items:
                i_index = i.rfind("/")
                self.file_items_dict[i[i_index + 1:]] = i[:i_index + 1]
            for key in self.file_items_dict:
                self.manual_file_item_list.addItem(key)

    def setup_loading_label(self, is_visible: bool):
        """
        显示加载效果
        :param is_visible:
        :return:
        """

        if is_visible:
            self.loading_label.setVisible(True)
            # 开始播放GIF动画
            self.movie.start()
            # 将标签置于顶层
            self.loading_label.setFixedSize(self.width(), self.height())
            self.loading_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        else:
            self.movie.stop()
            self.loading_label.setVisible(False)

    def print_novel_error_information(self, error_str):
        """
        用于打印处理小说时的错误信息提示
        """
        message = QMessageBox(self)
        # 设置消息框最小尺寸
        message.setMinimumSize(700, 200)
        message.setWindowTitle("处理信息")
        # 设置文字
        message.setText(str(error_str))
        # 设置信息性文字
        message.setInformativeText("该内容附近有错误信息")
        # 控制消息框类型以改变图标
        message.setIcon(QMessageBox.Icon.Warning)
        message.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        # 设置默认按钮，会被默认打开或突出显示
        message.setDefaultButton(QMessageBox.StandardButton.Ok)

        # 将消息框弹出，返回用户的选择
        ret = message.exec()

        if ret == QMessageBox.StandardButton.Ok:
            pass
        else:
            pass

    def print_information(self, error_str):
        """
        用于弹窗信息
        :param error_str:
        :return:
        """
        message = QMessageBox(self)
        # 设置消息框最小尺寸
        message.setMinimumSize(700, 200)
        message.setWindowTitle("处理信息")
        # 设置文字
        message.setText(str(error_str))
        # 控制消息框类型以改变图标
        message.setIcon(QMessageBox.Icon.NoIcon)
        message.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        # 设置默认按钮，会被默认打开或突出显示
        message.setDefaultButton(QMessageBox.StandardButton.Ok)

        # 将消息框弹出，返回用户的选择
        ret = message.exec()

        if ret == QMessageBox.StandardButton.Ok:
            pass
        else:
            pass

    def manual_select_str(self, select_str: str = None):
        """
        实现查询功能
        :return:
        """
        if select_str is None or select_str is False:
            select_str: str = self.manual_input_select_text.text()
        if select_str != "" and type(select_str) is str:
            search_result: bool = self.novel_edit_print.find(select_str)
            # if search_result:
            #     self.print_status_bar("已经查询到结果")
            # else:
            #     self.print_status_bar("没有查询到结果")
        else:
            self.print_information("查询参数异常，请Dbug代码")

    def manual_replace_str(self):
        """
        替换信息
        # 代码参考 https://blog.csdn.net/hw5230/article/details/128907777
        :return:
        """
        select_str: str = self.manual_input_select_text.text()
        replace_str: str = self.manual_input_replace_text.text()
        content: str = self.novel_edit_print.toPlainText()
        if select_str == "":
            self.print_information("查询条件不能为空")
        elif content == "":
            self.print_information("还未加载待处理的内容")
        else:
            selected_str: str = self.novel_edit_print.textCursor().selectedText()  # 已经被光标选中的字符
            if selected_str == select_str:
                # 光标选中的的确是查询到的内容
                self.novel_edit_print.insertPlainText(replace_str)
                # self.print_status_bar("内容已经修改")
            else:
                self.manual_select_str()

    def manual_replace_str_all(self):
        """
        一次性替换所有
        :return:
        """
        select_str: str = self.manual_input_select_text.text()
        replace_str: str = self.manual_input_replace_text.text()
        content: str = self.novel_edit_print.toPlainText()
        if select_str == "":
            self.print_information("查询条件不能为空")
        elif content == "":
            self.print_information("还未加载待处理的内容")
        else:
            content = content.replace(select_str, replace_str)
            self.novel_edit_print.clear()
            self.novel_edit_print.setPlainText(content)
            # self.print_status_bar("已经全部处理完")

    def print_content(self, content: str):
        """
        打印小说内容
        :param content:
        :return:
        """
        self.novel_edit_print.clear()
        if self.novel_edit_print.isEnabled() is False:
            self.novel_edit_print.setEnabled(True)  # 启用
        if self.novel_edit_print.isReadOnly() is False:
            self.novel_edit_print.setReadOnly(False)  # 允许编辑
        self.novel_edit_print.setPlainText(content + '\n')

    def __format_manual_show_item_clicked_novel_content(self):
        """
        显示选中的小说
        :return:
        """
        item = self.manual_file_item_list.selectedItems()[0]
        item_path: str = self.file_items_dict.get(item.text())
        file_path = item_path + item.text()
        self.trigger_open_file(item.text())

        self.read_novel_qth.get_param(file_path)
        self.read_novel_qth.start()

        self.novel_edit_print.moveCursor(QTextCursor.Start)

    def __format_manual_save_item_clicked_novel_content(self):
        """
        保存已处理的小说
        :return:
        """
        content: str = self.novel_edit_print.toPlainText()
        if self.manual_file_item_list.selectedItems():
            item = self.manual_file_item_list.selectedItems()[0]
            item_path: str = self.file_items_dict.get(item.text())
            file_path = item_path + item.text()
            with open(file_path, "w+", encoding="utf-8") as f:
                f.write(content)
                self.show_message_to_status_bar("文件 %s 已更新" % item.text())
        else:
            self.show_message_to_status_bar("还未选中需要保存的文件")

    def format_manual_save_other_path(self):
        """
        文件另存为
        :return:
        """
        content: str = self.novel_edit_print.toPlainText()
        if self.manual_file_item_list.selectedItems():
            save_novel_path = QFileDialog.getExistingDirectory(None, '设置结果文件目录', os.getcwd())
            if save_novel_path != "":
                save_file_path = save_novel_path + '/' + self.manual_file_item_list.selectedItems()[0].text()
                with open(save_file_path, "w+", encoding="utf-8") as f:
                    f.write(content)
                    self.show_message_to_status_bar("文件 %s 已保存至 %s 路径下" % (
                        self.manual_file_item_list.selectedItems()[0].text(), save_novel_path))
        else:
            self.show_message_to_status_bar("还未选中需要另存的文件")

    def trigger_open_file(self, file_name: str):
        self.status.showMessage(f"打开文件{file_name}")  # 在状态栏上显示信息"打开文件xxx.txt"，持续时间为0

    def trigger_save_file(self):
        self.status.showMessage("正在保存文件...", 5000)  # 在状态栏上显示信息"正在保存文件..."，持续时间为5000

    def show_message_to_status_bar(self, text: str):
        """
        在状态栏显示日志
        :param text:
        :return:
        """
        self.status.showMessage(text)
        self.setup_loading_label(False)
