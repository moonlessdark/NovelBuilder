from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QCursor, QMouseEvent, Qt
from PySide6.QtWidgets import QVBoxLayout, QListWidget


item_split_char = " <替换为> "  # 搜索历史列表的分割字符


class SearchAndReplaceWidget(QtWidgets.QWidget):
    """
    查询和替换的小界面
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self._history_list = None
        self._items: list = []

        self.widget_is_show: bool = False

        self.setFixedSize(260, 100)

        widget_select = QtWidgets.QWidget(self)
        self.manual_input_select_text = QtWidgets.QLineEdit(widget_select)
        self.manual_input_select_text.setPlaceholderText("请输入需要查询的内容")
        self.manual_input_replace_text = QtWidgets.QLineEdit(widget_select)
        self.manual_input_replace_text.setPlaceholderText("请输入需要替换的内容")
        self.manual_button_select_text = QtWidgets.QPushButton("查询", widget_select)
        self.manual_button_replace_text = QtWidgets.QPushButton("替换", widget_select)
        self.manual_button_replace_text_all = QtWidgets.QPushButton("替换全部", widget_select)

        self.manual_button_history_input = QtWidgets.QPushButton()
        self.manual_button_history_input.setIcon(QtGui.QIcon.fromTheme("document-open-recent"))  # 尝试使用主题图标

        lay_out_select_replace_1 = QtWidgets.QVBoxLayout()
        lay_out_select_replace_1.addWidget(self.manual_input_select_text)
        lay_out_select_replace_1.addWidget(self.manual_input_replace_text)

        lay_out_select_replace_2 = QtWidgets.QHBoxLayout()
        lay_out_select_replace_2.addWidget(self.manual_button_history_input)
        lay_out_select_replace_2.addWidget(self.manual_button_select_text)
        lay_out_select_replace_2.addWidget(self.manual_button_replace_text)
        lay_out_select_replace_2.addWidget(self.manual_button_replace_text_all)
        lay_out_select_replace_2.setSpacing(2)

        lay_out_select_replace = QtWidgets.QVBoxLayout(widget_select)
        lay_out_select_replace.addLayout(lay_out_select_replace_1)
        lay_out_select_replace.addLayout(lay_out_select_replace_2)
        lay_out_select_replace.setContentsMargins(5, 5, 5, 5)

        self.manual_button_history_input.clicked.connect(self.show_select_history)        
        self._history_list = SearchHistory(self)
        self._history_list.list_widget.itemClicked.connect(self.input_item_to_search_and_replace)

    def show_select_history(self):
        """
        显示查询历史
        :return: 
        """
        self._history_list.update_search_history(self._items)
        if self._history_list.isVisible() is False:
            self._history_list.show()

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
            self.manual_input_select_text.setText(item)
        return  True

class SearchHistory(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._search_list: list = []

        self.setWindowTitle("查询历史")

        layout = QVBoxLayout()
        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        self.adjustSize()
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
            if item[-1] != "":
                str_line = item[0] + item_split_char + item[1]
            else:
                str_line = item[0]
            _item_list.append(str_line)
        self.list_widget.addItems(_item_list)  # 添加列表项

    def mouseMoveEvent(self, event: QMouseEvent):
        # 获取鼠标位置并更新widget位置
        pos = event.globalPosition().toPoint()
        self.move(pos - self.rect().center())  # 将widget的中心移动到鼠标位置
