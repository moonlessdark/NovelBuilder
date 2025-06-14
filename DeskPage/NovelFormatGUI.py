import platform

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QHeaderView

from DeskPage.QprintTable import CustomTableModel
from Utils.dataClass import ToolBarEnum
from Utils.fileOpt import PathUtil


class QMainElement(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.pu = PathUtil()

        self.setMinimumSize(800, 600)
        self.setWindowTitle("NovelFormat")  # 设置窗口的标题

        if platform.system() == "Windows":
            icon_path: str = './_internal/Resources/Images/'
        else:
            icon_path: str = './Resources/Images/'
        QtCore.QDir.addSearchPath('icons', icon_path)
        self.setWindowIcon(QtGui.QIcon(self.pu.get_path_from_resources('file.png')))

        self.main_widget = QtWidgets.QWidget(self)  # 创建一个QWidget对象作为中央部件
        self.setCentralWidget(self.main_widget)  # 将中央部件设置为main_widget

        """
        创建菜单栏
        """
        menu_bar = self.menuBar()  # 创建一个菜单栏
        menu_file = menu_bar.addMenu("文件")  # 在菜单栏上添加一个菜单名为"文件"

        self.menu_action_file_open = QtGui.QAction(ToolBarEnum.open_file.value, self)  # 创建一个QAction对象，显示文本"打开"
        self.menu_action_file_open.setShortcut("Ctrl+O")
        menu_file.addAction(self.menu_action_file_open)  # 将QAction对象添加到"文件"菜单中

        self.menu_action_file_save = QtGui.QAction(ToolBarEnum.save_file.value, self)  # 创建一个QAction对象，显示文本"保存"
        self.menu_action_file_save.setShortcut("Ctrl+S")  # 设置QAction对象的快捷键为Ctrl+S
        menu_file.addAction(self.menu_action_file_save)  # 将QAction对象添加到"文件"菜单中

        edit_file = menu_bar.addMenu("编辑")
        self.menu_action_file_edit = QtGui.QAction(ToolBarEnum.select_and_replace.value, self)
        self.menu_action_file_edit.setShortcut("Ctrl+F")
        edit_file.addAction(self.menu_action_file_edit)

        """
        创建工具栏
        """
        self.tool_bar = self.addToolBar("mytool")  # 创建一个工具栏，并设置工具栏的标题为"mytool"
        self.tool_bar.setIconSize(QtCore.QSize(20, 20))  # 设置图标大小
        self.tool_bar.setToolButtonStyle(QtGui.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)  # 设置工具栏的按钮样式为文本在图标左侧

        # self.tool_action_open_file = QtGui.QAction(QtGui.QIcon('icons:file-open.png'), ToolBarEnum.open_file.value, self)
        self.tool_action_open_file = QtGui.QAction(QtGui.QIcon(self.pu.get_path_from_resources('file-open.png')),
                                                   ToolBarEnum.open_file.value, self)

        self.tool_bar.addAction(self.tool_action_open_file)  # 将QAction对象添加到工具栏中

        # self.tool_action_save_file = QtGui.QAction(QtGui.QIcon("icons:save.png"), ToolBarEnum.save_file.value, self)
        self.tool_action_save_file = QtGui.QAction(QtGui.QIcon(self.pu.get_path_from_resources('save.png')),
                                                   ToolBarEnum.save_file.value, self)

        self.tool_bar.addAction(self.tool_action_save_file)

        # self.tool_action_change_zh_Traditional = QtGui.QAction(QtGui.QIcon("icons:change.png"), ToolBarEnum.change_lan.value, self)
        self.tool_action_change_zh_Traditional = QtGui.QAction(
            QtGui.QIcon(self.pu.get_path_from_resources('change.png')),
            ToolBarEnum.change_lan.value, self)

        self.tool_bar.addAction(self.tool_action_change_zh_Traditional)

        # self.tool_action_type_setting = QtGui.QAction(QtGui.QIcon("icons:format.svg"), ToolBarEnum.type_setting.value, self)
        self.tool_action_type_setting = QtGui.QAction(QtGui.QIcon(self.pu.get_path_from_resources('format.png')),
                                                      ToolBarEnum.type_setting.value, self)

        self.tool_bar.addAction(self.tool_action_type_setting)

        # self.tool_action_clear_ad = QtGui.QAction(QtGui.QIcon("icons:clear.png"), ToolBarEnum.clear_ad.value, self)
        self.tool_action_clear_ad = QtGui.QAction(QtGui.QIcon(self.pu.get_path_from_resources('clear.png')),
                                                  ToolBarEnum.clear_ad.value, self)

        self.tool_bar.addAction(self.tool_action_clear_ad)

        # self.tool_action_remove_spaces_between_quotes = QtGui.QAction(QtGui.QIcon("icons:format_str.png"),
        #                                                               ToolBarEnum.remove_spaces_between_quotes.value,
        #                                                               self)
        self.tool_action_remove_spaces_between_quotes = QtGui.QAction(
            QtGui.QIcon(self.pu.get_path_from_resources('format_str.png')),
            ToolBarEnum.remove_spaces_between_quotes.value,
            self)
        self.tool_bar.addAction(self.tool_action_remove_spaces_between_quotes)

        # self.tool_action_format_line_warp = QtGui.QAction(QtGui.QIcon("icons:format_str.png"), ToolBarEnum.format_line_warp.value, self)
        self.tool_action_format_line_warp = QtGui.QAction(
            QtGui.QIcon(self.pu.get_path_from_resources('format_str.png')),
            ToolBarEnum.format_line_warp.value, self)
        self.tool_bar.addAction(self.tool_action_format_line_warp)

        # self.tool_action_format_line_warp_display_width = QtGui.QAction(QtGui.QIcon("icons:format_str.png"),
        #                                                                 ToolBarEnum.format_line_warp_display_width.value,
        #                                                                 self)
        self.tool_action_format_line_warp_display_width = QtGui.QAction(
            QtGui.QIcon(self.pu.get_path_from_resources('format_str.png')),
            ToolBarEnum.format_line_warp_display_width.value,
            self)
        self.tool_bar.addAction(self.tool_action_format_line_warp_display_width)

        self.tool_action_format_line_warp_tab = QtGui.QAction(
            QtGui.QIcon(self.pu.get_path_from_resources('format_str.png')),
            ToolBarEnum.format_line_warp_tab.value,
            self)
        self.tool_bar.addAction(self.tool_action_format_line_warp_tab)

        self.status = self.statusBar()  # 创建一个状态栏,用于显示状态信息

        self.loading_label = QtWidgets.QLabel(self)

        # 设置GIF动画的路径
        self.movie = QtGui.QMovie(self.pu.get_path_from_resources("loading.gif"))  # 确保GIF文件在可执行文件同一目录下
        self.loading_label.setVisible(False)
        self.movie.setCacheMode(QtGui.QMovie.CacheMode.CacheAll)
        self.loading_label.setMovie(self.movie)
        """
        加载功能界面
        """
        self.manual_file_item_list = QtWidgets.QListWidget()

        self.manual_button_get_file_list = QtWidgets.QPushButton()
        # self.manual_button_get_file_list.setText("打开")

        self.manual_button_get_file_list.setIcon(QtGui.QIcon(self.pu.get_path_from_resources('icons:file-open.png')))
        self.manual_button_get_file_list.setFlat(True)
        # self.manual_button_get_file_list.setIconSize(QtCore.QSize(25, 25))

        self.manual_button_save_file = QtWidgets.QPushButton()
        # self.manual_button_save_file.setText("保存")

        # self.manual_button_save_file.setIcon(QtGui.QIcon('icons:save.png'))
        self.manual_button_save_file.setIcon(QtGui.QIcon(self.pu.get_path_from_resources('icons:save.png')))

        self.manual_button_save_file.setFlat(True)
        # self.manual_button_save_file.setIconSize(QtCore.QSize(25, 25))

        self.manual_button_other_save_file = QtWidgets.QPushButton()
        # self.manual_button_other_save_file.setText("另存为")

        # self.manual_button_other_save_file.setIcon(QtGui.QIcon('icons:share.png'))
        self.manual_button_other_save_file.setIcon(QtGui.QIcon(self.pu.get_path_from_resources('icons:share.png')))

        self.manual_button_other_save_file.setFlat(True)
        # self.manual_button_other_save_file.setIconSize(QtCore.QSize(25, 25))

        self.manual_button_execute_mode = QtWidgets.QPushButton()
        # self.manual_button_execute_mode.setText("开始执行")

        # self.manual_button_execute_mode.setIcon(QtGui.QIcon('icons:success.png'))
        self.manual_button_execute_mode.setIcon(QtGui.QIcon(self.pu.get_path_from_resources('icons:success.png')))

        self.manual_button_execute_mode.setFlat(True)
        # self.manual_button_execute_mode.setIconSize(QtCore.QSize(25, 25))

        widget_select = QtWidgets.QWidget()
        self.manual_input_select_text = QtWidgets.QLineEdit(widget_select)
        self.manual_input_select_text.setPlaceholderText("请输入需要查询的内容")
        self.manual_input_replace_text = QtWidgets.QTextEdit(widget_select)
        self.manual_input_replace_text.setPlaceholderText("请输入需要替换的内容")
        self.manual_button_select_text = QtWidgets.QPushButton("查询", widget_select)
        self.manual_button_replace_text = QtWidgets.QPushButton("替换", widget_select)
        self.manual_button_replace_text_all = QtWidgets.QPushButton("替换全部", widget_select)

        lay_out_select_replace_1 = QtWidgets.QVBoxLayout()
        lay_out_select_replace_1.addWidget(self.manual_input_select_text)
        lay_out_select_replace_1.addWidget(self.manual_input_replace_text)

        lay_out_select_replace_2 = QtWidgets.QHBoxLayout()
        lay_out_select_replace_2.addWidget(self.manual_button_select_text)
        lay_out_select_replace_2.addWidget(self.manual_button_replace_text)
        lay_out_select_replace_2.addWidget(self.manual_button_replace_text_all)

        lay_out_select_replace = QtWidgets.QVBoxLayout(widget_select)
        lay_out_select_replace.addLayout(lay_out_select_replace_1)
        lay_out_select_replace.addLayout(lay_out_select_replace_2)

        self.novel_edit_print = QtWidgets.QPlainTextEdit()
        self.novel_edit_print.setPlaceholderText("等待加载小说内容")
        self.novel_edit_print.setEnabled(False)  # 默认禁止，等出现内容的时候再放开
        self.novel_edit_print.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)

        palette = QPalette()
        palette.setColor(QPalette.Base, QColor('#333333'))  # 设置背景色为 淡黑色
        palette.setColor(QPalette.Text, QColor('white'))  # 设置文字颜色为白色
        palette.setColor(QPalette.PlaceholderText, QColor('white'))  # 设置背景文字颜色为白色
        self.novel_edit_print.setPalette(palette)

        self.novel_table_print = QtWidgets.QTableView()

        """
        dock widget
        """
        self.dock = QtWidgets.QDockWidget('查询/换行', self)
        self.dock.setAllowedAreas(QtCore.Qt.DockWidgetArea.AllDockWidgetAreas)
        self.dock.setWidget(widget_select)
        self.dock.setFloating(True)  # 独立于主窗口之外
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        self.dock.setVisible(False)

        self._load_main_layout()

        self.manual_file_item_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.manual_file_item_list.itemDoubleClicked.connect(self.list_widget_edit_record)

    def list_widget_del_record(self):
        """
        删除记录
        :return:
        """
        _row_index = self.manual_file_item_list.currentRow()
        self.manual_file_item_list.takeItem(_row_index)

    def list_widget_edit_record(self, item):
        # 创建一个文本编辑器来编辑条目
        text, ok = QtWidgets.QInputDialog.getText(self, '编辑条目', '请输入新的文本:', QtWidgets.QLineEdit.Normal,
                                                  item.text())
        if ok and text != '':
            # if '.txt' not in text:
            #     text = text + '.txt'
            item.setText(text)

    def _load_main_layout(self):
        """
        加载布局，左右的结构，左侧是需要处理的小说列表，右侧是内容展示区
        :return:
        """
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        splitter.addWidget(self.manual_file_item_list)
        splitter.addWidget(self.novel_edit_print)
        # splitter.addWidget(self.novel_table_print)
        splitter.setSizes([130, self.width() - 130])
        layout_opt_format_novel = QtWidgets.QHBoxLayout(self.main_widget)
        layout_opt_format_novel.addWidget(splitter)
        layout_opt_format_novel.setContentsMargins(2, 2, 2, 2)
        layout_opt_format_novel.setSpacing(1)

    def load_dock_select_replace(self):
        """
        加载查询/替换dock栏
        :return:
        """
        if self.dock.isVisible():
            self.dock.setVisible(False)
        else:
            self.dock.setVisible(True)
