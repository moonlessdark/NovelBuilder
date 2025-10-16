import os

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QMouseEvent, Qt
from PySide6.QtWidgets import QVBoxLayout, QSizePolicy

from DeskPage.FindList import ListWidgetWithMenu

item_split_char: str = " <替换为> "  # 搜索历史列表的分割字符


class SearchAndReplaceWidget(QtWidgets.QWidget):
    """
    查询和替换的小界面
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self._history_list = None
        self._items: list = []

        self.manual_input_select_text = QtWidgets.QLineEdit()
        self.manual_input_select_text.setPlaceholderText("请输入需要查询的内容")
        self.manual_input_replace_text = QtWidgets.QLineEdit()
        self.manual_input_replace_text.setPlaceholderText("请输入需要替换的内容")
        self.manual_button_select_text = QtWidgets.QPushButton("查询")
        self.manual_button_replace_text = QtWidgets.QPushButton("替换")
        self.manual_button_replace_text_all = QtWidgets.QPushButton("替换全部")

        self.manual_button_history_input = QtWidgets.QPushButton()
        self.manual_button_history_input.setIcon(QtGui.QIcon.fromTheme("document-open-recent"))  # 尝试使用主题图标

        lay_out_select_replace_1 = QtWidgets.QVBoxLayout()
        lay_out_select_replace_1.addWidget(self.manual_input_select_text)
        lay_out_select_replace_1.addWidget(self.manual_input_replace_text)
        lay_out_select_replace_1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        lay_out_select_replace_2 = QtWidgets.QHBoxLayout()
        lay_out_select_replace_2.addWidget(self.manual_button_history_input)
        lay_out_select_replace_2.addWidget(self.manual_button_select_text)
        lay_out_select_replace_2.addWidget(self.manual_button_replace_text)
        lay_out_select_replace_2.addWidget(self.manual_button_replace_text_all)
        lay_out_select_replace_2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lay_out_select_replace_2.setSpacing(2)

        self.manual_button_history_input.clicked.connect(self.show_select_history_in_main_windows)

        self._history_list = SearchHistory()
        self._history_list.list_widget.itemClicked.connect(self.input_item_to_search_and_replace)

        self._history_list_is_show: bool = False

        # 主界面布局
        self.lay_out_select_replace = QtWidgets.QVBoxLayout(self)
        self.lay_out_select_replace.addLayout(lay_out_select_replace_1)
        self.lay_out_select_replace.addLayout(lay_out_select_replace_2)
        self.lay_out_select_replace.addWidget(self._history_list)
        # lay_out_select_replace.setContentsMargins(5, 5, 5, 5)
        self.lay_out_select_replace.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._history_list.hide()

    # def show_select_history(self):
    #     """
    #     显示查询历史
    #     :return:
    #     """
    #
    #     self._history_list.update_search_history(self._items)
    #     if not self._history_list_is_show:
    #         self._history_list.show()
    #         self._history_list_is_show = True
    #         self.setMinimumHeight(300)
    #         self.resize(self.width(), self.height() + self._history_list.height())
    #     else:
    #         self._history_list.hide()
    #         self._history_list_is_show = False
    #         self.setMinimumHeight(116)
    #         self.resize(self.width(), 116)

    def show_select_history(self):
        """
        显示查询历史
        :return:
        """
        self._history_list.update_search_history(self._items)

        # 切换历史列表的显示状态
        self._history_list_is_show = not self._history_list_is_show
        self._history_list.setVisible(self._history_list_is_show)

        # 使用布局管理器的自然行为来调整尺寸
        self.lay_out_select_replace.invalidate()  # 标记布局为需要重新计算
        self.layout().activate()  # 激活布局更新

        # 延迟调整大小以确保布局完成更新
        QtCore.QTimer.singleShot(0, lambda: (
            self.adjustSize(),
            self.parentWidget().adjustSize() if self.parentWidget() else None
        ))

    def show_select_history_in_main_windows(self):
        """
        显示查询历史,在侧边栏中
        :return:
        """
        self._history_list.update_search_history(self._items)

        # 切换历史列表的显示状态
        self._history_list_is_show = not self._history_list_is_show
        self._history_list.setVisible(self._history_list_is_show)

        # 触发布局更新
        self.lay_out_select_replace.invalidate()
        self.layout().activate()

    def is_in_main_window_sidebar(self):
        """
        检查当前组件是否在主窗口的侧边栏中，并打印组件树
        :return: bool
        """
        # 打印完整的组件树
        self.print_widget_tree()

        # 您的实际判断逻辑
        parent = self.parentWidget()
        while parent:
            class_name = parent.__class__.__name__
            object_name = getattr(parent, 'objectName', lambda: '')()
            print(f"Checking parent: {class_name}, name: {object_name}")

            # 在这里添加您的具体判断条件
            # ...

            parent = parent.parentWidget()

        return False

    def print_widget_tree(self):
        """
        打印组件树结构
        """
        def _print_tree(widget, level=0):
            indent = "  " * level
            class_name = widget.__class__.__name__
            object_name = getattr(widget, 'objectName', lambda: '')()
            size = f"{widget.width()}x{widget.height()}"
            print(f"{indent}{class_name} ({object_name}) [{size}]")

            # 遍历子组件
            if hasattr(widget, 'children'):
                for child in widget.children():
                    if isinstance(child, QtWidgets.QWidget):
                        _print_tree(child, level + 1)

        print("\n=== Widget Tree ===")
        _print_tree(self)
        print("==================\n")



    def update_search_history_items(self, items):
        # print(f"_items：{self._items}，item:{items}")
        if items not in self._items:
            self._items.append(items)

    def input_item_to_search_and_replace(self, item):
        """

        :param item:
        :return:
        """
        select_str: str = item.text()
        if select_str == "" or select_str is None:
            return False

        self.manual_input_select_text.clear()
        self.manual_input_replace_text.clear()
        if item_split_char in select_str:
            _s, _r = select_str.split(item_split_char)
            self.manual_input_select_text.setText(_s)
            self.manual_input_replace_text.setText(_r)
        else:
            self.manual_input_select_text.setText(select_str)
        return True


class SearchHistory(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)

        self._search_list: list = []

        layout = QVBoxLayout()
        self.list_widget = ListWidgetWithMenu(self)
        layout.addWidget(self.list_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setWindowModality(Qt.WindowModality.WindowModal)  # 使对话框模态，防止用户在子窗口操作时操作主窗口

    def update_search_history(self, search_items: list):
        """
        更新QList中的内容
        :param search_items:
        :return:
        """
        # print(f"search_items:{search_items}")
        if len(search_items) == 0:
            return None
        self.list_widget.clear()
        _item_list: list = []
        for item in search_items:
            if item[0] == "":
                # 查询没有值，没有保存的必要
                continue
            elif item[-1] != "":
                # 查询和替换
                str_line = item[0] + item_split_char + item[1]
            else:
                # 纯查询
                str_line = item[0]
            _item_list.append(str_line)
        self.list_widget.addItems(_item_list)  # 添加列表项
        return None

    def mouseMoveEvent(self, event: QMouseEvent):
        # 获取鼠标位置并更新widget位置
        pos = event.globalPosition().toPoint()
        self.move(pos - self.rect().center())  # 将widget的中心移动到鼠标位置
