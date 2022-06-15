import requests
import re
import os
import _thread
import time
import codecs
import sys
import psutil

'''
1. https://www.uuks.org     UU看书 - 质量高，没广告，书少
2. https://www.uukanshu.com UU看书 - 有广告
3. https://www.ptwxz.com    飘天文学 - 质量高，书多
4. http://www.bqxs520.com   笔趣阁 - 章节全，质量差
5. https://www.ibiquge.net  笔趣阁 - 爬取慢，章节缺失
'''

declaration = \
'''\n\n　=============================================
　欢迎阅读【henryyy】个人校对电子书。转载请保留本声明，谢谢合作～
　仅因个人爱好订阅及整理，如果您喜欢，望您购买VIP章节或正版纸质书。
　本书仅供试阅，版权归原作者/网站/出版社所有，请勿用于任何商业用途～
　★☆更多校对、精校版电子书下载及阅读敬请访问：★☆
　——阡陌居：www.1000qm.vip
　=============================================\n'''

file_default_content = \
'''
程序类型：小说爬虫 version 1.0
程序作者：henryyy
运行环境：windows
使用方法：把小说目录页网址复制进横线下任意一行，若想程序爬取该小说，请务必确保该行内没有任何多余字符，如行首空格
程序简介：爬取小说，自动排版，自动去广告，数字数，输出TXT文件转换为UTF-8编码，速度为每秒1000次申请访问。
作者声明：此程序仅供学习交流之用途，请勿用于任何商业用途。所有小说仅供试阅读，小说的版权归原作者/网站/出版社所有，请勿用于任何商业用途。作者对任何不当使用概不负责。

version 1.0 支援的网页有
1. UU看书：https://www.uuks.org - 质量高，没广告，书少
2. UU看书：https://www.uukanshu.com - 质量普通，有广告
3. 飘天文学：https://www.ptwxz.com - 质量高，书多
4. 笔趣阁：http://www.bqxs520.com - 章节全，质量差
5. 笔趣阁：https://www.ibiquge.net - 爬取慢，章节缺失

---------------------------------------------------------------------------------------

示例：

1. 呢喃诗章 （请删除网址前的空格，之后运行程序）
 https://www.uuks.org/b/41561/






'''

## 申请访问的速度（每秒x次）
speed = 100
## 需要爬取的章节（最新的x章）
num_of_chapters = 0
## 访问失败累计次数，超过15次则默认网站有反爬虫，终止程序
fail_count = 0

## 将txt文件从ansi编码转换为utf-8编码
def convert_to_utf8(file_name):
    blockSize = 1048576
    with codecs.open(file_name, "r", encoding="mbcs") as sourceFile:
        with codecs.open("new_" + file_name, "w", encoding="UTF-8") as targetFile:
            while True:
                contents = sourceFile.read(blockSize)
                if not contents:
                    break
                targetFile.write(contents)
    os.remove(file_name)
    os.rename('new_' + file_name,file_name)

## 预处理句子，根据关键词去除不想要的行，或者去除关键字，替换关键字
def pre_process(line, title_of_chapter):
    ## 规避空行
    if len(line) == 0:
        return ""
    ## 删除行首缩进
    while len(line) != 0 and line[0] in [" ", "　", "　", '\t', '\n', '\r']:
        line = line[1:]
    ## 规避空行
    if len(line) == 0:
        return ""
    ## 根据全句去除不想要的行
    unwanted_lines = ["", "\n", title_of_chapter]
    for unwanted_line in unwanted_lines:
        if line == unwanted_line:
            return ""
    ## 根据关键词去除不想要的行
    domains = ["https://", ".com", ".xyz", ".net", ".top", ".tech", ".org", ".gov", ".edu", ".ink", ".int", ".mil", ".put", ".cn", ".cc", ".biz", ".la",".bqkan8"]
    keywords = ["</a>", "7017k", "小说网", "小说在线阅读", "零点看书", "---", "()", "小说更新后会发送邮件到您的邮箱"]
    unwanted_keywords = domains + keywords
    for unwanted_keyword in unwanted_keywords:
        if unwanted_keyword in line:
            return ""
    ## 删除关键词
    unwanted_words = ["&nbsp;", "&emsp;", "&ldquo;", "&rdquo;", "\n", '\r', '\n\r', '\r\n']
    for unwanted_word in unwanted_words:
        line = line.replace(unwanted_word, "")
    ## 替换关键词
    replace_words = {"。。":"。", "、、":"、", "…":"...", "|":""}
    for replaced_word in replace_words.keys():
        line = line.replace(replaced_word, replace_words[replaced_word])
    ## 规避空行
    if len(line) == 0:
        return ""
    return "　　" + line + '\n'

