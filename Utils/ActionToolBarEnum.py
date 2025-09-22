
from enum import Enum


class ToolBarEnum(Enum):
    """
    工具栏的显示的文案
    """
    open_file = "打开"
    save_file = "保存"
    search_replace = "查询/替换(Ctrl+F)"
    change_lan = "繁简互换"
    type_setting = '排版'
    format_line_warp_tab = "非段落换行(缩进模式)"
    check_talk_str = "对话检测(繁体)"
    merge_talk_str = "对话合并(繁体)"
    split_paragraphs = "拆分段落(繁体)"

    """
    菜单栏的文案
    """
    edit_file = "编辑"
    select_and_replace = "查询和替换"
