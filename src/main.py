import re
import os
import time
import codecs
import _thread
import requests
import numpy as np
from my_fake_useragent import UserAgent

file_default_content = \
'''
程序类型：小说爬虫 version 1.2
程序作者：henryyy
运行环境：windows
使用方法：把小说目录页网址复制进横线下任意一行，若想程序爬取该小说，请务必确保该行内没有任何多余字符，如行首空格
程序简介：爬取小说，自动排版，自动去广告，数字数，输出TXT文件转换为UTF-8编码，速度为每秒20-100次访问。
作者声明：此程序仅供学习交流之用途，请勿用于任何商业用途。所有小说仅供试阅读，小说的版权归原作者/网站/出版社所有，请勿用于任何商业用途。作者对任何不当使用概不负责。

注：请不要提高访问率或者改成多线程！！！不要给网站带来太大负担！！！

---------------------------------------------------------------------------------------
支援的网页有:
    1. UU看书：https://www.uuks.org - 优点：质量高。缺点：书籍少
    2. UU看书：https://www.uukanshu.com - 优点：书籍较多。缺点：质量中等
    3. 飘天文学：https://www.ptwxz.com - 优点：质量高。缺点：书籍少
    4. 笔趣阁：http://www.bqxs520.com - 优点：章节全。缺点：质量低
    5. 笔趣阁：https://www.ibiquge.net - 优点：书籍特别多。缺点：爬取特别慢，质量低
    6. 波波中文网：https://www.bobozw.com - 随手加进来的，这网站不咋地
---------------------------------------------------------------------------------------

示例：
1. 呢喃诗章 （请删除网址前的空格，之后运行程序）
 https://www.uuks.org/b/41561/

2. 明克街13号 - 418章 （请删除网址前的空格，之后运行程序）
 https://www.uuks.org/b/49430/
 
3. 请自行写入后续网址...












'''

## 申请访问的速度（每秒x次）
speed = 100
## 需要爬取的章节（最新的x章）
num_of_chapters = 0

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

## 屏显进度条
def status_bar(current_num_of_keys, total_num_of_keys, start_time):
    progress = current_num_of_keys / total_num_of_keys
    total_num_of_grid = 20
    num_of_filled_grid = round(progress * total_num_of_grid)
    num_of_empty_grid = total_num_of_grid - num_of_filled_grid
    time_used = time.time() - start_time
    minutes_used = time_used//60
    seconds_used = time_used%60
    expected_time_used = (1/progress) * time_used if progress != 0 else 0
    expected_minutes_used = expected_time_used//60
    expected_seconds_used = expected_time_used%60
    print(f'\r进程: {num_of_filled_grid * "■"}{(num_of_empty_grid) * "□"} [{progress*100: >6.2f}%]  【已耗时：{minutes_used:0>2.0f}分{seconds_used:0>2.0f}秒】  【预计用时：{expected_minutes_used:0>2.0f}分{expected_seconds_used:0>2.0f}秒】',end="")

## 预处理语句，根据关键词去除不想要的行，或者去除关键字，替换关键字等等
def pre_process(line, title_of_chapter = "None"):
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
    keywords = ["</a>", "7017k", "小说网", "小说在线阅读", "零点看书", "---", "()", "小说更新后会发送邮件到您的邮箱", "正在手打中，请稍等片刻，内容更新后，请重新刷新页面，即可获取最新更新！"]
    unwanted_keywords = domains + keywords
    for unwanted_keyword in unwanted_keywords:
        if unwanted_keyword in line:
            return ""
    ## 删除关键词
    unwanted_words = ["&nbsp;", "&emsp;", "&ldquo;", "&rdquo;", "&lt;", "&rt;", "\n", '\r', '\n\r', '\r\n']
    for unwanted_word in unwanted_words:
        line = line.replace(unwanted_word, "")
    ## 替换关键词
    replace_words = {"。。": "。", "、、": "、", "…": "...", "|": "", "《》":"", ".asxs.":"**", "...。":"...", "…。":"…"}
    for replaced_word in replace_words.keys():
        line = line.replace(replaced_word, replace_words[replaced_word])
    ## 避免重复标题
    if line in title_of_chapter:
        return ""
    ## 规避空行
    if len(line) == 0:
        return ""
    return "　　" + line + '\n'