## 根据url爬取单独章节，并将章节添加到 字典 novel 里
def chapter_crawler(url_of_chapter, idx, encode, novel):
    ## 查看累计访问失败次数
    global fail_count
    if fail_count >= 20:
        return

    ## 根据不同网址定义正则表达式
    if "www.ptwxz.com" in url_of_chapter:
        title_of_chapter_regx = '</a>(.*?)</H1>'
        content_of_chapter_regx = ['&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<br />']
    elif "www.uuks.org" in url_of_chapter:
        title_of_chapter_regx = '<h1 id="timu">(.*?)</h1>'
        content_of_chapter_regx = ['<p>(.*?)</p>']
    elif "www.uukanshu.com" in url_of_chapter:
        title_of_chapter_regx = '<h1 id="timu">(.*?)</h1>'
        content_of_chapter_regx = ['p>(.*?)<', "br />(.*?)<", '>(.*?)<p', ">(.*?)<br", "[^ ](.*?)<br/>"]
    elif "www.bqxs520.com" in url_of_chapter:
        title_of_chapter_regx = '.*<h1>(.*?)</h1>'
        content_of_chapter_regx = ['br/>(.*?)<']
    elif "https://www.ibiquge.net" in url_of_chapter:
        title_of_chapter_regx = '.*<h1>(.*?)</h1>'
        content_of_chapter_regx = ['&nbsp;(.*?)<|\s']
    else:
        return

    ## 爬取网站内容
    try:
        response_2 = requests.get(url_of_chapter)
        response_2.encoding = encode
    except:
        time.sleep(0.1)
        fail_count += 1
        chapter_crawler(url_of_chapter, idx, encode, novel)
        fail_count -= 1
        return

    ##print(response_2.text)

    ## 爬取标题
    try:
        title_of_chapter = re.findall(title_of_chapter_regx, response_2.text)[0]
        title_of_chapter = title_of_chapter.lstrip()
    except:
        title_of_chapter = f"{idx+1}节 访问成功 爬取【标题】失败"

    ## 爬取内容
    try:
        for regx in content_of_chapter_regx:
            content_of_chapter = re.findall(regx, response_2.text)
            if not (len(content_of_chapter) == 0 or (len(content_of_chapter) == 1 and content_of_chapter[0] == "")):
                break
    except:
        content_of_chapter = [f"{idx+1}节 访问成功 爬取【内容】失败"]

    ## 判断内容是否为空
    if len(content_of_chapter) == 0 or (len(content_of_chapter) == 1 and content_of_chapter[0] == ""):
        content_of_chapter = [f"{idx+1}节 访问成功 爬取【内容】失败"]
        print(response_2.text)
        time.sleep(1)

    chapter_content = f'\n\n{title_of_chapter}\n'
    for line in content_of_chapter:
            chapter_content += pre_process(line, title_of_chapter)
    novel[idx] = chapter_content
    return

## 进度条
def status_bar(current_num_of_keys, total_num_of_keys, start_time, fail_count):
    progress = current_num_of_keys / total_num_of_keys
    num_of_grid = round(progress * 10 * 2)
    time_used = time.time() - start_time
    minutes_used = time_used//60
    seconds_used = time_used%60
    print(f'\r进程: {num_of_grid * "■"}{(20 - num_of_grid) * "□"} [{progress*100: >6.2f}%]    已耗时：{minutes_used:.0f}分 {seconds_used:.0f}秒    失败申请：{fail_count}次    ',end="")

