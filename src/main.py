from NovelSpider import *
from GUI import *

if __name__ == '__main__':
    a = SpiderGUI()

# pyinstaller -F -w --onefile main.py
# pyinstaller --icon=img/icon.ico --add-data C:\Users\hkh13\AppData\Local\Programs\Python\Python39\tcl\tix8.4.3;tcl\tix8.4.3  --add-data img;img -F -w --onefile main.py