## 根据url爬取单独章节，并将章节添加到 字典 novel 里
def chapter_crawler(url_of_chapter, idx, encode, novel, report, chapter_word_counts, depth = 0):
    ## 声明变量
    title_of_chapter = str()
    content_of_chapter = list()
    error = False

    ## 访问失败后，最多重复访问统一章节五次
    if depth >= 5:
        novel[idx] = f"\n\n第{idx + 1}节 访问失败\n　　无内容\n"
        report[idx] = f"\n\n第{idx + 1}节 访问失败\n　　网址: {url_of_chapter}\n"
        return 1

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
    elif "https://www.bobozw.com/" in url_of_chapter:
        title_of_chapter_regx = '<h1>(.*?)</h1>'
        content_of_chapter_regx = ['&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<']
    else:
        return 1

    ## 爬取网站内容，如果失败则重复申请
    try:
        ua = UserAgent(family='chrome')
        res = ua.random()
        headers = {"User-Agent": res}
        response_2 = requests.get(url=url_of_chapter, headers=headers)
        response_2.encoding = encode
    except:
        time.sleep(0.5)
        chapter_crawler(url_of_chapter, idx, encode, novel, report, chapter_word_counts, depth=depth+1)
        return 1

    ## 爬取标题，如果失败则使用警示语标题
    try:
        title_of_chapter = re.findall(title_of_chapter_regx, response_2.text)[0]
        title_of_chapter = title_of_chapter.lstrip()
    except:
        title_of_chapter = f"第{idx+1}节 访问成功 爬取【标题】失败"
        error = True

    ## 使用不同正则表达式爬取标题，直到成功。如果都失败，则用警示语内容
    try:
        for regx in content_of_chapter_regx:
            content_of_chapter = re.findall(regx, response_2.text)
            if not (len(content_of_chapter) == 0 or (len(content_of_chapter) == 1 and content_of_chapter[0] == "")):
                break
    except:
        content_of_chapter = [f"第{idx+1}节 访问成功 爬取【内容】失败"]
        error = True

    ## 判断内容是否为空，如果是，则用警示语内容
    if len(content_of_chapter) == 0 or (len(content_of_chapter) == 1 and content_of_chapter[0] == ""):
        content_of_chapter = [f"第{idx+1}节 访问成功 爬取【内容】失败"]
        error = True

    ## 组织内容，进行去广告等操作
    chapter_content = f'\n\n{title_of_chapter}\n'
    for line in content_of_chapter:
            chapter_content += pre_process(line, title_of_chapter)

    ## 数字数，并把字数放进【章节字数缓存区】
    chapter_word_count = 0
    for char in chapter_content:
        if '\u4e00' <= char and char <= '\u9fff':
            chapter_word_count += 1
    chapter_word_counts[idx] = chapter_word_count

    ## 将章节内容放进【小说内容缓存区】
    novel[idx] = chapter_content

    ## 如果过程产生错误，则吧错误报告写入【错误报告缓存区】
    if (error == True):
        report[idx] = chapter_content + f"　　URL: {url_of_chapter}\n\n"
        for line in response_2.text.splitlines():
            report[idx] = report[idx] + pre_process(line)
        return 1
    else:
        return 0

