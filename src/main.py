from NovelSpider import *
from GUI import *

if __name__ == '__main__':
    a = SpiderGUI()

r'''

代码使用指南：

0. 确认代码连同img文件夹放在统一目录下。
  img文件夹有两个文件，分别是icon.ico和sponsorship.png

1. 使用代码前需要安装的包（在terminal输入这些指令安装包）
  pip install requests
  pip install selenium
  pip install my_fake_useragent
  pip install pypinyin
  pip install psutil
  pip install Pillow
  pip install pyinstaller

2. 在terminal输入以下指令进行exe打包

  pyinstaller --icon=img/icon.ico --add-data C:\Users\hkh13\AppData\Local\Programs\Python\Python39\tcl\tix8.4.3;tcl\tix8.4.3  --add-data img;img -F -w --onefile main.py

'''
