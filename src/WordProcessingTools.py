import re
import html

## 处理小说标题
def process_title(line):
    ## 规避空行
    if len(line) == 0:
        return ""
    ## 删除行首缩进
    while len(line) != 0 and line[0] in [" ", "　", "　", '\t', '\n', '\r']:
        line = line[1:]
    return line

## 处理小说段落
def process_paragraph(string):
    ## 将html语言翻译成人类语言
    string = html.unescape(string)
    ## 清除剩余html元素
    string = re.sub(pattern=r'<.*?>.*？<.*?>;', repl="", string=string, flags=re.DOTALL)
    ## 翻译剩余html语言
    translate = {'<br>':'\n', '<br/>':'\n', '<br />':'\n', '<p>':'', '</p>':'\n', ' ':' ', '&nbsp;': ' '}
    for key in translate.keys():
        string = string.replace(key, translate[key])
    ## 分行
    lines = string.split('\n')
    output = []
    for line in lines:
        if line != '':
            output.append(line)
    return output

## 处理小说句子
def process_line(line, title_of_chapter = "No_Such_title"):
    ## 规避空行
    if len(line) == 0:
        return ""
    ## 清除剩余html元素
    line = re.sub(pattern='<.*?>.*?</.*?>', repl='', string=line)
    ## 删除行首缩进
    while len(line) != 0 and line[0] in [" ", "　", "　", '\t', '\n', '\r']:
        line = line[1:]
    ## 规避空行
    if len(line) == 0:
        return ""
    ## 根据全句去除不想要的行
    unwanted_lines = ["", "\n", title_of_chapter, "-- 上拉加载下一章 s -->", ""]
    for unwanted_line in unwanted_lines:
        if line == unwanted_line:
            return ""
    ## 根据关键词去除不想要的行
    domains = ["https://", ".com", ".xyz", ".net", ".top", ".tech", ".org", ".gov", ".edu", ".ink", ".int", ".mil",
               ".put", ".cn", ".cc", ".biz", ".la", ".bqkan8"]
    keywords = ["</a>", "7017k", "小说网", "小说在线阅读", "零点看书", "---", "()", "小说更新后会发送邮件到您的邮箱","正在手打中，请稍等片刻，内容更新后，请重新刷新页面，即可获取最新更新！"]
    unwanted_keywords = domains + keywords
    for unwanted_keyword in unwanted_keywords:
        if unwanted_keyword in line:
            return ""
    ## 删除关键词
    unwanted_words = ["&nbsp;", "&emsp;", "&ldquo;", "&rdquo;", "&lt;", "&rt;", "\n", '\r', '\n\r', '\r\n']
    for unwanted_word in unwanted_words:
        line = line.replace(unwanted_word, "")
    ## 替换关键词
    replace_words = {"…": "...", "┅": "...", "|": "", "《》": "", ".asxs.": "**", "...。": "...", "…。": "…", "赤果": "赤裸", "ꓹ ": "，"}
    for replaced_word in replace_words.keys():
        line = line.replace(replaced_word, replace_words[replaced_word])
    ## 避免重复标题
    if line in title_of_chapter:
        return ""
    ## 规避空行
    if len(line) == 0:
        return ""
    return "　　" + line + '\n'

## 数中文字数
def word_count_of_chin_char(string):
    output = 0
    for char in string:
        if '\u4e00' <= char and char <= '\u9fff' and char != '　':
            output += 1
    return output