## 爬取目录以及章节对应网址
def novel_crawler(url_of_book, num_of_chapter, url_of_books):
    ## 导入速度变量
    global speed
    ## 记录线程启动时间
    start_time = time.time()

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
        speed = 100
    elif "https://www.ibiquge.net" in url_of_book:
        encode = 'UTF-8'
        base_url = 'https://www.ibiquge.net'
        title_of_book_regx = '<h1>(.*?)</h1>'
        author_of_book_regx = '<p>作.*者：<a href=".*">(.*?)</a></p>'
        herf_of_chapters_regx ='<dd> <a style="" href="(.*?)">'
        start = 12
        stop = None
        step = 1
        speed = 20
    elif "https://www.bobozw.com/" in url_of_book:
        encode = 'ANSI'
        base_url = "https://www.bobozw.com/"
        title_of_book_regx = '<h1>(.*?)</h1>'
        author_of_book_regx = '<p>作&nbsp;&nbsp;&nbsp;&nbsp;者：(.*?)</p>'
        herf_of_chapters_regx = '<dd><a href="(.*?)">.*</a></dd>'
        start = 0
        stop = None
        step = 1
        speed = 30
    else:
        ## 如果不在预定义网址内，啧将html文件导出至【错误报告.txt】
        encode = "ANSI"
        ua = UserAgent(family='chrome')
        res = ua.random()
        headers = {"User-Agent": res}
        response_1 = requests.get(url=url_of_book, headers=headers)
        response_1.encoding = encode
        fout = open("错误报告.txt", 'w', encoding=encode)
        fout.write(response_1.text)
        fout.close()
        print(f"【错误报告.txt】已创建")
        url_of_books.remove(url_of_book)
        return 1

    ## 【小说内容缓存区】
    novel = dict()
    ## 【错误报告缓存区】
    report = dict()
    ## 【章节字数缓存区】
    chapter_word_counts = dict()

    ## 爬取目录页面内容
    try:
        ua = UserAgent(family='chrome')
        res = ua.random()
        headers = {"User-Agent": res}
        response_1 = requests.get(url=url_of_book, headers=headers)
        response_1.encoding = encode
    except:
        print(f"提示：{url_of_book} 访问目录失败")
        return

    ## 载入书籍信息
    try:
        title_of_book = re.findall(title_of_book_regx, response_1.text)[0]
        author_of_book = re.findall(author_of_book_regx, response_1.text)[0]
        herf_of_chapters = re.findall(herf_of_chapters_regx,response_1.text)
        url_of_chapters = [base_url + i for i in herf_of_chapters][start:stop:step]
    except:
        print(f"提示：{url_of_book} 爬取内容失败")
        return

    ##print(url_of_chapters)

    ##在终端输出书籍信息
    line_1 = "书名：" + title_of_book + '\n'
    line_2 = "作者：" + author_of_book + '\n'
    line_3 = "链接：" + url_of_book + '\n'
    print(line_1+line_2+line_3, end="")

    ## 定位需要爬取的章节位置
    start = 0 if (num_of_chapter <= 0) else (len(url_of_chapters) - num_of_chapter)
    stop = len(url_of_chapters)
    total = stop - start

    ## 定义访问率
    access_rate = 1/speed

    ## 多线程执行章节爬取，导入字典中
    for idx in range(start, stop):
        status_bar(len(novel.keys()), total, start_time)
        url_of_chapter = url_of_chapters[idx]
        try:
            _thread.start_new_thread(chapter_crawler, (url_of_chapter, idx, encode, novel, report, chapter_word_counts))
        except:
            novel[idx] = f"\n\n第{idx + 1}节 线程启动失败\n　　无内容\n"
            report[idx] = f"\n\n第{idx + 1}节 线程启动失败\n　　网址: {url_of_chapter}\n"
        time.sleep(access_rate)

    ## 建立时间戳
    time_stamp = time.time()

    ## 等待线程执行完毕，最多等待30秒
    while len(novel.keys()) < total and time.time() - time_stamp <= 30:
        time.sleep(0.1)
        status_bar(len(novel.keys()), total, start_time)
        pass

    ## 输出100%进度条
    status_bar(len(novel.keys()), total, start_time)
    print()

    ## 为所有章节排序
    keys = sorted(novel.keys())

    ## 统计全文中文字符字数
    total_word_count = sum(list(chapter_word_counts.values()))
    avg = np.mean(list(chapter_word_counts.values()))
    print(f"字数：{total_word_count/10000:.1f}万  ->  平均每章 {round(avg)} 字")

    ## 开始写入txt文件
    try:
        ## 定义储存路径
        save_path = title_of_book + ".txt"
        ## 打开文件
        fout = open(save_path, 'w', encoding=encode)
        ## 写入【书籍信息】
        fout.write("书籍信息" + '\n')
        fout.write(f"　　书名：{title_of_book} \n")
        fout.write(f"　　作者：{author_of_book} \n")
        fout.write(f"　　字数：{total_word_count/10000:.1f}万 \n")
        fout.write(f"　　校对：henryyy \n")
        fout.write(f"　　链接：{url_of_book} \n")

        accumulated_word_count = 0
        ## 写入【正文内容】
        for idx in keys:
            fout.write(novel[idx])
            ##accumulated_word_count += chapter_word_counts[idx]
            ##fout.write(f"　　***\n")
            ##fout.write(f"　　【阅读进度：{accumulated_word_count/total_word_count:.2%}】")
            ##fout.write(f"　　【进度(字数)：{accumulated_word_count/total_word_count:.2%}  {accumulated_word_count/10000:.1f}/{total_word_count/10000:.1f}万 字】\n")
            ##fout.write(f"　　【进度(章节)：{(idx+1) / total:.2%}  {idx+1}/{total} 章】\n")
        ## 写入完毕，关闭文件流
        fout.close()
        ## 转换为UTF-8格式
        if encode != 'UTF-8':
            convert_to_utf8(save_path)
        ## 屏幕输出结果
        print(f"结果：{start + 1} 至 {stop} 章已被写入 {save_path}")
    except:
        save_path = title_of_book + ".txt"
        print(f"提示；文件【{save_path}】写入失败")

    ## 写入【错误报告】
    if len(report.keys()) != 0:
        try:
            ## 打开专属错误报告之输出流
            fout = open(title_of_book + "_错误报告.txt", 'w', encoding=encode)
            ## 写入章节错误报告
            for idx in sorted(report.keys()):
                fout.write(report[idx])
            ## 关闭输出流
            fout.close()
            print(f"提示：爬取过程错误，【{title_of_book + '_错误报告.txt'}】已就绪")
        except:
            print(f"提示；文件【{title_of_book + '_错误报告.txt'}】写入失败")

    url_of_books.remove(url_of_book)

    return 0

