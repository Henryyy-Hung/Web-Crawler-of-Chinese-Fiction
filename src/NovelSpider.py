# -*- coding: utf-8 -*-
import re
import os
import time
import requests
import threading
import WordProcessingTools
from selenium import webdriver
from my_fake_useragent import UserAgent

class ChapterContent(object):
    def __init__(self, url='', title='', content='', report_title='', report_content=''):
        self.__url = url
        self.__title = title
        self.__content = content
        self.__report_title = report_title
        self.__report_content = report_content
        self.__word_count = 0
        self.__ready = False

    @property
    def url(self):
        return self.__url
    @url.setter
    def url(self, value):
        self.__url = value
    @property
    def title(self):
        return self.__title
    @title.setter
    def title(self, value):
        self.__title = value
    @property
    def content(self):
        return self.__content
    @content.setter
    def content(self, value):
        self.__content = value
    @property
    def report_title(self):
        return self.__report_title
    @report_title.setter
    def report_title(self, value):
        self.__report_title = value
    @property
    def report_content(self):
        return self.__report_content
    @report_content.setter
    def report_content(self, value):
        self.__report_content = value
    @property
    def word_count(self):
        return self.__word_count
    @word_count.setter
    def word_count(self, value):
        self.__word_count = value
    @property
    def ready(self):
        return self.__ready
    @ready.setter
    def ready(self, value):
        self.__ready = value
        if self.__ready == True:
            self.__word_count += WordProcessingTools.word_count_of_chin_char(self.title)
            self.__word_count += WordProcessingTools.word_count_of_chin_char(self.content)

