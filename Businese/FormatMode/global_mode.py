# # encoding: utf-8
# import re
#
# from novel_bussinese.Tools.textToPackage import formatContent as f
# from novel_bussinese.Bussines.FormatMode.common import FormatCommon
# from novel_bussinese.template.rexp_template import Template
#
#
# class global_mode:
#
#     def __init__(self):
#         """
#         全局模式，通过大量的正则匹配来进行格式化
#         """
#         self.fc = f()
#
#     @staticmethod
#     def format_double_quotation_mark(content: str) -> list:
#         """
#         双引号之后进行切割数组，形式为  "xxxx"<换行>
#         :param content: 文本正文
#         :return:
#         """
#         a = re.findall('“([^“]*)”', content)
#         if len(a) > 0:
#             for i in a:
#                 content = re.sub(i + '”', i + '”'"\\n", content)
#         content_list: list = content.split("\n")
#         return content_list
#
#     def wrap_by_double_quotation_mark(self, content: str) -> list:
#         """
#         检查2句对话中间的句子里有没有标识符可以进行换行
#         如果纯在可以判断换行的标识符，那就在这些标识符后面进行换行
#         如果不存在换行标识符，就检查是否存在不允许换行的特殊字符，如果没有，就整句换行
#         :param content:
#         :return:
#         """
#         change_line_str = Template.wrap_character.value
#         result = re.findall("”(.*?)“", content)
#         if len(result) > 0:
#             for i in range(len(result)):
#                 str_bool = False
#                 is_split_not = 0
#                 split_string = result[i]
#                 sa = content.split(split_string)
#                 if len(sa) == 2:
#                     left_str = sa[0]
#                     right_str = sa[1]
#                 else:
#                     ah = self.fc.remake_content_list(content=content, split_str=split_string)
#                     left_str = ah[0]
#                     right_str = ah[1]
#                 temp_str = result[i]
#                 for n in change_line_str:  # 循环一下标点符号
#                     if n in temp_str:
#                         str_bool = True
#                         temp_str = re.sub(n, n + "\\n", temp_str)
#                 if str_bool is True:
#                     """
#                     存在换行符，开始换行
#                     """
#                     content = left_str + temp_str + right_str
#                 elif str_bool is False:
#                     """
#                     如果str里面没有特定的标点符号，那么执行以下操作
#                     """
#                     str_not_split = Template.talk_str.value
#                     for x in str_not_split:
#                         if split_string.find(x) != 0:
#                             """
#                             不是以数组里的字符开头的话，就可以正常换行
#                             """
#                             is_split_not += 1
#                     if is_split_not == len(str_not_split):
#                         """
#                         不能换行的字符，都不存在，那么这一行就可以加换行符了
#                         """
#                         a = split_string + right_str
#                         content = content.replace(a, "\n" + a)
#         return content.split("\n")
#
#     def format_start_str(self, content: str) -> list:
#         """
#         双引号左侧的数据，如果有以下标识符，就换行
#         :param content:
#         :return:
#         """
#         change_line_str = Template.wrap_character.value  # 句号之类的
#         while True:
#             result = re.findall("(.*?)“", content)
#             if len(result) > 0:
#                 for i in result:
#                     if i != "":
#                         split_result = content.split(i)
#                         left_result = split_result[0]
#                         right_result = split_result[1]
#                         if "了一声" not in i:
#                             if "”" in i:
#                                 n = re.sub("”", "”\\n", i)
#                                 content = left_result + n + right_result
#                             else:
#                                 for m in change_line_str:
#                                     if m in i:
#                                         i = re.sub(m, m + "\\n", i)
#                                 content = left_result + i + right_result
#             else:
#                 content_list_by_ju = re.sub("。", "。\\n", content)
#                 str_content = ""
#                 for s in content_list_by_ju:
#                     str_content = str_content + s
#                 content = str_content
#             return content.split("\n")
#
#     @staticmethod
#     def __left_index(start_str_index: list, end_str_index: list) -> list:
#         left_star_list = []
#         for ss in range(len(start_str_index)):
#             if ss == 0:
#                 x = 0
#                 y = start_str_index[ss]
#             else:
#                 x = end_str_index[ss - 1]
#                 y = start_str_index[ss]
#             left_star_list.append([x, y])
#         return left_star_list
#
#     @staticmethod
#     def __right_index(start_str_index: list, end_str_index: list) -> list:
#         right_star_list = []
#         for ssr in range(len(start_str_index)):
#             if ssr == len(start_str_index) - 1:
#                 x = end_str_index[ssr]
#                 y = -1
#             else:
#                 x = end_str_index[ssr]
#                 y = start_str_index[ssr + 1]
#             right_star_list.append([x, y])
#         return right_star_list
#
#     def wrap_by_str(self, content: list) -> list:
#         global any
#         talk_str = Template.talk_str.value
#         end_str = Template.end_str.value
#         line_content_str = ""
#         for l in content:
#             if l != '':
#                 start_str_index = [substr.start() for substr in re.finditer('“', l)]  # 得到所有的开始符
#                 end_str_index = [substr.start() for substr in re.finditer('”', l)]  # 得到所有的结束符
#                 if len(start_str_index) == len(end_str_index) and len(start_str_index) > 0:  # 说明有开始结束符，且是数量相同的
#                     c = lambda start_str_index, end_str_index: True if any(
#                         int(end_str_index[i]) > int(start_str_index[i]) for i in
#                         range(len(start_str_index))) else False  # 检查是不是开始符+结束符的排序
#                     if c(start_str_index=start_str_index, end_str_index=end_str_index) is True:
#                         # 如是结束符的下标都大于开始符的下标，这是正确的数据
#                         str_split_point = 0  # 字符串下标标记点，用于记录当前字符串已经切到那个字符
#                         for k in range(len(start_str_index)):
#
#                             left_star_list = self.__left_index(start_str_index=start_str_index,
#                                                                end_str_index=end_str_index)
#                             right_star_list = self.__right_index(start_str_index=start_str_index,
#                                                                  end_str_index=end_str_index)
#                             end_str_index_str = end_str_index[k] + 1
#                             right_check_str: str = l[right_star_list[k][0]:right_star_list[k][1]]
#                             left_check_str: str = l[left_star_list[k][0]:left_star_list[k][1]]
#                             if right_star_list[k][1] == -1:  # 到末尾了
#                                 if left_star_list[k][0] == 0:
#                                     if any(right_check_str.find(j) == 1 for j in end_str) or any(
#                                             j in right_check_str for j in talk_str):
#                                         # 说明双引号结尾的第一个字符是不需要换行的或者这里面有表示说话的
#                                         line_content_str = line_content_str + l[str_split_point:] + '\n'
#                                     else:
#                                         line_content_str = line_content_str + '\n' + l[str_split_point:end_str_index[
#                                                                                                            k] + 1] + '\n' + l[
#                                                                                                                             end_str_index[
#                                                                                                                                 k] + 1:] + '\n'
#                                 else:  # 没到末尾，说明现在是倒数第二句，让我们来看看
#                                     if any(left_check_str.find(j) == 1 for j in end_str):  # 检测右侧是否有不需要换行的字符
#                                         line_content_str = line_content_str + l[str_split_point:] + '\n'
#                                     elif any(j in left_check_str for j in talk_str):  # 开始检查开始符左侧是否有关键字
#                                         # 如果左侧有表示说话的字符，那么就从左侧换行
#                                         line_content_str = line_content_str + '\n' + l[str_split_point:end_str_index[
#                                                                                                            k] + 1] + '\n' + l[
#                                                                                                                             end_str_index[
#                                                                                                                                 k] + 1:] + '\n'
#                                     else:
#                                         line_content_str = line_content_str + l[str_split_point:] + '\n'
#                             else:
#                                 # 如果不是不是结尾的，就开始判断
#                                 if any(right_check_str.find(j) == 1 for j in end_str):  # 检测右侧是否有不需要换行的字符
#                                     # 说明第一个开头的字符是不需要换行的
#                                     line_content_str = line_content_str + l[str_split_point:end_str_index_str]
#                                     str_split_point = end_str_index_str
#                                 elif any(j in left_check_str for j in talk_str):  # 开始检查开始符左侧是否有关键字
#                                     # 如果左侧有表示说话的字符，那么就从左侧换行
#                                     line_content_str = line_content_str + '\n' + l[
#                                                                                  str_split_point:end_str_index_str] + '\n'
#                                     str_split_point = end_str_index_str
#                                 else:  # 如果左侧也没有，右侧也没有，那么就一整句之间换行
#                                     line_content_str = line_content_str + '\n' + l[str_split_point:end_str_index_str]
#                                     str_split_point = end_str_index_str
#
#                     else:
#                         line_content_str = line_content_str + '\n' + l + '\n'
#                 else:  # 不然，开始符和结束符的数量不一致或者压根没有开始结束符，说明数据异常，需要人工识别处理
#                     line_content_str = line_content_str + '\n' + l + '\n'
#         return line_content_str.split('\n')
#
#     def wrap_by_str2(self, content: list) -> list:
#         """
#         一行文字中，双引号左右2边都有内容的进行判断，检查是前面还是后面需要换行。
#         :param content:
#         :return:
#         """
#         talk_str = Template.talk_str.value
#         end_str = Template.end_str.value
#         line_content_str = ""
#         for l in content:
#             if l != '':
#                 change_line_left = False
#                 change_line_right = False
#                 l_list_left = l.split('“')
#                 l_list_right = l.split('”')
#                 if len(l_list_left) > 2:
#                     """
#                     如果查到了多条数据
#                     """
#                     start_str_index = [substr.start() for substr in re.finditer('“', l)]
#                     end_str_index = [substr.start() for substr in re.finditer('”', l)]
#                     short_list = start_str_index if len(start_str_index) < len(end_str_index) else end_str_index
#                     for index in range(len(short_list)):
#                         i = 0 if index == 0 else end_str_index[index - 1] + 1
#                         # 开始检查是否有对话
#                         sss = l[i:start_str_index[index]]
#                         if any(ss in sss for ss in talk_str):
#                             line_content_str = line_content_str + '\n' + l[i:end_str_index[index] + 1]
#                         else:
#                             # line_content_str = line_content_str + l[i:end_str_index[index] + 1]
#                             if l[i] != '”':
#                                 jj = l[end_str_index[index] + 1:end_str_index[index] + 2]
#                                 if any(j in jj for j in end_str):
#                                     line_content_str = line_content_str + l[i:end_str_index[index] + 1]
#                                 else:
#                                     line_content_str = line_content_str + '\n' + l[i:end_str_index[index] + 1] + '\n'
#                             else:
#                                 line_content_str = line_content_str + '\n' + l[i:end_str_index[index] + 1] + '\n'
#                 elif len(l_list_left) == 2:
#                     """
#                     如果刚好只有前后2条
#                     """
#                     if l_list_left[0] != '':
#                         """
#                         检查对话左侧的数据
#                         """
#                         for e in talk_str:
#                             if e in l_list_left[0]:
#                                 change_line_left = True
#                                 continue
#                     if l_list_right[1] != '':
#                         for e in talk_str:
#                             if e in l_list_right[1]:
#                                 change_line_right = True
#                         for k in end_str:
#                             """
#                             这里我们检查一下双引号后面有没有接不允许换行的字符
#                             """
#                             if l_list_right[0] == k:
#                                 change_line_right = True
#                     if change_line_left is True:
#                         """
#                         如果左侧有说话的词语右侧没有
#                         """
#                         line_str = l.replace('”', '”' + '\n')
#                         line_content_str = line_content_str + line_str + '\n'
#                     elif change_line_right is True:
#                         """
#                         如果左侧没有但右侧有
#                         """
#                         line_str = l.replace('“', '\n' + '“')
#                         line_content_str = line_content_str + line_str + '\n'
#                     else:
#                         """
#                         如果左侧和右侧都有说话的词语，或者都没有说话的词语
#                         """
#                         line_content_str = line_content_str + l + '\n'
#                 else:
#                     line_content_str = line_content_str + l + '\n'
#         return line_content_str.split('\n')
#
#     def merge_talk(self, content: list) -> list:
#         """
#         将双引号中的所有内容重新拼接为一行显示
#         :param content:
#         :return:
#         """
#         content_str = ""
#         is_start = False
#         for h in content:
#             if h != '':
#                 if is_start is False:
#                     # 如果最有一次出现的开始符的index大于结束符,说明这句话没说完
#                     if h.rfind('“') > h.rfind('”'):
#                         # 开始新的循环
#                         is_start = True
#                         content_str = content_str + h
#                     else:
#                         # 正常换行
#                         content_str = content_str + h + '\n'
#                 elif is_start is True:
#                     if h[0] != '“' and h.rfind('“') < h.rfind('”'):  # 不是以开始双引号开头，但是有结束双引号结尾。说明这句话说完了
#                         is_start = False
#                         content_str = content_str + h + '\n'
#                     elif h[0] != '“' and h.rfind('“') > h.rfind('”'):  # 不是以开始双引号开头，但是以开始双引号结尾，说明虽然说完了，但是又说了一句话
#                         content_str = content_str + h
#                     elif h[0] != '“' and h.rfind('“') == h.rfind('”'):  # 不是以开始双引号开头，但是居然没有开始符合和结束符，说明话还没说完
#                         content_str = content_str + h
#                     else:
#                         # 如果进来这一行，理论上有异常数据了。上一句明明还没说完，但第一个字符居然是结束双引号,避免接下来数据异常，还是进行换行操作
#                         is_start = False
#                         content_str = content_str + h + '\n'
#         return content_str.split('\n')
#
#
# class FormatByGlobal2:
#     """
#     全局模式2,推荐使用。
#     该模式的逻辑：
#     1、先按照换行符，把整篇文章都换行。
#     2、再根据双引号的规则，拼接出一行正文。
#     3、再根据结束符号进行二次换行处理，效果比全局模式1更好
#     """
#
#     def __init__(self):
#         self.ad_str_tuple: dict = Template.ad_str.value  # 广告字符
#         self.talk_str_list: list = Template.talk_str.value  # 表示说话的字符，双引号左右2侧都有可能出现
#         self.end_str_list: list = Template.end_str.value  # 双引号右侧表示说话后的第一个字符，碰到这个就不能换行了
#         self.warp_str_list: list = Template.wrap_character.value  # 统一换行字符
#
#     def new_format(self, content_list: list) -> list:
#         """
#         格式化
#         :param content_list:
#         :return:
#         """
#         content_f = ""
#         content_fl = []
#         for line_str in content_list:
#             content_f = content_f + FormatCommon().wrap_by_punctuation_mark_line(line_str)  # 先全部按照换行符处理一下，全部换行
#         content_l: list = content_f.split("\n")
#         for ii in content_l:
#             i_str = re.sub('\s', '', ii)  # 清理空格字符 \s 表示为空格
#             if i_str != "":
#                 content_fl.append(i_str)
#         return content_fl
#
#     def line_feed_by_str(self, content_list: list) -> list:
#         """
#         按换行字符把所有内容进行统一换行
#         :param content_list: 按换行符进行数组切割后的list
#         :return:
#         """
#         result_list: list = []
#         for line in content_list:
#             if line != "":
#                 line_str: str = line
#                 for warp_str in self.warp_str_list:
#                     if line_str.count(warp_str) > 0 and line_str[-1:] != warp_str:
#                         # 如果结束符的个数大于0，并且该行文本的最后一个字符不是该换行字符
#                         line_str = line_str.replace(warp_str, warp_str + '\n')
#                 line_str_list: list = line_str.split("\n")
#                 for line_str in line_str_list:
#                     if line_str != "":
#                         result_list.append(line_str)
#         return result_list
#
#     def format_end_str(self, content_list: list) -> list:
#         """
#         检查每一行的结束是否有结束符号
#         :param content_list:
#         :return:
#         """
#         start_wrap_character = Template.wrap_character_by_line.value
#         result_list: list = []
#         temp_str: str = ""  # 用于存放临时字符的
#         for line in content_list:
#             if any(wrap_str in line[-1:] for wrap_str in start_wrap_character):
#                 sss = temp_str + line
#                 if FormatCommon().check_str_is_line(sss):
#                     result_list.append(temp_str + line)
#                     temp_str = ""
#                 else:
#                     temp_str = temp_str + line
#             else:
#                 temp_str = temp_str + line
#         if temp_str != "":
#             # 避免出现漏网之鱼
#             result_list.append(temp_str)
#         return result_list
