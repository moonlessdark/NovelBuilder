from PySide6.QtCore import QThread, QWaitCondition, QMutex, Signal

from DeskFunc.ChapterPunctuation import check_double_quotation_marks
from DeskFunc.changeZhTraditional import change_zh_traditional, full_width_to_half_width
from DeskFunc.formatString import LineWrap
from Utils.ActionToolBarEnum import ToolBarEnum


class ManualFormat(QThread):
    """
    手动格式化
    """
    sin_out = Signal(str)
    sin_work_status = Signal(bool)
    sin_status_bar = Signal(str, bool)
    sin_out_information = Signal(str)
    sin_out_select_error_str = Signal(int)
    sin_work_status_loading = Signal(bool)

    def __init__(self):
        super().__init__()

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

    def stop_execute(self):
        """
        线程暂停
        :return:
        """
        self.working = False

    def get_param(self, format_mode: str, content: str):
        """
        获取一下参数
        :param content: 需要处理的内容
        :param format_mode: 格式化类型
        :return:
        """
        self.working = True
        self.content = content
        self.format_mode = format_mode

    def run(self) -> None:
        content = ""
        _error_str_num: int = -1
        self.mutex.lock()

        try:
            self.sin_work_status_loading.emit(True)

            if self.format_mode == ToolBarEnum.format_line_warp_tab.value:
                """
                异常换行：缩进模式
                """
                content = LineWrap().check_str_in_display_width_func_new(self.content)
            elif self.format_mode == ToolBarEnum.change_lan.value:
                """
                繁简互换
                """
                content = change_zh_traditional(self.content)
            elif self.format_mode == ToolBarEnum.type_setting.value:
                """
                排版
                """
                content = full_width_to_half_width(self.content)
                content: str = LineWrap().first_line_tab(content)
            elif self.format_mode == ToolBarEnum.check_talk_str.value:
                """
                检查对话
                """
                _error_str_num: int = check_double_quotation_marks(self.content)
                if _error_str_num == -1:
                    self.sin_out_information.emit("检测结束")
            elif self.format_mode == ToolBarEnum.merge_talk_str.value:
                """
                对话合并
                """
                content: str = LineWrap().merge_period_outside_quotes(self.content)
            elif self.format_mode == ToolBarEnum.split_paragraphs.value:
                """
                拆分段落
                """
                content: str = LineWrap().newline_after_period_outside_quotes(self.content)
            elif self.format_mode == ToolBarEnum.talk_str_change.value:
                """
                对话符转换,英语转繁体。
                只有内容中没有 中文的 “”，只有英文的 ""，才进行转换
                """
                content: str = LineWrap().talk_str_en_to_zw(self.content)

        except Exception as e:
            # 打印异常信息
            self.sin_out_information.emit(str(e))
        else:
            # print(f"_error_str_num:{_error_str_num}")
            if _error_str_num != -1:
                # 不等于-1，表示有异常 “” 符号，需要显示一下
                self.sin_out_select_error_str.emit(_error_str_num)
            else:
                _content = content if content != "" else self.content
                # 如果没有触发任何异常，就返回处理后的信息
                self.sin_out.emit(_content)
        finally:
            self.sin_status_bar.emit("处理结束", False)
            self.mutex.unlock()
            self.sin_work_status_loading.emit(False)
