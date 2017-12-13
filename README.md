学习Python for Data Analysis源码,IDE为pycharm
需要安装的python依赖
1. pandas
2. pylab
3. numpy
4. basemap（map这个工程需要用到）
着重说一下basemap的安装
(1)确认电脑有pip；
(2)下载pyproj和basemap
   通过连接 http://www.lfd.uci.edu/~gohlke/pythonlibs/下载两个文件：
   basemap‑1.1.0‑cp36‑cp36m‑win_amd64.whl
   pyproj‑1.9.5.1‑cp36‑cp36m‑win_amd64.whl
(3)打开命令提示符，将当前目录设置为下载文件所在的目录
(4)安装pyproj和basemap：
   pip install pyproj‑1.9.5.1‑cp36‑cp36m‑win_amd64.whl
   pyproj安装好之后继续安装basemap：
   pip install basemap‑1.1.0‑cp36‑cp36m‑win_amd64.whl


datasets目录中存放的是需要源码处理的数据（大文件无法上传，请参照https://github.com/wesm/pydata-book）
