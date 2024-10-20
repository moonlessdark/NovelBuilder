# coding=utf-8

def is_chinese(uchar):
    '''判断一个unicode是否是汉字'''
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if u'\u0030' <= uchar <= u'\u0039':
        return True
    return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    return False


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    return False


# gbk宽度可用于对齐，中文占两个字符位置
def gbkwordlen(u):
    if is_number(u) or is_alphabet(u):
        return 1
    return 2


# 计算文本显示宽度
def gbkwordslen(uw):
    i: int = 0
    for u in uw:
        i += gbkwordlen(u)
    return i


def trunc_word(uw, len):
    l = 0
    i = 1
    for u in uw:
        l += gbkwordlen(u)
        if l > len:
            return uw[:i - 1]
        i += 1
    return uw


if __name__ == '__main__':

    a = u"kwklwkw"
    # print(trunc_word(a, 6))
    print(gbkwordslen(a))