## 爬取目录以及章节对应网址
def novel_crawler(url_of_book, num_of_chapter, url_of_books):
    global speed
    start_time = time.time()
    linear = False

    ## 根据不同网址定义正则表达式
    if "www.ptwxz.com" in url_of_book:
        encode = 'ANSI'
        base_url = url_of_book
        title_of_book_regx = '<h1>(.*?)最新章节</h1>'
        author_of_book_regx = '作者：(.*?) &nbsp; &nbsp;'
        herf_of_chapters_regx = '<li><a href="(.*?)">'
        start = 0
        stop = None
        step = 1
        speed = 100
    elif "www.uuks.org" in url_of_book:
        encode = 'UTF-8'
        base_url = 'https://www.uuks.org'
        title_of_book_regx = '<h3>《(.*?)》正文</h3>'
        author_of_book_regx = '<h2>作者：(.*?)</h2>'
        herf_of_chapters_regx ='<li><a href="(.*)">.*</a></li>'
        start = 1
        stop = None
        step = 1
        speed = 100
    elif "www.uukanshu.com" in url_of_book:
        encode = 'ANSI'
        base_url = 'https://www.uukanshu.com'
        title_of_book_regx = '<h1><a href=".*" title="(.*?)最新章节">.*</a></h1>'
        author_of_book_regx = '<h2>.*作者：<a href=".*" target="_blank">(.*?)</a></h2>'
        herf_of_chapters_regx ='<li><a href="(.*?)" title=".*" target="_blank">.*</a></li>'
        start = -1
        stop = 0
        step = -1
        speed = 50
    elif "http://www.bqxs520.com" in url_of_book:
        encode = 'UTF-8'
        base_url = 'http://www.bqxs520.com'
        title_of_book_regx = '<h1>(.*?)</h1>'
        author_of_book_regx = '<p>作.*者：(.*?)</p>'
        herf_of_chapters_regx ='<dd><a href="(.*?)">'
        start = 9
        stop = None
        step = 1
    elif "https://www.ibiquge.net" in url_of_book:
        encode = 'UTF-8'
        base_url = 'https://www.ibiquge.net'
        title_of_book_regx = '<h1>(.*?)</h1>'
        author_of_book_regx = '<p>作.*者：<a href=".*">(.*?)</a></p>'
        herf_of_chapters_regx ='<dd> <a style="" href="(.*?)">'
        start = 12
        stop = None
        step = 1
        speed = 0.5
        linear = True
    else:
        return

    ## 小说储存区，类似于缓冲区
    novel = dict()

    ## 爬取目录页面内容
    try:
        response_1 = requests.get(url_of_book)
        response_1.encoding = encode
    except:
        print("爬取目录失败")
        novel_crawler(url_of_book, num_of_chapter)
        return

    ##print(response_1.text)

    ## 载入书籍信息
    try:
        title_of_book = re.findall(title_of_book_regx, response_1.text)[0]
        author_of_book = re.findall(author_of_book_regx, response_1.text)[0]
        herf_of_chapters = re.findall(herf_of_chapters_regx,response_1.text)
        url_of_chapters = [base_url + i for i in herf_of_chapters][start:stop:step]
    except:
        print("Crawl content page failed.")
        return

    ##print(herf_of_chapters)
    ##print(url_of_chapters)

    ##在终端输出书籍信息
    line_1 = "书名：" + title_of_book + '\n'
    line_2 = "作者：" + author_of_book + '\n'
    line_3 = "链接：" + url_of_book + '\n'
    print(line_1+line_2+line_3, end="")

    ## 定位需要爬取的章节
    start = 0 if (num_of_chapter <= 0) else (len(url_of_chapters) - num_of_chapter)
    stop = len(url_of_chapters)
    total = stop - start

    access_rate = 1/speed
    ## 多线程执行章节爬取，导入字典中
    for idx in range(start, stop):
        status_bar(len(novel.keys()), total, start_time, fail_count)
        url_of_chapter = url_of_chapters[idx]
        try:
            if linear == True:
                chapter_crawler(url_of_chapter, idx, encode, novel)
            else:
                _thread.start_new_thread(chapter_crawler, (url_of_chapter, idx, encode, novel))
                time.sleep(access_rate)
        except:
            print("Fail to crawl chapter", idx)

    ##print(f'\r进程: {20 * "■"} {1:.2%}', end="")

    time_stamp = time.time()


    ## 等待线程执行完毕，最多等待30秒
    while len(novel.keys()) < total and time.time() - time_stamp <= 30:
        time.sleep(0.1)
        status_bar(len(novel.keys()), total, start_time, fail_count)
        if fail_count >= 15:
            break
        pass

    status_bar(len(novel.keys()), total, start_time, fail_count)
    print()

    keys = sorted(novel.keys())

    extension = "" if start == 0 else f"({start+1}-{stop})"

    ##打开文件
    save_path = title_of_book + f"{extension}.txt"
    ## 移除旧文件
    try:
        os.remove(save_path)
        print(f"提示：{save_path} 已被擦除")
    except:
        pass
    print(f"提示：{save_path} 已创建")

    ## 统计全文中文字符字数
    word_count = 0
    for idx in keys:
        for s in novel[idx]:
            if '\u4e00' <= s and s <= '\u9fff':
                word_count += 1

    ## 开始写入文件
    fout = open(save_path, 'a+', encoding=encode)
    fout.write("书籍信息" + '\n')
    fout.write(f"　　书名：{title_of_book}{extension}\n")
    fout.write(f"　　作者：{author_of_book}\n")
    fout.write(f"　　字数：{word_count/10000:.1f}万\n")
    fout.write(f"　　校对：henryyy\n")
    ## fout.write(f"　　链接：{url_of_book}\n")

    ##fout.write(declaration)
    for idx in keys:
        fout.write(novel[idx])
    print(f"结果：{start+1} 至 {stop} 章已被写入 {save_path}")
    fout.close()

    if encode != 'UTF-8':
        convert_to_utf8(save_path)

    url_of_books.remove(url_of_book)

    return 0

