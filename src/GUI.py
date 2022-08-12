# -*- coding:utf-8 -*-
import os
import re
import sys
import time
import webbrowser
import NovelSpider
import threading
from tkinter import *
from tkinter import ttk
from tkinter.tix import *
from itertools import chain
from PIL import Image, ImageTk
from tkinter import font as tkFont
from pypinyin import pinyin, Style
from tkinter.scrolledtext import ScrolledText

## book_info.html 的格式定义
html_prefix =\
'''
<!DOCTYPE HTML>
<html>

  <head>

    <meta charset="utf-8" / >

    <title>我的书单</title>

    <base target="_blank" />

    <!-- no link -->

    <meta name="author" content="小说爬虫" />
    <meta name="generator" content="小说爬虫" />
    <meta name="description" content="用户自定义的书单" />
    <meta name="keywords" content="自定义书单,爬虫" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- no script -->

    <style type="text/css" media="screen">
	
	* {
	   box-sizing: border-box;
    }

    body {
      background: rgb(231, 212, 182) url(https://github.com/Henryyy-Hung/Web-Crawler-of-Chinese-Fiction/blob/main/src/img/wood.jpg?raw=true) repeat fixed top left;
      <!--
      background-image: linear-gradient(to right top, rgb(155, 196, 202), rgb(180, 209, 213), rgb(220, 240, 249), rgb(180, 209, 213), rgb(155, 196, 202));
      //-->
      background-attachment: fixed;
      --fontsize: 24px;
      font-size: var(--fontsize);
    }

    .noselect {
      -webkit-touch-callout: none;
      -webkit-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
      user-select: none;
    }

    .container {
      max-width: 70%;
      margin: 50px 0px;
      background-color: rgba(255, 255, 255, 0.7);
      border-radius: 30px;
      margin-left: auto;
      margin-right: auto;
      box-shadow: 0px 0px 15px black;
      padding: 30px;
    }

    .header {
      color:black;
      text-align:center;
      font-size: 2em;
      font-weight: 600;
    }

    .book_list {
      margin: 2em auto;
    }

    dl {
      list-style-type:none;
      counter-reset: list_num;
      text-align: justify;
      text-align-last: justify;
    }

    dt {
      display: inline-block;
      text-align: left;
      text-align-last: left;
      vertical-align: top;
      width: 15em;
    }

    dt>a {
      animation: fade-in 1s ease-in 0s 1 normal;
      animation-fill-mode: both;
      <!--
      animation-name: fade-in;
      animation-duration: 1s;
      animation-timing-function: ease-in;
      animation-delay: 0s;
      animation-iteration-count: 1;
      animation-direction: normal;
      //-->
    }

    dt>a::before {
      counter-increment: list_num;
      content: counter(list_num) ". ";
    }

    dt>a {
      display: inline-block;
      border-radius: 10px;
      padding: 10px;
      width: 15em;
      white-space: normal;
      text-overflow:ellipsis;
      white-space: nowrap;
      overflow: hidden;
    }

    dt>a:link, dt>a:visited, dt>a:active, dt>a:hover {
      color: black;
      background-color: transparent;
      text-decoration: none;
    }

    dt>a:hover {
      background-color: rgba(255,255,255,0.5);
      white-space: normal;
      position: relative;
      transform: scale(1.05,1.05);
      transition-duration: 0.15s;
      z-index: 2147483647;
    }

    dt>a:active {
      background-color: rgba(255,255,255,1);
      box-shadow: 0 0 10px 1px rgba(0, 140, 186, 0.5);
    }

    .footer {
      text-align: center;
      margin-top: 20px;
    }

    address>a:link, address>a:visited, address>a:active, address>a:hover {
      animation-name: shift_color;
      animation-duration: 1s;
      animation-iteration-count: infinite;
      animation-direction: alternate;
    }

    @keyframes shift_color {
      0% {color: black;}
      100% {color: blue;}
    }

    @keyframes fade-in {
      0% {opacity: 0;}
      100% {opacity: 1;}
    }
    </style>

  </head>

  <body class="noselect">

    <div class="container">

      <div class="header">
          我的书单
      </div>

      <hr />

      <div class="book_list">
        <dl>
'''

