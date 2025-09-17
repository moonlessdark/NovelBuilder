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
