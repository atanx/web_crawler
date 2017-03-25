### 打包
```sh
python setup.py py2exe
```
### 安装说明
系统要求 win7, chrome浏览器
1. 初次安装请解压包所在目录下的chromedriver.exe
文件所在目录添加到path中。

### FAQ
1. Q: 启动程序后浏览器无法打开？
   A:请检查chrome是否安装，若已安装chrome浏览器，
   请到https://chromedriver.storage.googleapis.com/index.html?path=2.26/
   下载chrome版本相对应的chromedriver.exe

### 升级说明
1. BUG修复
修复人气值解析错误，导致无法输出结果。
当没有在线人数时，online_viewer被解析成字符串，
导致后续过滤函数`_filter()`中报数字转换错误。

