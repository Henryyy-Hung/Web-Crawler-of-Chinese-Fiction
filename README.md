
## **基本资料**
* 名称：【小说爬虫】
* 版本：1.1.3 ([**点此下载最新版**](https://github.com/Henryyy-Hung/Web-Crawler-of-Chinese-Fiction/raw/main/exe/%E5%B0%8F%E8%AF%B4%E7%88%AC%E8%99%ABv1.1.3.exe))
* 要求：Win 10 或以上
* 功能：从小说网站抓取小说内容，排版并保存为TXT文档。
* 教程：[**点此查看使用方法**](#使用方法)，请务必跟着教程一步一步来。
* 备注：本软件免费且无毒。若出现任何问题，一是没按操作来，二是用了【[**支援的网站**](#支援的网站 "Goto 支援的网站")】以外的网站，三是在繁忙时间使用，网站伺服器处理不过来。[点此查看源代码](https://github.com/Henryyy-Hung/Web-Crawler-of-Chinese-Fiction/tree/main/src)。如有任何问题，请用我主页上的email联络我。

## **预览图片**
<img src="https://user-images.githubusercontent.com/78750074/179153333-c544e2c9-b499-43d4-96a2-79edf1a1ee0c.jpg" alt="demo" width="640" height="320" />
<img src="https://user-images.githubusercontent.com/78750074/183332140-c4bde035-b525-4735-84ae-fe09266128f4.png" alt="booklist" width="640" height="320" />
（没错我在学习html和css，这界面做的好看吧哈哈哈哈）

## **制作目的**
* 提供一款真正简单易用的小说下载器。
  * 仅需复制粘贴网址，点击开始按钮。
* 方便使用封闭式阅读器的朋友以及需要离线阅读的中小学生追书。
  * 一经建立书单，后续一键下载最新章节TXT。
* 提供排版过的原始小说文本。
  * 排版格式为：标题不缩进，段落缩进两个中文全角空格，章节间空两行。同时自动去除网址等广告。
* 方便分享书籍。
  * 只要将 `book_info.html` 文件分享给别人，别人就能够使用你的书单。

## **使用方法**
* 从【[**支援的网站**](#支援的网站 "Goto 支援的网站")】中选择一本你中意的书，点开目录页面。（请勿使用其它网站！！！）
  * 例如：https://www.uuks.org/b/52716/
* 复制目录页面的网页链接。
  * 例如：复制以上链接
* 回到应用，手动输入书名至【**书名栏**】，并复制链接至【**链接栏**】。
  * 例如：【书名：道诡异仙】【链接：[https://www.uuks.org/b/52716/](https://www.uuks.org/b/52716/)】
* 点击右侧【**添加数据**】按钮，将书籍放入候选区。
  * - [ ] `道诡异仙` <- 候选区状态
* 在候选区勾选书籍，点击【**开始下载**】，即可开始下载。
  * - [X] `道诡异仙` <- 候选区状态
* 下载完成后，点击【**查看文件**】按钮，打开装有已下载文件的文件夹。
  * 你会在文件夹里见到 `道诡异仙.txt`
* 如有再次下载的需要，请点击【**保存书单**】，以便下次打开时恢复数据。
  * 注：应用程序同一目录下名为 `book_info.html` 的文件是用户自己创建的书单，请勿删除。

## **支援的网站**
网站名|网址|书目数量|优点|缺点
-----|----|-------|----|----
31小说网|https://www.31xs.com|73000+|更新快，质量高| 经常崩溃
UU看书|https://www.uuks.org|65000+|质量高|暂未发现
飘天文学|https://www.ptwxz.com|8800+|质量高|内地无法使用
爱笔楼|https://www.ibiquge.net|无法统计|超多书！|质量低，或有广告
笔趣阁①|http://www.bqxs520.com|无法统计|更新快|质量低，或有广告

## **更新日志**

#### Version 1.0.0   (14/6/2022)
* 新增
  * 添加了只爬取最近100章按钮。
  
#### Version 1.1.0   (18/6/2022) 此版本书单不兼容上个版本书单！！！
* 新增
  * 添加了打开已保存文件按钮。
  * 将使用教程从软件内部转移至Github。
  * 允许用户打开及浏览书单。（将书单从不可见的pkl格式改为html格式。）
* 优化
  * 优化了使用界面，下载完成后会自动取消勾选。
  * 优化了使用界面，候选区书籍会根据拼音排序。
  
#### Version 1.1.1   (25/7/2022)
* 优化
  * 优化了等待下载界面。
* 修复
  * 修复了阻塞mainloop()导致的卡顿。
  
#### Version 1.1.2   (5/8/2022)
* 优化
  * 美化了“我的书单”界面。
* 修复
  * 修复了31小说网无法下载问题。
  
#### Version 1.1.3   (8/8/2022) 此版本书单不兼容上个版本书单！！！
* 新增
  * 移除了取消全选按钮，替换为反向选择按钮。
  * 新增了下载后的统计页面，显示总共下载多少书籍以及总共消耗多少时间。
* 优化
  * html书单自动根据中文拼音排序。
  * 美化了“我的书单”界面。
  * 优化了爬取算法，加入随机元素。
  * 优化了爬取速度算法，如用户有编程基础，可自行浏览源代码(novel spider的crawl novel函数内)开启该功能。从而限制本程序的cpu使用率，防止cpu过热。
* 修复
  * 修复了用户在程序运行一半时，立刻停止再重重新下载所产生的错误。
  * 修复了中断下载时，正在下载的项目也会被取消勾选的错误。
  * 修复了删除所选后，候选莫名多出一些空白位置的bug。
  * 修复了鼠标在候选区中变成文字输入图示的bug。
  
#### Version 1.1.4   (9/8/2022)
* 新增
  * 右键点击选项可直接编辑选项。
  * 右键双击可直接在浏览器打开选项。
  * 可通过ENTER键进行书籍的输入。
* 优化
  * 在添加书籍和删除书籍后，会自动返回最顶部。
  * 优化候选区界面，增加四边边距。
  * 鼠标悬浮在选项上时，会有颜色变化提示。
* 修复
  * 修复在选项区域不可滚动屏幕的bug。
  
#### Version 1.2.0   (待定)
* 尝试建立小说索引库，可以直接在应用内搜索并爬取。
* 扩充支援的网站。

后续版本不会有大更新，但还是会根据我自己的使用情况有更新。|
--------------------------------------------------------|

## **备注**
这是2022年大二暑假所写的一个小程序。

## **免责声明**
0. 【小说爬虫】对爬取速度进行了极大的限制，已尽量减少对网站的负担。
1. 【小说爬虫】是一款解析指定规则并获取内容的工具，为广大网络文学爱好者提供一种方便、快捷舒适的试读体验。
2. 您可以自行浏览[源代码](https://github.com/Henryyy-Hung/Web-Spider-of-Chinese-Fiction/blob/main/src/NovelSpider.py)，添加正则表达式，从选定的网页上下载文字至txt文档，也可使用预定义的网站。
3. 各第三方网站返回的内容与【小说爬虫】无关，【小说爬虫】对其概不负责，亦不承担任何法律责任。
4. 任何通过使用【小说爬虫】而链接到的第三方网页均为他人制作或提供，您可能从第三方网页上获得其他服务，【小说爬虫】对其合法性概不负责，亦不承担任何法律责任。
5. 您可能从第三方网页上获得其他服务，【小说爬虫】对其合法性概不负责，亦不承担任何法律责任。
6. 对于第三方网站之内容与立场，【小说爬虫】不会支持或反对，您应该对下载文章的内容自行承担风险。
7. 【小说爬虫】不做任何形式的保证：不保证搜索服务不中断，不保证搜索结果的安全性、正确性、及时性、合法性。
8. 因网络状况、通讯线路、第三方网站等任何原因而导致您不能正常使用【小说爬虫】，【小说爬虫】不承担任何法律责任。
9. 【小说爬虫】致力于最大程度地减少网络文学阅读者在自行搜寻txt文档过程中的无意义的时间浪费。
10. 任何单位或个人认为通过【小说爬虫】搜索链接到的第三方网页内容可能涉嫌侵犯其信息网络传播权，应该及时向【小说爬虫】提出书面权力通知，并提供身份证明、权属证明及详细侵权情况证明。
11. 【小说爬虫】在收到上述法律文件后，将会依法尽快断开相关链接内容。
