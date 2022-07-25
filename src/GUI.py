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

html_prefix =\
'''
<!DOCTYPE HTML>
<html>

  <head>
  
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/ >
        
    <title>我的书单</title>
    
    <base target="_blank"/>
    
    <!-- no link -->
    
    <meta name="author" content="小说爬虫" />
    <meta name="generator" content="小说爬虫" />
    <meta name="description" content="用户自定义的书单" />
    <meta name="keywords" content="自定义书单,爬虫" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    
    <!-- no script -->
    
    <style type="text/css" media="screen">
    body {
    background-image:url(https://raw.githubusercontent.com/Henryyy-Hung/Web-Crawler-of-Chinese-Fiction/main/src/img/web_background.png);
    background-size: 234px 234px;
    background-attachment: fixed;
    }
    #header {
    color:black;
    text-align:center;
    text-shadow: 2px 2px 2px #bbbbbb;
    }
    #section {
    align:center;
    }
    #book_list {
    display: table;
    margin: 0 auto;
    font-size:x-large;
    max-width: 16em;
    }
    #footer {
    border-top: #bbbbbb solid 2px;
    background-image:url(https://raw.githubusercontent.com/Henryyy-Hung/Web-Crawler-of-Chinese-Fiction/main/src/img/web_background.png);
    color:black;
    text-align:right;
    position:fixed;
    bottom:0em;
    width:99%;
    padding: 0.5em 0 0.5em 0;
    }
    a:link {
    color: black;
    background-color: transparent;
    text-decoration: none;
    }
    a:visited {
    color: black;
    background-color: transparent;
    text-decoration: none;
    }
    a:hover {
    color: blue;
    background-color: transparent;
    text-decoration: none;
    }
    a:active {
    color: blue;
    background-color: transparent;
    text-decoration: none;
    }
    </style>
        
  </head>
    
  <body>
  
    <div id="header">
      <h1>我的书单</h1>
      <hr />
    </div>
    
    <div id="section">
      <div id="book_list">
        <ol>
'''

html_postfix =\
'''        </ol>
        <br />
      </div>
    </div>

    <div id="footer">
      <address>
        软件主页:&nbsp;<a href="https://github.com/Henryyy-Hung/Web-Spider-of-Chinese-Fiction"><i>点此跳转</i></a>&nbsp;<br />
      </address>
    </div>
    
  </body>

</html>
'''