## 从txt文件中抓取网址
def get_url_of_books(file_contains_url_of_books):
    ## 如果外部储存不存在，则重新创建预定义文件
    if not os.path.exists(file_contains_url_of_books):
        fout = open(file_contains_url_of_books, 'w', encoding='UTF-8')
        fout.write(file_default_content)
        fout.close()
        print(f"\n提示：未发现 {file_contains_url_of_books} 文件，已重新创建。")
        print(f"提示：请在 {file_contains_url_of_books} 文件中写入想要爬取的小说目录网址。")
        return []
    ## 读取输入流，抓取网址，并且对网址加工，使其处在未激活状态
    url_of_books = []
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

## 主函数
def main():
    ## 定义外部储存文件名
    file_contains_url_of_books = "url.txt"
    ## 读取外部储存
    url_of_books = get_url_of_books(file_contains_url_of_books)
    ## 确认要爬取的东西非空
    if len(url_of_books) == 0:
        print(f"\n提示：{file_contains_url_of_books} 中未写入需要爬取的网址")
    ## 开始爬取
    for url_of_book in url_of_books.copy():
        print("\n" + str("-" * 100))
        novel_crawler(url_of_book, num_of_chapters, url_of_books)
        print("-" * 100)
    ## 等待爬取结束
    while len(url_of_books) != 0:
        time.sleep(1)
        pass
    print("\n<程序执行完毕>")
    input("<按回车键结束程序>")
    return

main()

## pyinstaller -F main.py