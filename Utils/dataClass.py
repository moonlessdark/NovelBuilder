from enum import Enum


class ToolBarEnum(Enum):
    """
    工具栏的显示的文案
    """
    open_file: str = "打开"
    save_file: str = "保存"
    change_lan: str = "繁简互换"
    type_setting: str = '排版'
    clear_ad: str = "清理广告"
    remove_spaces_between_quotes = "对话中的错误换行"
    format_line_warp: str = "非段落换行(字符模式)"
    format_line_warp_display_width: str = "非段落换行(视觉模式)"
    format_line_warp_tab: str = "非段落换行(缩进模式)"

    """
    菜单栏的文案
    """
    edit_file: str = "编辑"
    select_and_replace: str = "查询和替换"