def get_url_of_books(file_contains_url_of_books):
    if not os.path.exists(file_contains_url_of_books):
        fout = open(file_contains_url_of_books, 'w', encoding='UTF-8')
        fout.write(file_default_content)
        fout.close()
        print(f"\n提示：未发现 {file_contains_url_of_books} 文件，已重新创建。")
        print(f"提示：请在 {file_contains_url_of_books} 文件中写入想要爬取的小说目录网址。")
        return []

    url_of_books = []
    try:
        fin = open(file_contains_url_of_books, 'r', encoding='UTF-8')
        fout = open('new_' + file_contains_url_of_books, 'w', encoding='UTF-8')
        for line in fin.readlines():
            line = line[:-1]                                            ## remove the '\n' in the end of line
            if ("www." in line) and (" " not in line):
                url_of_books.append(line)
                fout.write(' ' + line + '\n')
            else:
                fout.write(line + '\n')
        fin.close()
        fout.close()
        os.remove(file_contains_url_of_books)
        os.rename('new_' + file_contains_url_of_books, file_contains_url_of_books)
        return url_of_books
    except:
        print(f"\n提示：未找到{file_contains_url_of_books}文件，请重试")
        return []

def main():
    file_contains_url_of_books = "url.txt"
    url_of_books = get_url_of_books(file_contains_url_of_books)
    if len(url_of_books) == 0:
        print(f"\n提示：{file_contains_url_of_books} 中未写入需要爬取的网址")
    for url_of_book in url_of_books.copy():
        print("\n" + str("-" * 100))
        novel_crawler(url_of_book, num_of_chapters, url_of_books)
        print("-" * 100)
    while len(url_of_books) != 0:
        time.sleep(1)
        pass
    print("\n<程序执行完毕>")
    input("<按回车键结束程序>")
    return

main()

## pyinstaller -F main.py