## 用于爬取网络小说的爬虫对象
class SpiderGUI(object):

    def __init__(self):
        ## 设置选项容器
        self.choice_buttons = []

        self.book_info = dict()
        ## 载入历史记录
        if os.path.exists('book_info.html'):
            self.load_info_list()

        ## 预定义主窗口变量
        self.background_color = '#bdc0c8'
        self.master_frame_title = '小说爬虫  v1.1'
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
        self.cancel_select_all_button = Button(master=self.level_3_NE_frame, text="取消全选", command=self.cancel_select_all, font=self.button_font,bg=self.button_background_color, fg=self.button_foreground_color, activebackground=self.button_activebackground_color, activeforeground=self.button_activeforeground_color, borderwidth=self.button_border_width)
        self.cancel_select_all_button.place(anchor=CENTER, relx=0.5, rely=0.3, relwidth=0.9, relheight=0.125)
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
        ## 链接输入框
        self.book_url_entry = Entry(master=self.level_4_input_frame, font=self.entry_font, borderwidth=self.entry_border_width)
        self.book_url_entry.place(anchor=CENTER, relx=0.6725, rely=0.5, relwidth=0.655, relheight=0.7)
        self.book_url_entry.insert(0, '链接')
        self.book_url_entry.bind("<Button-1>", self.clear_book_url_entry_text)

        ## 创建滚动面板
        self.choice_panel = ScrolledText(master=self.level_3_NW_frame, selectbackground='white', selectforeground='blue')
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
        self.add_book_button_tip = Balloon(master=self.level_3_SE_frame)
        self.add_book_button_tip.bind_widget(self.add_book_button, balloonmsg="点此将左侧【书名】及其对应【链接】加入可选下载项目中。")
        tips.append( self.add_book_button_tip)
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
                sub.configure(bg='#cbcbc9')

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
        urls = reversed(urls)

        ## 预定义定义弹窗变量
        top_background_color = 'white'
        top_forebackground_color = 'black'
        top_label_font = tkFont.Font(size=16, weight='bold')
        ## 定义进度条变量
        style = ttk.Style()
        style.theme_use('alt')
        style.configure("blue.Horizontal.TProgressbar", foreground='#b6cbde', background='#b6cbde')

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
        ## self.top.wm_transient(self.master) ## 始终置顶

        ## 创建标签
        self.title_label = Label(master=self.top, text="书名：等待响应中...", bg=top_background_color, fg=top_forebackground_color, font=top_label_font, anchor=W)
        self.title_label.place(anchor=CENTER, relx=0.5, rely=0.2, relwidth=0.9, relheight=0.2)
        self.author_label = Label(master=self.top, text="作者：等待响应中...", bg=top_background_color, fg=top_forebackground_color, font=top_label_font, anchor=W)
        self.author_label.place(anchor=CENTER, relx=0.5, rely=0.4, relwidth=0.9, relheight=0.2)
        self.notice_label =  Label(master=self.top, text="提示：等待响应中...", bg=top_background_color, fg=top_forebackground_color, anchor=W)
        self.notice_label.place(anchor=CENTER, relx=0.5, rely=0.9, relwidth=0.9, relheight=0.15)
        ## 创建进度条
        self.progress_bar = ttk.Progressbar(master=self.top, maximum=10000, value=0, style="red.Horizontal.TProgressbar")
        self.progress_bar.place(anchor=CENTER, relx=0.5, rely=0.65, relwidth=0.9, relheight=0.2)

        ## 关闭窗口时的动作
        def on_closing():
            self.title_label.destroy()
            self.author_label.destroy()
            self.progress_bar.destroy()
            self.notice_label.destroy()
            self.top.destroy()
            self.start_button['state'] = ACTIVE
            self.latest_chapter_only_check_button['state'] = ACTIVE
        self.top.protocol("WM_DELETE_WINDOW", on_closing)

        ## 开始爬取书籍
        for url in urls:
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
            #3 启动爬虫
            spider.crawl_novel()
            ## 爬取后取消勾选
            for choice_button in self.choice_buttons:
                if self.book_info[choice_button.cget("text")] == url:
                    choice_button.deselect()
        ## 关闭程序
        on_closing()
        ## 显示弹窗
        self.about_software()

    ## 将书籍从输入框添加进缓存区
    def add_book(self):
        title = self.book_title_entry.get()
        url = self.book_url_entry.get()
        if title not in self.book_info.keys() and title != '书名' and url != "链接" and "http" in url :
            self.create_choice_button(book_title=title, book_url=url, selected=True)
            self.book_title_entry.delete(0, END)
            self.book_url_entry.delete(0, END)
            self.book_title_entry.insert(0, '书名')
            self.book_url_entry.insert(0, '链接')

    ## 全选缓存区中所有书籍
    def select_all(self):
        for choice_button in self.choice_buttons:
            choice_button.select()

    ## 取消全选
    def cancel_select_all(self):
        for choice_button in self.choice_buttons:
            choice_button.deselect()

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
            self.choice_panel.insert('1.0', '\n\n')
        ## 禁止编辑缓存区
        self.choice_panel.config(state=DISABLED)


    def load_info_list(self):
        fin = open("book_info.html", 'r', encoding='UTF-8')
        regx = re.compile('<li><a href="(?P<url>.*?)">(?P<title>.*?)</a></li>')
        for line in fin.readlines():
            info = regx.search(line)
            if info != None:
                self.book_info[info.group('title')] = info.group('url')
        fin.close()

    ## 将缓存区书籍永久储存
    def save_info_list(self):
        fout = open("book_info.html", 'w', encoding='UTF-8')
        fout.write(html_prefix)
        for book_title in self.book_info:
            fout.write(f'        <li><a href="{self.book_info[book_title]}">{book_title}</a></li>\n')
        fout.write(html_postfix)
        fout.close()

    ## 打赏页面
    def about_software(self):
        ## 预定义弹窗变量
        top_background_color = 'white'
        top_forebackground_color = 'black'
        top_label_font = tkFont.Font(size=16, weight='bold')
        ## 创建弹窗
        top = Toplevel(master=self.master, bg=top_background_color)
        top.title('关于应用')
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
        text_label = Label(master=top, text="用都用了，打个赏呗~", font=top_label_font, bg='white')
        text_label.place(anchor=W, relx=0.5, rely=0.5)

    def open_save_path(self):
        os.startfile(os.getcwd()+os.sep+'fiction')

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
        choice_button = Checkbutton(self.choice_panel, text=book_title, bg=self.choice_button_background_color, anchor='w', font=self.choice_button_font, variable=var, onvalue=1, offvalue=0)
        choice_button.var = var
        ## 根据需求来预选项目
        if selected==True:
            choice_button.select()
        else:
            choice_button.deselect()
        ## 将项目加入缓存区
        self.choice_buttons.append(choice_button)
        self.choice_panel.window_create('1.0', window=choice_button)
        self.choice_panel.insert('1.0', '\n\n')
        ## 禁止编辑缓存区
        self.choice_panel.config(state=DISABLED)

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





