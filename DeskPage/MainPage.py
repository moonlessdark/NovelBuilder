from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPalette, QColor, QShortcut, QKeySequence
from PySide6.QtWidgets import QMessageBox, QGraphicsScene, QStyle

from DeskPage.PageLoading import TransparentLoadingView
from DeskPage.ReQPlainTextEdit import ZoomableTextEdit
from DeskPage.SearchAndReplacePage import SearchAndReplaceWidget, SearchHistory
from Utils.ActionToolBarEnum import ToolBarEnum


class QMainElement(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)
        self.setWindowTitle("小说排版工具")

        self.tool_bar = self.addToolBar("tool_function")  # 创建一个工具栏，并设置工具栏的标题为"mytool"
        self.tool_bar.setIconSize(QtCore.QSize(20, 20))  # 设置图标大小
        self.tool_bar.setToolButtonStyle(QtGui.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)  # 设置工具栏的按钮样式为文本在图标左侧
        self.tool_bar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)  # 当有图标时只显示图标

        # 打开文件
        self.tool_action_open_file = QtGui.QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon), ToolBarEnum.open_file.value, self)
        self.tool_bar.addAction(self.tool_action_open_file)  # 将QAction对象添加到工具栏中
        # 保存文件
        self.tool_action_save_file = QtGui.QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton), ToolBarEnum.save_file.value, self)
        self.tool_bar.addAction(self.tool_action_save_file)

        # 分割线
        self.tool_bar.addSeparator()

        # 查询/替换
        self.tool_action_search_replace = QtGui.QAction(ToolBarEnum.search_replace.value, self)
        self.tool_bar.addAction(self.tool_action_search_replace)
        self.tool_action_search_replace.triggered.connect(self.show_search)

        # 分割线
        self.tool_bar.addSeparator()

        # 繁简互换
        self.tool_action_change_zh_Traditional = QtGui.QAction(ToolBarEnum.change_lan.value, self)
        self.tool_bar.addAction(self.tool_action_change_zh_Traditional)

        # 对话符号由英文转为繁体
        self.tool_action_change_en_to_zw = QtGui.QAction(ToolBarEnum.talk_str_change.value, self)
        self.tool_bar.addAction(self.tool_action_change_en_to_zw)

        # 分割线
        self.tool_bar.addSeparator()

        # 对话合并（繁体模式下可用）
        self.tool_action_merge_stalk_str = QtGui.QAction(ToolBarEnum.merge_talk_str.value, self)
        self.tool_action_merge_stalk_str.setToolTip('如果这一行没有说完，那么就将下一段合并进来。仅限繁体文本可用')
        self.tool_bar.addAction(self.tool_action_merge_stalk_str)

        # 拆分段落（繁体模式下可用）
        self.tool_action_split_paragraphs = QtGui.QAction(ToolBarEnum.split_paragraphs.value, self)
        self.tool_action_split_paragraphs.setToolTip('将双引号之外的句号都拆分为新的一段')
        self.tool_bar.addAction(self.tool_action_split_paragraphs)

        # 检查对话符
        self.tool_action_check_stalk_str = QtGui.QAction(ToolBarEnum.check_talk_str.value, self)
        self.tool_action_check_stalk_str.setToolTip('检查文本中的错误 “ ” 符号')
        self.tool_bar.addAction(self.tool_action_check_stalk_str)

        # 分割线
        self.tool_bar.addSeparator()
        # 格式化(首行缩进模式)
        self.tool_action_format_line_warp_tab = QtGui.QAction(ToolBarEnum.format_line_warp_tab.value, self)
        self.tool_bar.addAction(self.tool_action_format_line_warp_tab)

        # 重新排版
        self.tool_action_type_setting = QtGui.QAction(ToolBarEnum.type_setting.value, self)
        self.tool_bar.addAction(self.tool_action_type_setting)


        """
        内容展示区
        """
        _widget_content = QtWidgets.QWidget(self)
        self.novel_edit_print = ZoomableTextEdit(self)
        self.novel_edit_print.setPlaceholderText("等待加载小说内容")
        self.novel_edit_print.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)

        palette = QPalette()
        palette.setColor(QtGui.QPalette.ColorRole.Base, QColor('#333333'))  # 设置背景色为 淡黑色
        palette.setColor(QtGui.QPalette.ColorRole.Text, QColor('white'))  # 设置文字颜色为白色
        palette.setColor(QtGui.QPalette.ColorRole.PlaceholderText, QColor('white'))  # 设置背景文字颜色为白色
        self.novel_edit_print.setPalette(palette)

        self.setCentralWidget(_widget_content)  # 设置为中央部件

        """
        布局一下
        """
        _lay_out_main_gui = QtWidgets.QVBoxLayout(_widget_content)
        _lay_out_main_gui.addWidget(self.novel_edit_print)
        _lay_out_main_gui.setContentsMargins(5, 5, 5, 5)
        """
        查询、替换小窗口
        """
        self.widget_search = SearchAndReplaceWidget(self)
        self.dock = QtWidgets.QDockWidget('查询/换行', self)
        self.dock.setAllowedAreas(QtCore.Qt.DockWidgetArea.AllDockWidgetAreas)
        self.dock.setWidget(self.widget_search)
        self.dock.setFloating(True)  # 独立于主窗口之外
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        self.dock.setVisible(False)

        # 信号槽
        self.widget_search.manual_button_select_text.clicked.connect(self.manual_select_str)
        self.widget_search.manual_button_replace_text.clicked.connect(self.manual_replace_str)
        self.widget_search.manual_button_replace_text_all.clicked.connect(self.manual_replace_str_all)

        """
        设置快捷键
        """
        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self.show_search)

        """
        加载中效果
        """
        self._loading_view = TransparentLoadingView(_widget_content)
        self.show_loading(False)  # loading窗口默认不显示

    def show_search(self):
        """
        显示 查询/替换窗口
        :return:
        """
        self.dock.setVisible(True)

    def show_loading(self, is_show: bool):
        """
        显示加载中窗口
        :return:
        """
        if is_show:
            self._loading_view.show()
        else:
            self._loading_view.hide()

    def print_content(self, content: str):
        """
        显示小说内容
        :param content:
        :return:
        """

        self.novel_edit_print.clear()
        self.novel_edit_print.setPlainText(content)

    def get_content(self) -> str:
        """
        获取内容
        :return:
        """
        return self.novel_edit_print.toPlainText()

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

    def manual_select_str(self):
        """
        实现查询功能
        :return:
        """
        select_str = self.widget_search.manual_input_select_text.text()
        if select_str is not None and select_str != "" and type(select_str) is str:
            search_result: bool = self.novel_edit_print.find(select_str)
            if search_result:
                # 将查询内容加入到搜索历史
                self.widget_search.update_search_history_items([select_str, ""])
        else:
            self.print_information("请输入查询内容")

    def manual_replace_str(self):
        """
        替换信息
        # 代码参考 https://blog.csdn.net/hw5230/article/details/128907777
        :return:
        """
        select_str: str = self.widget_search.manual_input_select_text.text()
        replace_str: str = self.widget_search.manual_input_replace_text.text()
        content: str = self.get_content()

        if select_str == "":
            self.print_information("查询条件不能为空")
        elif content == "":
            self.print_information("还未加载待处理的内容")
        else:
            selected_str: str = self.novel_edit_print.textCursor().selectedText()  # 已经被光标选中的字符
            if selected_str == select_str:
                # 光标选中的的确是查询到的内容
                self.novel_edit_print.insertPlainText(replace_str)
                self.widget_search.update_search_history_items([select_str, replace_str])
            else:
                self.manual_select_str()

    def manual_replace_str_all(self):
        """
        一次性替换所有
        :return:
        """
        select_str: str = self.widget_search.manual_input_select_text.text()
        replace_str: str = self.widget_search.manual_input_replace_text.text()
        content: str = self.get_content()

        if replace_str is None:
            replace_str = ""

        if select_str == "":
            self.print_information("查询条件不能为空")
        elif content == "":
            self.print_information("还未加载待处理的内容")
        else:
            content = content.replace(select_str, replace_str)
            self.novel_edit_print.clear()

            if "\\n" in content:
                content_list: list = content.split('\\n')
                content = "\n".join(content_list)
            self.novel_edit_print.setPlainText(content)
            self.widget_search.update_search_history_items([select_str, replace_str])

    def highlight_text(self, position: int):

        cursor = QtGui.QTextCursor(self.novel_edit_print.document())
        cursor.setPosition(position)
        
        # line_number = cursor.blockNumber() + 1  # 行号从1开始计数
        # column_number = position - cursor.block().position()  # 列号计算，从行首算起
        # print(f"行号: {line_number}, 列号: {column_number}")

        # 将光标移动到这个位置以显示给用户
        self.novel_edit_print.setTextCursor(cursor)
        self.novel_edit_print.centerCursor()

        # 查询这一行的文字
        _text_str: str = self.novel_edit_print.toPlainText()
        _line_end_index: int = _text_str[position-1:].find("\n")
        # 选择指定长度的文本
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Right, QtGui.QTextCursor.MoveMode.KeepAnchor, _line_end_index+1)

        # 设置文本格式（例如，背景色为黄色）
        _format_str = QtGui.QTextCharFormat()
        _format_str.setForeground(QtCore.Qt.GlobalColor.yellow)
        cursor.setCharFormat(_format_str)

    def resizeEvent(self, event):
        # 获取窗口新尺寸并重新更新loading窗口大小
        new_size = event.size()
        # print(f"宽度: {new_size.width()}, 高度: {new_size.height()}")
        self._loading_view.resize(new_size)