class NovelSpider(object):
    def __init__(self, spiderGUI=None):
        ## 和图形界面建立链接
        self.__GUI = spiderGUI
        ## 需要的信息
        self.__url_of_book = r''
        self.__base_url = r''
        self.__encode = r'UTF-8'
        self.__regx_of_book_title = []
        self.__regx_of_book_author = []
        self.__regx_of_chap_href = []
        self.__key_of_content = {'start':0, 'stop':None, 'step':1}
        self.__regx_of_chap_title = []
        self.__regx_of_chap_content = []
        self.__speed_of_crawling = 1
        self.__num_of_chapters_wanted = 0
        self.__crawler_mode = 'requests'
        ## 自动处理的信息
        self.__title_of_book = ''
        self.__author_of_book = ''
        self.__url_of_chapters = []
        self.__content = dict()
        self.__start_time = time.time()
        self.__last_modify_time = time.time()
        self.__state = True
        ## 保存路径
        self.novel_path = os.getcwd() + os.sep + "fiction"
        self.report_path = os.getcwd() + os.sep + "fiction_report"
        super().__init__()

    @property
    def url_of_book(self):
        return self.__url_of_book
    @url_of_book.setter
    def url_of_book(self, value):
        self.__url_of_book = value

    @property
    def base_url(self):
        return self.__base_url
    @base_url.setter
    def base_url(self, value):
        self.__base_url = value

    @property
    def encode(self):
        return self.__encode
    @encode.setter
    def encode(self, value):
        self.__encode = value

    @property
    def regx_of_book_title(self):
        return self.__regx_of_book_title
    @regx_of_book_title.setter
    def regx_of_book_title(self, value):
        self.__regx_of_book_title = value

    @property
    def regx_of_book_author(self):
        return self.__regx_of_book_author
    @regx_of_book_author.setter
    def regx_of_book_author(self, value):
        self.__regx_of_book_author = value

    @property
    def regx_of_chap_href(self):
        return self.__regx_of_chap_href
    @regx_of_chap_href.setter
    def regx_of_chap_href(self, value):
        self.__regx_of_chap_href = value

    @property
    def key_of_content(self):
        return self.__key_of_content
    @key_of_content.setter
    def key_of_content(self, value):
        self.__key_of_content = value

    @property
    def regx_of_chap_title(self):
        return self.__regx_of_chap_title
    @regx_of_chap_title.setter
    def regx_of_chap_title(self, value):
        self.__regx_of_chap_title = value

    @property
    def regx_of_chap_content(self):
        return self.__regx_of_chap_content
    @regx_of_chap_content.setter
    def regx_of_chap_content(self, value):
        self.__regx_of_chap_content = value

    @property
    def speed_of_crawling(self):
        return self.__speed_of_crawling
    @speed_of_crawling.setter
    def speed_of_crawling(self, value):
        self.__speed_of_crawling = value

    @property
    def num_of_chapters_wanted(self):
        return self.__num_of_chapters_wanted
    @num_of_chapters_wanted.setter
    def num_of_chapters_wanted(self, value):
        value = 0 if value <= 0 else value
        self.__num_of_chapters_wanted = value

    @property
    def content(self):
        return self.__content
    @content.setter
    def content(self, value):
        self.__content = value

    @property
    def title_of_book(self):
        return self.__title_of_book
    @title_of_book.setter
    def title_of_book(self, value):
        self.__title_of_book = value

    @property
    def author_of_book(self):
        return self.__author_of_book
    @author_of_book.setter
    def author_of_book(self, value):
        self.__author_of_book = value

    @property
    def url_of_chapters(self):
        return self.__url_of_chapters
    @url_of_chapters.setter
    def url_of_chapters(self, value):
        self.__url_of_chapters = value

    @property
    def crawler_mode(self):
        return self.__crawler_mode
    @crawler_mode.setter
    def crawler_mode(self, value):
        if value == 'selenium':
            if self.speed_of_crawling > 3:
                self.speed_of_crawling = 3
        self.__crawler_mode = value

    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, value):
        self.__state = value

    ## 获取有多少个章节为【ready】状态
    def __len__(self):
        count = 0
        for idx in self.content:
            if self.content[idx].ready == True:
                count += 1
        return count

    ## 从网页取得响应，request为快速方法，selenium为慢速方法
    def get_response(self, url):
        response = None
        if self.crawler_mode == 'requests':
            for i in range(5):
                try:
                    ua = UserAgent(family='chrome')
                    res = ua.random()
                    headers = {"User-Agent": res}
                    response = requests.get(url=url, headers=headers, timeout = 10)
                    response.encoding = self.encode
                    return response.text
                except:
                    continue
        elif self.crawler_mode == 'selenium':
            for i in range(5):
                try:
                    option = webdriver.ChromeOptions()
                    option.add_argument('headless')
                    option.add_argument("--window-size=1920,1080")
                    option.add_argument("--disable-extensions")
                    option.add_argument("--disable-gpu")
                    option.add_argument("--disable-software-rasterizer")
                    option.add_argument('--no-sandbox')
                    option.add_argument('--ignore-certificate-errors')
                    option.add_argument('--allow-running-insecure-content')
                    option.add_argument("blink-settings=imagesEnabled=false")
                    browser = webdriver.Chrome(options=option)
                    browser.get(url)
                    time.sleep(3)
                    response = browser.page_source.__str__()
                    browser.delete_all_cookies()
                    browser.quit()
                    return response
                except:
                    continue
        return response

    ## 渐进式缩小范围提取所需内容
    @staticmethod
    def extract_word(string, list_of_regx):
        current_cycle = [string]
        for regx in list_of_regx:
            regx = re.compile(regx, re.DOTALL)
            next_cycle = []
            for element in current_cycle:
                next_cycle.extend(regx.findall(element))
            current_cycle = next_cycle.copy()
            next_cycle.clear()
        return current_cycle

    ## 输出栏 和GUI的唯一接口
    def msgbox(self, target, value):
        if self.state == True:
            try:
                if target == 'progress_bar':
                    self.__GUI.progress_bar['value'] = value
                elif target == 'title_label':
                    self.__GUI.title_label['text'] = value
                elif target == 'author_label':
                    self.__GUI.author_label['text'] = value
                elif target == 'notice_label':
                    self.__GUI.notice_label['text'] = value
                self.__GUI.top.update()
            except :
                self.state = False

    ## 状态条
    def status_bar(self):
        ## 获取当前爬虫进度
        current_num_of_keys = len(self)
        total_num_of_keys = self.num_of_chapters_wanted if self.num_of_chapters_wanted > 0 else len(self.url_of_chapters)
        progress = current_num_of_keys / total_num_of_keys if total_num_of_keys > 0 else 0
        ## 获取已用时间
        time_used = int(time.time() - self.__start_time)
        minutes_used = time_used // 60
        seconds_used = time_used % 60
        ## 获取逾期时间
        expected_time_used = int((1 / progress) * time_used) if progress > 0 else 0
        expected_minutes_used = expected_time_used // 60
        expected_seconds_used = expected_time_used % 60
        ## 输出当前【爬虫进度】【耗时】【预计耗时】
        output = f'提示：【已耗时：{minutes_used:0>2.0f}分{seconds_used:0>2.0f}秒】【预计用时:{expected_minutes_used:0>2.0f}分{expected_seconds_used:0>2.0f}秒】                    进度：{progress:6.2%}'
        self.msgbox(target='notice_label', value=output)
        self.msgbox(target='progress_bar', value=int(progress * 10000))

    ## 去除列表中重复元素
    @staticmethod
    def remove_duplication(array):
        temp = list()
        for element in array:
            if element not in temp:
                temp.append(element)
        return temp

    ## 爬取小说章节名称，章节内容
    def crawl_chapter_page(self, chapter_content):
        ## 向网页发送请求，得到网页内容
        try:
            response =self.get_response(chapter_content.url)
        except:
            chapter_content.title = chapter_content.report_title = f'内容访问失败'
            chapter_content.content = chapter_content.report_content = f'链接：{chapter_content.url}'
            chapter_content.ready = True
            return False
        if response == None:
            chapter_content.title = chapter_content.report_title = f'内容访问失败'
            chapter_content.content = chapter_content.report_content = f'链接：{chapter_content.url}'
            chapter_content.ready = True
            return False
        ## 根据正则表达式提取对应内容
        chap_title = self.extract_word(response, self.regx_of_chap_title)
        chap_content = self.extract_word(response, self.regx_of_chap_content)
        ## 如果没有提取到任何内容，则报错
        if len(chap_title) == 0 or len(chap_content) == 0:
            chapter_content.title = chapter_content.report_title = f'内容访问成功'
            chapter_content.content = f'爬取失败\n链接：{chapter_content.url}'
            chapter_content.report_content = f'爬取失败\n链接：{chapter_content.url}\n响应:\n{response}'
            chapter_content.ready = True
            return False
        ## 章节名称
        chapter_content.title = WordProcessingTools.process_title(chap_title[0])
        ## 对章节名称进行加工
        temp = ""
        ## 第一步，进行段处理（如有必要）
        if len(chap_content) == 1:
            chap_content = WordProcessingTools.process_paragraph(chap_content[0])
        ## 第二部，进行句处理
        for line in chap_content:
            temp += WordProcessingTools.process_line(line, title_of_chapter=chapter_content.title)
        ## 将处理过的小说内容赋予小说内容类
        chapter_content.content += temp
        ## 将小说内容的状态改为ready
        chapter_content.ready = True
        ## 更新最近修改时间
        self.__last_modify_time = time.time()
        return True

    ## 爬取小说目录页面，获取小说基本资料及章节链接
    def crawl_content_page(self):
        ## 获取网页内容
        try:
            response = self.get_response(self.url_of_book)
        except:
            self.msgbox(target='title_label', value=f'书名：爬取失败')
            self.msgbox(target='author_label', value=f'作者：爬取失败')
            self.msgbox(target='notice_label', value=f'提示：无法访问内容，书籍目录页面爬取失败。')
            return False
        ## 爬取书籍名称
        if self.title_of_book == '':
            title_of_book = self.extract_word(response, self.regx_of_book_title)
            if len(title_of_book) == 0:
                self.msgbox(target='title_label', value=f'书名：爬取失败')
                self.msgbox(target='author_label', value=f'作者：爬取失败')
                self.msgbox(target='notice_label', value=f'提示：书籍标题爬取失败。')
                return False
            title_of_book = title_of_book[0]
            self.title_of_book = title_of_book
        ## 爬取书籍作者
        if self.author_of_book == '':
            author_of_book = self.extract_word(response, self.regx_of_book_author)
            if len(author_of_book) == 0:
                self.msgbox(target='author_label', value=f'作者：爬取失败')
                self.msgbox(target='notice_label', value=f'提示：书籍作者爬取失败。')
                return False
            author_of_book = author_of_book[0]
            self.author_of_book = author_of_book
        ## 爬取书籍目录
        if True:
            href_of_chapters = self.extract_word(response, self.regx_of_chap_href)
            if len(href_of_chapters) == 0:
                self.msgbox(target='notice_label', value=f'提示：书籍目录链接爬取内容失败。')
                return False
            if isinstance(href_of_chapters[0], tuple):
                url_of_chapters = [self.base_url + href[0] if href[0] != '' else href[1] for href in href_of_chapters]
            else:
                url_of_chapters = [self.base_url + href for href in href_of_chapters]
            url_of_chapters = url_of_chapters[self.key_of_content['start']: self.key_of_content['stop']: self.key_of_content['step']]
            url_of_chapters = self.remove_duplication(url_of_chapters)
            self.url_of_chapters.extend(url_of_chapters)
        return True

    ## 保存小说及报告
    def save_novel(self):
        ## 输出文件编码格式
        output_encoding = 'UTF-8'
        ## 统计字数
        word_count_of_book = 0
        for key in self.content.keys():
            word_count_of_book += self.content[key].word_count
        ## 章节：书籍信息
        self.content[-3] = ChapterContent()
        self.content[-3].title = f'书籍信息'
        self.content[-3].content = f'　　书名：{self.title_of_book} \n　　作者：{self.author_of_book} \n　　字数：{word_count_of_book / 10000:.1f}万 \n　　校对：小说爬虫 v1.0 \n'
        ## 章节：免责声明
        self.content[-2] = ChapterContent()
        self.content[-2].title = f'声明'
        self.content[-2].content = f'　　文本资源来源于网络，只是因个人兴趣而校对本书，未经作者授权，仅供广大网友试读之用。\n　　版权属于原作者/网站/出版社，禁止任何形式的组织或个人以盈利为目的传播本书，本书文本提供、校对、制作者不承担法律及连带责任。\n　　如果喜欢这本书，请支持作者，购买VIP内容。\n'
        ## 分卷：正文卷
        if self.content[self.start_chapter].content != '':
            self.content[-1] = ChapterContent()
            self.content[-1].title = f'正文卷'
            self.content[-1].content = f''
        ## 创建目录
        if not os.path.exists(self.novel_path):
            os.mkdir(self.novel_path)
        if not os.path.exists(self.report_path):
            os.mkdir(self.report_path)
        ## 打开小说文件和报告文件
        novel = open(f'{self.novel_path}{os.sep}{self.title_of_book}.txt', 'w', encoding=output_encoding)
        report = open(f'{self.report_path}{os.sep}{self.title_of_book}_report.txt', 'w', encoding=output_encoding)
        ## 按照顺序写入小说章节和报告
        keys_of_chapters_of_book = sorted(self.content.keys())
        for key in keys_of_chapters_of_book:
            chapter_content = self.content[key]
            ## 写入小说章节
            novel.write(chapter_content.title)
            novel.write('\n')
            novel.write(chapter_content.content)
            novel.write('\n\n')
            ## 如果报告为空，不写入报告
            if chapter_content.report_title == '' and chapter_content.report_content == '':
                continue
            ## 写入小说报告
            report.write(chapter_content.report_title)
            report.write('\n')
            report.write(chapter_content.report_content)
            report.write('\n\n')
        ## 关闭文档
        novel.close()
        report.close()
        ## 确认报告是否存在
        report_exist = True
        with open(f'{self.report_path}{os.sep}{self.title_of_book}_report.txt', 'r', encoding=output_encoding) as fin:
            for line in fin:
                if line != '\n':
                    break
            else:
                report_exist = False
        ## 若报告没有实质内容，则删除报告
        if report_exist == False:
            os.remove(f'{self.report_path}{os.sep}{self.title_of_book}_report.txt')

    ## 整合所有函数，爬取小说
    def crawl_novel(self):
        ## 根据url调整参数
        if self.auto_setting(self.url_of_book) == False:
            self.msgbox(target='title_label', value=f'书名：爬取失败')
            self.msgbox(target='author_label', value=f'作者：爬取失败')
            self.msgbox(target='notice_label', value=f'提示：该书籍链接不属于预定义范围，爬取失败。')
            return False
        ## 通过url爬取【书籍信息】以及【所有章节的链接】
        if self.crawl_content_page() == False:
            return False
        ## 确认爬取章节的范围
        self.start_chapter = 0 if self.num_of_chapters_wanted <= 0 else len(self.url_of_chapters) - self.num_of_chapters_wanted
        self.stop_chapter = len(self.url_of_chapters)
        self.total_chapter = self.stop_chapter - self.start_chapter
        ## 限制速度
        if self.speed_of_crawling > 10:
            self.__speed_of_crawling = 10
        ## 定义访问率
        access_rate = 1 / self.speed_of_crawling
        ## 输出书籍信息到屏幕上
        self.msgbox(target='title_label', value=f'书名：{self.title_of_book}')
        self.msgbox(target='author_label', value=f'作者：{self.author_of_book}')
        ## 多线程爬取章节
        for idx in range(self.start_chapter, self.stop_chapter):
            ## 进行判定，是否终止程序
            if self.state == False:
                return False
            ## 显示进度条
            self.status_bar()
            url_of_chapter = self.url_of_chapters[idx]
            self.content[idx] = ChapterContent(url=url_of_chapter)
            if 'http' not in url_of_chapter:
                self.content[idx].title = url_of_chapter
                self.content[idx].ready = True
                continue
            try:
                thread = threading.Thread(target=self.crawl_chapter_page, args=(self.content[idx],))
                thread.start()
            except:
                self.content[idx].title = self.content[idx].report_title = f'第{idx + 1}节 线程启动失败'
                self.content[idx].content = self.content[idx].report_content = f'网址: {url_of_chapter}'
            finally:
                time.sleep(access_rate)
        ## 等待线程执行完毕
        while len(self) < self.total_chapter and time.time() - self.__last_modify_time < 60:
            ## 进行判定，是否终止程序
            if self.state == False:
                return False
            time.sleep(0.1)
            self.status_bar()
        self.status_bar()
        self.msgbox(target='notice_label', value=f'提示：【{self.title_of_book}】爬取完毕，保存文件中。')
        try:
            ## 保存文件
            self.save_novel()
            time.sleep(0.5)
            ## 生成提示
            self.msgbox(target='notice_label', value=f'提示：【{self.title_of_book}】爬取完毕，TXT文件已保存。')
        except:
            ## 生成提示
            self.msgbox(target='notice_label', value=f'提示：【{self.title_of_book}】爬取完毕，TXT文件保存失败。')
        finally:
            time.sleep(0.5)
        return True

    ## 预定义指定网站的参数
    def auto_setting(self, url):
        if r'aabook.xyz' in url:
            self.url_of_book = url
            self.base_url = r'https://aabook.xyz/'
            self.encode = r'UTF-8'
            self.regx_of_book_title = [r'<h1 class="index_title">(.*?)</h1>']
            self.regx_of_book_author = [r'<p class="index_info"><span>作者：(.*?)</span></p>']
            self.regx_of_chap_href = [r'<p class="index_info">.*?<p class="section_title">作品相关</p>(.*?)<p class="section_title">性福宝排行榜</p>', r'<li><a href="(.*?)" title=.*?</a></li>|<p class="section_title">(.*?)</p>']
            self.key_of_content = {'start': 0, 'stop': None, 'step': 1}
            self.regx_of_chap_title = [r'<h1 class="chapter_title">(.*?)</h1>']
            self.regx_of_chap_content = [r'<div class="chapter_con" id="chapter_content">(.*?)</div>',r'<p>(.*?)</p>']
            self.speed_of_crawling = 0.6
            self.crawler_mode = 'selenium'
        elif r'www.31xs.net' in url:
            self.url_of_book = url
            self.base_url = r'https://www.31xs.net'
            self.encode = r'UTF-8'
            self.regx_of_book_title = [r'<meta property="og:novel:book_name" content="(.*?)" />']
            self.regx_of_book_author = [r'<meta property="og:novel:author" content="(.*?)" />']
            self.regx_of_chap_href = [r'<dd><a href="(.*?)">.*?</a></dd>']
            self.key_of_content = {'start': 0, 'stop': None, 'step': 1}
            self.regx_of_chap_title = [r'<h1>(.*?)</h1>']
            self.regx_of_chap_content = [r'<p>(.*?)</p>']
            self.speed_of_crawling = 30
            self.crawler_mode = 'requests'
        elif r'www.ptwxz.com' in url:
            self.url_of_book = url
            self.base_url = url
            self.encode = r'ANSI'
            self.regx_of_book_title = ['<h1>(.*?)最新章节</h1>']
            self.regx_of_book_author = ['作者：(.*?) &nbsp; &nbsp;']
            self.regx_of_chap_href = ['<li><a href="(.*?)">']
            self.key_of_content = {'start': 0, 'stop': None, 'step': 1}
            self.regx_of_chap_title = [r'<[Hh]1><a href=".*?">.*</a>(.*?)</[Hh]1>']
            self.regx_of_chap_content = [r'&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<']
            self.speed_of_crawling = 30
            self.crawler_mode = 'requests'
        elif r'www.uuks.org' in url:
            self.url_of_book = url
            self.base_url = r'https://www.uuks.org'
            self.encode = r'UTF-8'
            self.regx_of_book_title = [r'<h3>《(.*?)》正文</h3>']
            self.regx_of_book_author = [r'<h2>作者：(.*?)</h2>']
            self.regx_of_chap_href = [r'<div class="box_con">.*?</div>(.*?)</div>', r'<li><a href="(.*?)">.*?</a></li>']
            self.key_of_content = {'start': 0, 'stop': None, 'step': 1}
            self.regx_of_chap_title = [r'<h1 id="timu">(.*?)</h1>']
            self.regx_of_chap_content = [r'<p>(.*?)</p>']
            self.speed_of_crawling = 30
            self.crawler_mode = 'requests'
        elif r'www.bqxs520.com' in url:
            self.url_of_book = url
            self.base_url = r'http://www.bqxs520.com'
            self.encode = r'UTF-8'
            self.regx_of_book_title = [r'<h1>(.*?)</h1>']
            self.regx_of_book_author = [r'<p>作.*?者：(.*?)</p>']
            self.regx_of_chap_href = [r'<dd><a href="(.*?)">']
            self.key_of_content = {'start': 9, 'stop': None, 'step': 1}
            self.regx_of_chap_title = [r'<h1>\s?(.*?)</h1>']
            self.regx_of_chap_content = [r'br\s*/>(.*?)<']
            self.speed_of_crawling = 30
            self.crawler_mode = 'requests'
        elif r'www.ibiquge.net' in url:
            self.url_of_book = url
            self.base_url = r'https://www.ibiquge.net'
            self.encode = r'UTF-8'
            self.regx_of_book_title = [r'<h1>(.*?)</h1>']
            self.regx_of_book_author = [r'<p>作.*者：.*?<a href=".*?">(.*?)</a>.*?</p>']
            self.regx_of_chap_href = [r'<dd> <a style="" href="(.*?)">']
            self.key_of_content = {'start': 12, 'stop': None, 'step': 1}
            self.regx_of_chap_title = [r'<h1>(.*?)</h1>']
            self.regx_of_chap_content = [r'&nbsp;(.*?)<|\s']
            self.speed_of_crawling = 20
            self.crawler_mode = 'requests'
        else:
            self.url_of_book = url
            self.base_url = r''
            self.encode = r'UTF-8'
            self.regx_of_book_title = [r'']
            self.regx_of_book_author = [r'']
            self.regx_of_chap_href = [r'']
            self.key_of_content = {'start': 0, 'stop': None, 'step': 1}
            self.regx_of_chap_title = [r'']
            self.regx_of_chap_content = [r'']
            self.speed_of_crawling = 50
            self.crawler_mode = 'requests'
            return False
        return True

    ## 用来测试 requests 和 selenium 获取的html文档有何不同
    def test(self, url, encode, crawler_mode = 'requests'):
        self.encode = encode
        self.crawler_mode = crawler_mode
        self.title_of_book = '网页响应'
        self.author_of_book = url
        self.content[0] = ChapterContent()
        self.content[0].title = f'网页响应'
        self.content[0].content = self.get_response(url)
        self.save_novel()

    def get_page(self, url):
        self.content[0] = ChapterContent()
        self.content[0].url = url
        self.auto_setting(url)
        self.start_chapter = 0
        self.crawl_chapter_page(self.content[0])
        self.novel_path = os.getcwd() + os.sep + "fiction_report"
        self.save_novel()


if __name__ == "__main__":
    url = input("url: ")
    print("start crawling")
    NovelSpider().get_page(url)



