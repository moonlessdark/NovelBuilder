import zhconv


def tradition2simple(hans_str: str):
    """
    Function: 将 hans_str 繁简互换
    """
    if zhconv.issimp(hans_str, True):
        return zhconv.convert(hans_str, 'zh-tw')
    return zhconv.convert(hans_str, 'zh-cn')
