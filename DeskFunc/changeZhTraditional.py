from zhconv import zhconv


def change_zh_traditional(content: str):
    """
    繁简互换
    :param content:
    :return:
    """
    if zhconv.issimp(content, True):
        return zhconv.convert(content, 'zh-tw')
    return zhconv.convert(content, 'zh-cn')


def full_width_to_half_width(text: str) -> str:
    result = []

    text = full_to_half(text)

    for char in text:
        code = ord(char)
        # 全角字母A-Z转换（0xFF21-0xFF3A）
        if 0xFF21 <= code <= 0xFF3A:
            result.append(chr(code - 0xFEE0))
        # 全角字母a-z转换（0xFF41-0xFF5A）
        elif 0xFF41 <= code <= 0xFF5A:
            result.append(chr(code - 0xFEE0))
        else:
            result.append(char)
    return ''.join(result)


# 定义全角到半角的映射字典
full_width_to_half_width_dict: dict = {
    '！': '!', '＂': '"', '＃': '#', '＄': '$', '％': '%',
    '＆': '&', '＇': "'", '（': '(', '）': ')', '＊': '*',
    '＋': '+', '，': ',', '－': '-', '．': '.', '／': '/',
    '０': '0', '１': '1', '２': '2', '３': '3', '４': '4',
    '５': '5', '６': '6', '７': '7', '８': '8', '９': '9',
    '：': ':', '；': ';', '＜': '<', '＝': '=', '＞': '>',
    '？': '?', '＠': '@', '［': '[', '＼': '\\', '］': ']',
    '＾': '^', '＿': '_', '｀': '`', '｛': '{', '｜': '|',
    '｝': '}', '～': '~'
}


def full_to_half(text) -> str:
    # 使用映射字典替换全角标点为半角标点
    result = ''
    for char in text:
        result += full_width_to_half_width_dict.get(char, char)
    return result