html_postfix =\
'''        <dt></dt>
        <dt></dt>
        <dt></dt>
        <dt></dt>
        <dt></dt>
        <dt></dt>
        <dt></dt>
        <dt></dt>
        <dt></dt>

        </dl>
      </div>

      <hr />

      <div class="footer">
          <address>
            <a href="https://github.com/Henryyy-Hung/Web-Spider-of-Chinese-Fiction" id="source">点此跳转至软件主页</a>
          </address>
      </div>

    </div>

  </body>

</html>
'''

## 用于爬取网络小说的爬虫对象
class SpiderGUI(object):

    ## 初始化窗口
    def __init__(self):
        ## 设置选项容器
        self.choice_buttons = []

        self.book_info = dict()
        ## 载入历史记录
        if os.path.exists('book_info.html'):
            self.load_info_list()

        ## 预定义主窗口变量
        self.background_color = '#bdc0c8'
        self.master_frame_title = '小说爬虫  v1.1.5'
        self.master_frame_width = 600
        self.master_frame_height = 450
        self.master_icon_path = self.get_resource_path(f'{"img"}{os.sep}{"icon.ico"}') #f'{os.getcwd()}{os.sep}{"img"}{os.sep}{"icon.ico"}'

        ## 设置主窗口
        self.master = Tk()
        self.master.title(self.master_frame_title)
        self.master.iconbitmap(self.master_icon_path)
        self.screenwidth = self.master.winfo_screenwidth()
        self.screenheight = self.master.winfo_screenheight()
        alignstr = f'{int(self.master_frame_width)}x{int(self.master_frame_height)}+{int((self.screenwidth-self.master_frame_width)/2)}+{int((self.screenheight-self.master_frame_height)/2)}'
        self.master.geometry(alignstr)
        self.master.minsize(width=self.master_frame_width, height=self.master_frame_height)
        self.master.attributes('-alpha', 0.9)

        ## 进行窗口划分
        ## 一级下方窗口
        self.level_1_N_frame = Frame(master=self.master, bg=self.background_color)
        self.level_1_N_frame.place(relx=0.5, rely=0.4, relwidth=1.0, relheight=0.8, anchor=CENTER)
        ## 一级上方窗口
        self.level_1_S_frame = Frame(master=self.master, bg=self.background_color)
        self.level_1_S_frame.place(relx=0.5, rely=0.9, relwidth=1.0, relheight=0.2, anchor=CENTER)
        ## 二级左边窗口
        self.level_2_W_frame = Frame(master=self.level_1_N_frame, bg=self.background_color)
        self.level_2_W_frame.place(relx=0.4, rely=0.5, relwidth=0.8, relheight=1.0, anchor=CENTER)
        ## 二级右边窗口
        self.level_2_E_frame = Frame(master=self.level_1_N_frame, bg=self.background_color)
        self.level_2_E_frame.place(relx=0.9, rely=0.5, relwidth=0.2, relheight=1.0, anchor=CENTER)
        ## 三级左上窗口
        self.level_3_NW_frame = Frame(master=self.level_2_W_frame, bg=self.background_color)
        self.level_3_NW_frame.place(relx=0.5, rely=0.425, relwidth=1.0, relheight=0.85, anchor=CENTER)
        ## 三级左下窗口
        self.level_3_SW_frame = Frame(master=self.level_2_W_frame, bg=self.background_color)
        self.level_3_SW_frame.place(relx=0.5, rely=0.925, relwidth=1.0, relheight=0.15, anchor=CENTER)
        ## 三级右上窗口
        self.level_3_NE_frame = Frame(master=self.level_2_E_frame, bg=self.background_color)
        self.level_3_NE_frame.place(relx=0.5, rely=0.425, relwidth=1.0, relheight=0.85, anchor=CENTER)
        ## 三级右下窗口
        self.level_3_SE_frame = Frame(master=self.level_2_E_frame, bg=self.background_color)
        self.level_3_SE_frame.place(relx=0.5, rely=0.925, relwidth=1.0, relheight=0.15, anchor=CENTER)
        ## 四级中心窗口
        self.level_4_input_frame = Frame(master=self.level_3_SW_frame, bg=self.background_color)
        self.level_4_input_frame.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=1.0, anchor=CENTER)

        ## 预定义按键变量
        self.button_font = tkFont.Font(size=15, weight='bold')
        self.button_background_color = '#7d90a5'
        self.button_activebackground_color = '#707c94'
        self.button_foreground_color = 'white'
        self.button_activeforeground_color = 'white'
        self.button_border_width = 5

        ## 创建按钮
        ## 爬虫启动按钮
        self.start_button = Button(master=self.level_1_S_frame, text="开始下载", command=self.start_crawling, font=self.button_font, bg=self.button_background_color, fg=self.button_foreground_color, activebackground=self.button_activebackground_color, activeforeground=self.button_activeforeground_color, borderwidth=self.button_border_width)
        self.start_button.place(anchor=CENTER, relx=0.5, rely=0.5, relwidth=0.4, relheight=0.6)
        ## 添加书籍资料按钮
        self.add_book_button = Button(master=self.level_3_SE_frame, text="添加数据", command=self.add_book, font=self.button_font,bg=self.button_background_color, fg=self.button_foreground_color, activebackground=self.button_activebackground_color, activeforeground=self.button_activeforeground_color, borderwidth=self.button_border_width)
        self.add_book_button.place(anchor=CENTER, relx=0.5, rely=0.5, relwidth=0.9, relheight=0.7)
        ## 全选表单按钮
        self.select_all_button = Button(master=self.level_3_NE_frame, text="全选书单", command=self.select_all, font=self.button_font,bg=self.button_background_color, fg=self.button_foreground_color, activebackground=self.button_activebackground_color, activeforeground=self.button_activeforeground_color, borderwidth=self.button_border_width)
        self.select_all_button.place(anchor=CENTER, relx=0.5, rely=0.1, relwidth=0.9, relheight=0.125)
        ## 全不选表单按钮
        self.reverse_selected_button = Button(master=self.level_3_NE_frame, text="反向选择", command=self.reverse_selected, font=self.button_font,bg=self.button_background_color, fg=self.button_foreground_color, activebackground=self.button_activebackground_color, activeforeground=self.button_activeforeground_color, borderwidth=self.button_border_width)
        self.reverse_selected_button.place(anchor=CENTER, relx=0.5, rely=0.3, relwidth=0.9, relheight=0.125)
        ## 删除选中表单按钮
        self.delete_selected_button = Button(master=self.level_3_NE_frame, text="删除已选", command=self.delete_selected, font=self.button_font,bg=self.button_background_color, fg=self.button_foreground_color, activebackground=self.button_activebackground_color, activeforeground=self.button_activeforeground_color, borderwidth=self.button_border_width)
        self.delete_selected_button.place(anchor=CENTER, relx=0.5, rely=0.5, relwidth=0.9, relheight=0.125)
        ## 保存表单按钮
        self.save_info_list_button = Button(master=self.level_3_NE_frame, text="保存书单", command=self.save_info_list, font=self.button_font,bg=self.button_background_color, fg=self.button_foreground_color, activebackground=self.button_activebackground_color, activeforeground=self.button_activeforeground_color, borderwidth=self.button_border_width)
        self.save_info_list_button.place(anchor=CENTER, relx=0.5, rely=0.7, relwidth=0.9, relheight=0.125)
        ## 打赏按钮
        self.open_save_path_button = Button(master=self.level_3_NE_frame, text="查看文件", command=self.open_save_path, font=self.button_font,bg=self.button_background_color, fg=self.button_foreground_color, activebackground=self.button_activebackground_color, activeforeground=self.button_activeforeground_color, borderwidth=self.button_border_width)
        self.open_save_path_button.place(anchor=CENTER, relx=0.5, rely=0.9, relwidth=0.9, relheight=0.125)

        ## 预定义输入框变量
        self.entry_font = tkFont.Font(size=15, weight='bold')
        self.entry_border_width = 5

        ## 创建输入框
        ## 书名输入框
        self.book_title_entry = Entry(master=self.level_4_input_frame, font=self.entry_font, borderwidth=self.entry_border_width)
        self.book_title_entry.place(anchor=CENTER, relx=0.15, rely=0.5, relwidth=0.3, relheight=0.7)
        self.book_title_entry.insert(0, '书名')
        self.book_title_entry.bind("<Button-1>", self.clear_book_title_entry_text)
        self.book_title_entry.bind("<FocusIn>", self.clear_book_title_entry_text)
        self.book_title_entry.bind("<KeyPress>", self.clear_book_title_entry_text)
        ## 链接输入框
        self.book_url_entry = Entry(master=self.level_4_input_frame, font=self.entry_font, borderwidth=self.entry_border_width)
        self.book_url_entry.place(anchor=CENTER, relx=0.6725, rely=0.5, relwidth=0.655, relheight=0.7)
        self.book_url_entry.insert(0, '链接')
        self.book_url_entry.bind("<Button-1>", self.clear_book_url_entry_text)
        self.book_url_entry.bind("<FocusIn>", self.clear_book_url_entry_text)
        self.book_url_entry.bind("<KeyPress>", self.clear_book_url_entry_text)
        ## 允许使用ENTER键进行输入
        self.book_title_entry.bind('<KeyRelease-Return>', lambda e: e.widget.tk_focusNext().focus())
        self.book_url_entry.bind('<KeyRelease-Return>', lambda e: self.add_book())

        ## 创建滚动面板
        self.choice_panel = ScrolledText(master=self.level_3_NW_frame, selectbackground='white', selectforeground='blue', cursor="arrow", wrap=NONE)
        self.choice_panel.place(anchor=CENTER, relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95)

        ## 列表选项变量
        self.choice_button_font = tkFont.Font(size=13, weight='bold')
        self.choice_button_background_color = 'white'

        ## 爬取最近100章选项框
        var = IntVar()
        self.latest_chapter_only_check_button = Checkbutton(master=self.level_1_S_frame, text="仅最新100章", bg=self.background_color, activebackground=self.background_color, anchor='w', font=self.choice_button_font, variable=var, onvalue=1, offvalue=0)
        self.latest_chapter_only_check_button.var = var
        self.latest_chapter_only_check_button.place(anchor=W, relx=0.75, rely=0.5)

        ## 创建选项列表
        for book_name in sorted(self.book_info.keys(), key=self.to_pinyin, reverse=True):
            self.create_choice_button(book_title=book_name)
        ## 允许编辑缓存区
        self.choice_panel.config(state=NORMAL)
        ## 在结尾加上空行
        self.choice_panel.insert(END, '\n\n')
        ## 禁止编辑缓存区
        self.choice_panel.config(state=DISABLED)


        def link_to_github_scroll_handler(event):
            if self.choice_panel.vbar.get()[0] == 0.0:
                self.link_to_github.place(anchor=N, relx=0.5, rely=0)
            else:
                self.link_to_github.place_forget()
        ## 创建使用说明链接
        self.link_to_github = Label(self.choice_panel, text="点此参阅使用说明", bg=self.background_color, fg='black')
        self.link_to_github.bind("<Button-1>", lambda e: webbrowser.open_new_tab("https://github.com/Henryyy-Hung/Web-Crawler-of-Chinese-Fiction"))
        self.link_to_github.place(anchor=N, relx=0.5, rely=0)
        self.choice_panel.bind("<MouseWheel>", link_to_github_scroll_handler)

        ## 创建提示标签
        tips = []
        self.start_button_tip = Balloon(master=self.level_1_S_frame)
        self.start_button_tip.bind_widget(self.start_button, balloonmsg="点此启动爬虫，下载选中书籍。")
        tips.append(self.start_button_tip)

        self.start_button_tip = Balloon(master=self.level_1_S_frame)
        self.start_button_tip.bind_widget(self.latest_chapter_only_check_button, balloonmsg="勾选此处后，仅下载所选中书籍最新的100章。")
        tips.append(self.start_button_tip)

        self.add_book_button_tip = Balloon(master=self.level_3_SE_frame)
        self.add_book_button_tip.bind_widget(self.add_book_button, balloonmsg="点此将左侧【书名】及其对应【链接】加入可选下载项目。")
        tips.append( self.add_book_button_tip)

        self.save_info_list_button_tip = Balloon(master=self.level_3_NE_frame)
        self.save_info_list_button_tip.bind_widget(self.select_all_button, balloonmsg="选中左侧所有项目。")
        tips.append(self.save_info_list_button_tip)

        self.save_info_list_button_tip = Balloon(master=self.level_3_NE_frame)
        self.save_info_list_button_tip.bind_widget(self.reverse_selected_button, balloonmsg="取消左侧所有选中项目，选中左侧所有取消项目。")
        tips.append(self.save_info_list_button_tip)

        self.save_info_list_button_tip = Balloon(master=self.level_3_NE_frame)
        self.save_info_list_button_tip.bind_widget(self.delete_selected_button, balloonmsg="从左侧区域删除所有选中项目。")
        tips.append(self.save_info_list_button_tip)

        self.save_info_list_button_tip = Balloon(master=self.level_3_NE_frame)
        self.save_info_list_button_tip.bind_widget(self.save_info_list_button, balloonmsg="点此储存已添加的【书籍信息】，下次打开应用自动恢复。\n文件名为book_info，可在程序同目录下找到。")
        tips.append(self.save_info_list_button_tip)
        self.open_save_path_button_tip = Balloon(master=self.level_3_NE_frame)
        self.open_save_path_button_tip.bind_widget(self.open_save_path_button, balloonmsg="点此打开文件夹，查看已保存书籍。")
        tips.append(self.open_save_path_button_tip)
        self.book_title_entry_tip = Balloon(master=self.level_4_input_frame)
        self.book_title_entry_tip.bind_widget(self.book_title_entry, balloonmsg="请在此输入书名")
        tips.append(self.book_title_entry_tip)
        self.book_url_entry_tip = Balloon(master=self.level_4_input_frame)
        self.book_url_entry_tip.bind_widget(self.book_url_entry, balloonmsg="请在此处输入对应网文网址")
        tips.append(self.book_url_entry_tip)

        ## 编辑提示标签背景色
        for tip in tips:
            for sub in tip.subwidgets_all():
                sub.configure(bg='#dddddd')

        ## 开始循环显示
        mainloop()

    ## 添加多线程，防止阻塞mainloop()
    def start_crawling(self):
        thread = threading.Thread(target=self.release_spider, args=())
        thread.start()

    ## 释放爬虫
    def release_spider(self):
        ## 将待爬取书籍链接放入列表中
        urls = []
        for choice_button in self.choice_buttons.copy():
            if choice_button.var.get() == True:
                urls.append(self.book_info[choice_button.cget("text")])

        ## 如果没有链接，禁止启动爬虫
        if urls == []:
            return None

        ## 禁止同时启动第二只爬虫
        self.start_button['state'] = DISABLED
        self.latest_chapter_only_check_button['state'] = DISABLED

        ## 翻转顺序，先进先出
        urls = list(reversed(urls))
        ## 记录待下载书籍总量
        num_of_books = len(urls)
        ## 记录已下载书籍总量
        self.num_of_books_downloaded = 0

        ## 预定义定义弹窗变量
        top_background_color = 'white'
        top_forebackground_color = 'black'
        top_label_font = tkFont.Font(size=16, weight='bold')
        ## 定义进度条变量
        style = ttk.Style()
        style.theme_use('alt')
        style.configure("blue.Horizontal.TProgressbar", foreground='#5a768c', background='#5a768c')
        style.configure("red.Horizontal.TProgressbar", foreground='#958268', background='#958268')

        ## 创建弹窗
        self.top = Toplevel(master=self.master, bg=top_background_color)
        self.top.title('小说下载进度')
        top_level_width = 500
        top_level_height = 200
        alignstr = f'{int(top_level_width)}x{int(top_level_height)}+{int((self.screenwidth - top_level_width) / 2)}+{int((self.screenheight - top_level_height) / 2)}'
        self.top.geometry(alignstr)
        self.top.iconbitmap(self.master_icon_path)
        self.top.attributes('-alpha', 0.9)
        self.top.resizable(False, False)
        ## self.top.grab_set()  # 置顶页面
        self.top.wm_transient(self.master) ## 始终置顶

        ## 创建标签
        self.title_label = Label(master=self.top, text="书名：等待响应中...", bg=top_background_color, fg=top_forebackground_color, font=top_label_font, anchor=W)
        self.title_label.place(anchor=CENTER, relx=0.5, rely=0.2, relwidth=0.9, relheight=0.2)
        self.author_label = Label(master=self.top, text="作者：等待响应中...", bg=top_background_color, fg=top_forebackground_color, font=top_label_font, anchor=W)
        self.author_label.place(anchor=CENTER, relx=0.5, rely=0.4, relwidth=0.9, relheight=0.2)
        self.notice_label =  Label(master=self.top, text="提示：等待响应中...", bg=top_background_color, fg=top_forebackground_color, anchor=W)
        self.notice_label.place(anchor=CENTER, relx=0.5, rely=0.9, relwidth=0.9, relheight=0.15)

        ## 创建进度条
        self.progress_bar = ttk.Progressbar(master=self.top, maximum=10000, value=0, style="blue.Horizontal.TProgressbar")
        self.progress_bar.place(anchor=CENTER, relx=0.5, rely=0.65, relwidth=0.9, relheight=0.2)

        ## 关闭窗口时的动作
        def on_closing():
            ## 更新时间戳，使在该时间戳之前创建的爬虫无法向GUI传递信息，以及时间戳之前创建的爬虫释放for循环停止
            self.start_time_ns = time.time_ns()
            ## 摧毁所有弹窗组件
            self.title_label.destroy()
            self.author_label.destroy()
            self.progress_bar.destroy()
            self.notice_label.destroy()
            self.top.destroy()
            ## 重新允许用户进行操作
            self.start_button['state'] = ACTIVE
            self.latest_chapter_only_check_button['state'] = ACTIVE
            return None

        ## 绑定关闭窗口与on_closing函数
        self.top.protocol("WM_DELETE_WINDOW", on_closing)

        ## 记录启动时间
        start_time = time.time()
        ## 记录启动时间（纳秒级别）
        self.start_time_ns = time.time_ns()
        ## 复制启动时间（纳秒级别）并保持不变
        start_time_ns = self.start_time_ns
        num_of_books_downloaded = self.num_of_books_downloaded

        ## 开始爬取书籍
        for idx in range(0, num_of_books):
            ## 如果启动时间被更新，代表本次爬取已经结束，不启动余下任何爬虫
            if start_time_ns != self.start_time_ns:
                break
            ## 赋予当前url
            url = urls[idx]
            ## 每当上一次爬取结束，刷新页面信息
            self.title_label['text'] = "书名：等待响应中..."
            self.author_label['text'] = "作者：等待响应中..."
            self.progress_bar['value'] = 0
            self.notice_label['text'] = "提示：等待响应中..."
            ## 创建爬虫
            spider = NovelSpider.NovelSpider(self)
            spider.url_of_book = url
            ## 启动只爬取最后一百章
            if self.latest_chapter_only_check_button.var.get() == True:
                spider.num_of_chapters_wanted = 100
            ## 启动爬虫
            spider.crawl_novel()
            ## 删除爬虫
            del spider
            ## 爬取后取消勾选
            if self.num_of_books_downloaded - num_of_books_downloaded == 1:
                for choice_button in self.choice_buttons:
                    if self.book_info[choice_button.cget("text")] == url:
                        choice_button.deselect()
                        break
            ## 重新赋值
            num_of_books_downloaded = self.num_of_books_downloaded

        ## 更新时间信息
        current_time = time.time()
        time_used = current_time - start_time
        hours_used = time_used // 3600
        minutes_used = (time_used % 3600) // 60
        seconds_used = time_used % 60
        ## 写入信息
        if self.num_of_books_downloaded == 0:
            msg = f'下载失败\n\n若非手动终止\n\n请重新参阅使用说明'
        elif hours_used > 99:
            msg = f'合计: {self.num_of_books_downloaded}本书\n\n耗时: {hours_used:0>1.0f}时{minutes_used:0>2.0f}分\n\n打个赏吧！求求了！'
        elif hours_used > 0:
            msg = f'合计: {self.num_of_books_downloaded}本书\n\n耗时: {hours_used:0>1.0f}时{minutes_used:0>2.0f}分{seconds_used:0>2.0f}秒\n\n打个赏吧！求求了！'
        elif minutes_used > 0:
            msg = f'合计: {self.num_of_books_downloaded}本书\n\n耗时: {minutes_used:0>2.0f}分{seconds_used:0>2.0f}秒\n\n打个赏吧！求求了！'
        else:
            msg = f'合计: {self.num_of_books_downloaded}本书\n\n耗时: {seconds_used:0>2.0f}秒\n\n打个赏吧！求求了！'

        ## 关闭程序
        on_closing()
        ## 显示弹窗
        self.pop_window(msg)

    ## 打赏页面
    def pop_window(self, msg):
        ## 预定义弹窗变量
        top_background_color = 'white'
        top_forebackground_color = 'black'
        top_label_font = tkFont.Font(size=16, weight='bold')
        ## 创建弹窗
        top = Toplevel(master=self.master, bg=top_background_color)
        top.title('小说下载结果')
        top_level_width = 500
        top_level_height = 200
        top.iconbitmap(self.master_icon_path)
        alignstr = f'{int(top_level_width)}x{int(top_level_height)}+{int((self.screenwidth - top_level_width) / 2)}+{int((self.screenheight - top_level_height) / 2)}'
        top.geometry(alignstr)
        top.grab_set()  # 置顶页面
        top.attributes('-alpha', 0.9)
        top.resizable(False, False)
        ## 创建二维码窗口
        qr_code_path = self.get_resource_path(f'{"img"}{os.sep}{"sponsorship.png"}')
        global qr_code
        qr_code = ImageTk.PhotoImage(Image.open(qr_code_path))
        qr_code_label = Label(master= top, image=qr_code, text="微信赞赏码", compound='bottom')
        qr_code_label.place(anchor=W, relx=0.1, rely=0.5)
        ## 创建文字窗口
        text_label = Label(master=top, text=f"{msg}", font=top_label_font, bg='white', justify=LEFT)
        text_label.place(anchor=W, relx=0.5, rely=0.5)

    ## 将书籍从输入框添加进缓存区
    def add_book(self):
        title = self.book_title_entry.get()
        url = self.book_url_entry.get()
        title = title.replace("\n", "")
        if title != '书名' and url != "链接" and "http" in url:
            if title not in self.book_info.keys():
                self.create_choice_button(book_title=title, book_url=url, selected=True)
            else:
                self.book_info[title] = url
            self.book_title_entry.delete(0, END)
            self.book_url_entry.delete(0, END)
            self.book_title_entry.insert(0, '书名')
            self.book_url_entry.insert(0, '链接')
            self.master.focus()
            ## 每次添加完书籍后移动到初始位置
            self.choice_panel.yview_moveto(0)

    ## 全选缓存区中所有书籍
    def select_all(self):
        for choice_button in self.choice_buttons:
            choice_button.select()

    ## 反选
    def reverse_selected(self):
        for choice_button in self.choice_buttons:
            if choice_button.var.get() == True:
                choice_button.deselect()
            else:
                choice_button.select()

    ## 删除选中项目
    def delete_selected(self):
        ## 允许编辑缓存区
        self.choice_panel.config(state=NORMAL)
        ## 删除已选项目，并且让其他项目消失
        for choice_button in self.choice_buttons.copy():
            value = choice_button.var.get()
            if  value == True:
                self.delete_choice_button(choice_button)
            else:
                choice_button.place_forget()
        ## 重新载入剩余项目
        for choice_button in self.choice_buttons:
            self.choice_panel.window_create('1.0', window=choice_button)
            self.choice_panel.insert('1.0', '\n\n  ')
        ## 清空多余空行
        self.choice_panel.delete(f'{2*len(self.choice_buttons)+2}.0', END)
        ## 在结尾加上空行
        self.choice_panel.insert(END, '\n\n')
        ## 禁止编辑缓存区
        self.choice_panel.config(state=DISABLED)
        ## 每次删除完书籍后移动到初始位置
        self.choice_panel.yview_moveto(0)

    ## 从书单中加载书籍和其对应链接
    def load_info_list(self):
        fin = open("book_info.html", 'r', encoding='UTF-8')
        regx = re.compile('<dt><a href="(?P<url>.*?)">(?P<title>.*?)</a></dt>')
        for line in fin.readlines():
            info = regx.search(line)
            if info != None:
                self.book_info[info.group('title')] = info.group('url')
        fin.close()

    ## 将缓存区书籍永久储存
    def save_info_list(self):
        fout = open("book_info.html", 'w', encoding='UTF-8')
        fout.write(html_prefix)
        for book_title in sorted(self.book_info.keys(), key=self.to_pinyin, reverse=False):
            fout.write(f'          <dt><a href="{self.book_info[book_title]}">{book_title}</a></dt>\n')
        fout.write(html_postfix)
        fout.close()

    ## 打开已保存的文件
    def open_save_path(self):
        self.novel_path = os.getcwd()+os.sep+'fiction'
        if not os.path.exists(self.novel_path):
            os.mkdir(self.novel_path)
        os.startfile(self.novel_path)

    ## 点击时清除书名栏说明文字
    def clear_book_title_entry_text(self, event):
        if self.book_title_entry.get() == '书名':
            self.book_title_entry.delete(0, END)

    ## 点击时清除链接栏说明文字
    def clear_book_url_entry_text(self, event):
        if self.book_url_entry.get() == '链接':
            self.book_url_entry.delete(0, END)

    ## 创建选项栏
    def create_choice_button(self, book_title="未知", book_url="", selected=False):
        ## 允许编辑缓存区
        self.choice_panel.config(state=NORMAL)
        ## 将书籍信息保存至容器
        if book_title not in self.book_info.keys():
            self.book_info[book_title] = book_url
        ## 创建选项
        var = IntVar()
        choice_button = Checkbutton(self.choice_panel, text=book_title, bg=self.choice_button_background_color, anchor='w', font=self.choice_button_font, variable=var, onvalue=1, offvalue=0, cursor="hand2")
        choice_button.var = var
        ## 根据需求来预选项目
        if selected==True:
            choice_button.select()
        else:
            choice_button.deselect()
        ## 将项目加入缓存区
        self.choice_buttons.append(choice_button)
        self.choice_panel.window_create('1.0', window=choice_button)
        self.choice_panel.insert('1.0', '\n\n  ')
        ## 禁止编辑缓存区
        self.choice_panel.config(state=DISABLED)

        ## 右键单击可编辑选项
        def RightClickChoiceButton(event):
            self.book_title_entry.delete(0, END)
            self.book_url_entry.delete(0, END)
            self.book_title_entry.insert(0, choice_button.cget("text"))
            self.book_url_entry.insert(0, self.book_info[choice_button.cget("text")])
            self.book_title_entry.xview_moveto(0)
            self.book_url_entry.xview_moveto(1)
        choice_button.bind("<Button-3>", RightClickChoiceButton)

        ## 右键双击选项可直接打开网页
        choice_button.bind("<Double-Button-3>", lambda e: webbrowser.open_new_tab(f'{self.book_info[choice_button.cget("text")]}'))

        ## 使得在图标上也能滚动候选区
        def OnMouseWheel(event):
            self.choice_panel.yview_scroll(int(-1*(event.delta/40)), "units")
            return "break"
        choice_button.bind("<MouseWheel>", OnMouseWheel)
        choice_button.bind("<Button-4>", OnMouseWheel)
        choice_button.bind("<Button-5>", OnMouseWheel)

        ## 设定选项的悬浮样式
        choice_button.bind('<Enter>', lambda e: choice_button.configure(bg=choice_button['activebackground']))
        choice_button.bind('<Leave>', lambda e: choice_button.configure(bg=self.choice_button_background_color))

    ## 删除选项栏
    def delete_choice_button(self, choice_button):
        ## 从容器中删除书籍信息
        book_title = choice_button.cget("text")
        if book_title in self.book_info.keys():
            del self.book_info[book_title]
        ## 删除选项
        self.choice_buttons.remove(choice_button)
        choice_button.place_forget()
        choice_button.destroy()

    ## 获取pyinstaller加载外部文件时的地址
    @staticmethod
    def get_resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    ## 使用拼音排序
    @staticmethod
    def to_pinyin(s):
        return ''.join(chain.from_iterable(pinyin(s, style=Style.TONE3)))
