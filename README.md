
## **基本资料**
* 名称：【小说爬虫】
* 版本：1.1
* 功能：从不提供下载的小说网站爬取TXT文档，自动校对等。
* 下载：[**点此下载最新版**](https://github.com/Henryyy-Hung/Web-Crawler-of-Chinese-Fiction/blob/main/exe/%E5%B0%8F%E8%AF%B4%E7%88%AC%E8%99%ABv1.1.exe?raw=true)
* 教程：请参阅[**使用方法**](#使用方法)，跟着教程一步一步来
* 备注：本软件完全免费，无毒。如果若出现任何问题，一是没按操作来，二是用了【[**支援的网站**](#支援的网站 "Goto 支援的网站")】以外的网站，三是在繁忙时间使用，网站伺服器处理不过来。

<img src="https://user-images.githubusercontent.com/78750074/179153333-c544e2c9-b499-43d4-96a2-79edf1a1ee0c.jpg" alt="demo" width="640" height="320" />

## **制作目的**
* 下载只供阅读的网站中的TXT文本
* 排版并校对该TXT文本
* 一经建立书单，后续一键下载
* 方便只能用离线阅读器的朋友们(e.g. 初高中生)追书
* 其实这玩意最主要还是用来搞TXT给使用封闭式墨水屏阅读器的朋友们追书的。

## **使用方法**
* 从【[**支援的网站**](#支援的网站 "Goto 支援的网站")】中选择一本你中意的书，点开目录页面。（请勿使用其它网站！！！）
    * 例如：https://www.ptwxz.com/html/14/14431/
* 复制目录页面的网页链接。
    * 例如：复制以上链接
* 回到应用，手动输入书名至【**书名栏**】，并复制链接至【**链接栏**】。
    * 例如：书名：`道诡异仙` 链接：`https://www.ptwxz.com/html/14/14431/`
* 点击右侧【**添加数据**】按钮，将书籍放入候选区。
    * - [ ] `道诡异仙` <- 候选区状态
* 在候选区勾选书籍，点击【**开始下载**】，即可开始下载。
    * - [X] `道诡异仙` <- 候选区状态
* 下载完成后，点击【**查看文件**】按钮，打开装有已下载文件的文件夹。
    * 你会在文件夹里见到 `道诡异仙.txt`
* 如有再次下载的需要，请点击【**保存书单**】，以便下次打开时恢复数据。
    * 注：应用程序同一目录下名为 `book_info.html` 的文件是用户自己创建的书单，请勿删除。

## **支援的网站**
网站名|网址|书目数量|优点|缺点|补充资料
-----|----|-------|----|----|-------
31小说网|https://www.31xs.net|73000|更新快，质量高| 在繁忙时段可能用不了|
UU看书|https://www.uuks.org|65000|质量高|暂未发现|
飘天文学|https://www.ptwxz.com|8800|质量高|书籍少|
笔趣阁|http://www.bqxs520.com|无法统计|章节全|质量低，或有广告|
笔趣阁|https://www.ibiquge.net|无法统计|书籍特别多|质量低，或有广告|
疯情书屋|https://aabook.xyz/|4000|小黄文你懂的|速度慢15倍|需要自行安装chormdriver

## **更新计划**
- [X] 添加只爬取最近100章按钮，避免浪费时间空间以及对网站造成负荷。`v1.0 已更新`
- [X] 将使用教程转移至Github，令页面更简洁。`v1.1 已更新`
- [X] 修改用户保存的书单，从用户不可见格式修改为html格式，将书单打造成一个网站导航页面，方便用户浏览网站。`v1.1 已更新`
- [X] 修改UI设定，添加一键打开文件夹选项，方便用户爬取完后直接打开文件夹获得TXT文件。`v1.1 已更新`
- [ ] 尝试建立小说索引库，可以直接在应用内搜索并爬取。`预计 v1.2 更新 (如果有赞助的话)`
- [ ] 扩充支援的网站。`预计 v1.3 更新 (如果有赞助的话)`

## **免责声明**
0. 【小说爬虫】对爬取速度进行了限制，已尽量减少对网站的负担。
1. 【小说爬虫】是一款解析指定规则并获取内容的工具，为广大网络文学爱好者提供一种方便、快捷舒适的试读体验。
2. 您可以自行浏览[源代码](https://github.com/Henryyy-Hung/Web-Spider-of-Chinese-Fiction/blob/main/src/NovelSpider.py)，添加正则表达式，从选定的网页上下载文字至txt文档，也可使用预定义的网站。
3. 各第三方网站返回的内容与【小说爬虫】无关，【小说爬虫】对其概不负责，亦不承担任何法律责任。
4. 任何通过使用【小说爬虫】而链接到的第三方网页均为他人制作或提供，您可能从第三方网页上获得其他服务，【小说爬虫】对其合法性概不负责，亦不承担任何法律责任。
5. 您可能从第三方网页上获得其他服务，【小说爬虫】对其合法性概不负责，亦不承担任何法律责任。
6. 对于第三方网站之内容与立场，【小说爬虫】不会支持或反对，您应该对下载文章的内容自行承担风险。
7. 【小说爬虫】不做任何形式的保证：不保证搜索服务不中断，不保证搜索结果的安全性、正确性、及时性、合法性。
8. 因网络状况、通讯线路、第三方网站等任何原因而导致您不能正常使用【小说爬虫】，阅读不承担任何法律责任。
9. 【小说爬虫】致力于最大程度地减少网络文学阅读者在自行搜寻txt文档过程中的无意义的时间浪费
10. 【小说爬虫】鼓励广大小说爱好者通过阅读发现优秀网络小说及其提供商，并建议阅读正版图书。
11. 任何单位或个人认为通过【小说爬虫】搜索链接到的第三方网页内容可能涉嫌侵犯其信息网络传播权，应该及时向阅读提出书面权力通知，并提供身份证明、权属证明及详细侵权情况证明。
12. 【小说爬虫】在收到上述法律文件后，将会依法尽快断开相关链接内容。
