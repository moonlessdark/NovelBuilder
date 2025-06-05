from PySide6.QtCore import QThread, QWaitCondition, QMutex, Signal

from Businese.FormatMode.ClearAdString import ClearAd
from Businese.FormatMode.LineWrapFormat import LineWrap
from Businese.FormatMode.lineWrapFormatV3 import LineWrapV3
from Businese.FormatModeV2.utils import FormatStr
from Utils.dataClass import ToolBarEnum
from Utils.fileOpt import FileOpt
from Utils.tradition import tradition2simple


class ReadNovel(QThread):
    """
    读取小说内容
    """
    sin_out = Signal(str)
    sin_work_status = Signal(str)
    sin_work_status_loading = Signal(bool)

    def __init__(self):
        super().__init__()
        self.working: bool = False
        self.novel_path: str = ""

    def __del__(self):
        # 线程状态改为和线程终止
        self.working = False

    def pause(self):
        """
        线程暂停
        :return:
        """
        self.working = False

    def get_param(self, novel_path: str):
        """
        获取一下参数
        :param novel_path: 需要处理的内容
        :return:
        """
        self.working = True
        self.novel_path = novel_path

    def run(self):
        self.sin_work_status_loading.emit(True)
        if self.novel_path == "":
            self.sin_work_status.emit(f"需要读取的小说文件路径错误 {self.novel_path}")
            return False
        content = FileOpt().read_novel_file(self.novel_path)
        self.sin_out.emit(content)
        self.sin_work_status_loading.emit(False)
        return True


class ManualFormat(QThread):
    """
    手动格式化
    """
    sin_out = Signal(str)
    sin_work_status = Signal(bool)
    sin_status_bar = Signal(str, bool)
    sin_out_information = Signal(str)
    sin_out_select_error_str = Signal(str)
    sin_work_status_loading = Signal(bool)

    def __init__(self):
        super().__init__()

        self.line_wrap = LineWrapV3()
        self.line_wrap_v2 = FormatStr()
        self.working = True
        self.is_First_time = True
        self.cond = QWaitCondition()
        self.mutex = QMutex()

        self.content = ""
        self.format_mode = ""

    def __del__(self):
        # 线程状态改为和线程终止
        self.working = False
        # self.wait()

    def pause(self):
        """
        线程暂停
        :return:
        """
        self.working = False

    def start_execute_init(self):
        """
        线程开始
        :return:
        """
        self.working = True
        # self.cond.wakeAll()

    def get_param(self, format_mode: str, content: str):
        """
        获取一下参数
        :param content: 需要处理的内容
        :param format_mode: 格式化类型
        :return:
        """
        self.start_execute_init()
        self.content = content
        self.format_mode = format_mode

    def run(self) -> None:
        content = ""
        self.mutex.lock()
        import time

        try:
            self.sin_work_status_loading.emit(True)
            if self.format_mode == ToolBarEnum.format_line_warp.value:
                """
                异常换行：字符模式
                处理非段落换行。用于处理盗版小说爬去的异常换行
                如果要写加强版的话，那就是在此基础上，再判断双引号中的内容是否需要换行
                """
                # 以下内容为 预处理
                content: str = self.line_wrap.plus_str_format(self.content)
                # 开始处理
                # content_list: list = self.line_wrap.check_str_is_line(content)
                # content: str = LineWrap().format_merge_list(content_list)
                content = self.line_wrap_v2.format_str(content)
            elif self.format_mode == ToolBarEnum.format_line_warp_display_width.value:
                """
                异常换行：视觉模式
                """
                content = self.line_wrap.check_str_in_display_width(self.content)
            elif self.format_mode == ToolBarEnum.format_line_warp_tab.value:
                """
                异常换行：缩进模式
                """
                content = self.line_wrap.check_str_in_display_width_v2(self.content)
            elif self.format_mode == ToolBarEnum.remove_spaces_between_quotes.value:
                """
                去除双引号中间的异常换行
                """
                content = self.line_wrap.plus_str_remove_spaces_between_quotes(self.content)
            elif self.format_mode == ToolBarEnum.clear_ad.value:
                """
                去除广告
                """
                content = ClearAd().clear_ad_str(self.content)
                content = ClearAd().clear_html_code(content)
            elif self.format_mode == "词语纠错":
                """
                词语纠错
                """
                self.sin_out_information.emit("暂时不支持")
            elif self.format_mode == ToolBarEnum.change_lan.value:
                """
                繁简互换
                """
                content = tradition2simple(self.content)
            elif self.format_mode == ToolBarEnum.type_setting.value:
                """
                排版
                """
                content: str = self.line_wrap.first_line_tab(self.content)
        except Exception as e:
            # 打印异常信息
            self.sin_out_information.emit(str(e))
        else:
            # 如果没有触发任何异常，就返回处理后的信息
            self.sin_out.emit(content)
        finally:
            self.sin_status_bar.emit("处理结束", False)
            self.mutex.unlock()
            self.sin_work_status_loading.emit(False)
