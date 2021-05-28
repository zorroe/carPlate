
### 车牌识别客户端


### 车牌识别服务端 [点击](https://github.com/LiXuuuu/carPlateServer)

### 项目计划书 [点击](http://139.196.240.235:10000/schedule)



### 桌面端V0.1

#### 介绍

主文件  [carPlateRec.py](https://github.com/LiXuuuu/carPlate/blob/0.1/carPlateRec.py)

1. 使用pydesigner设计ui界面，pyside2加载界面ui文件
2. get_video函数负责打开摄像头，使用YoLo模型对摄像头采集到的视频进行检测，若检测到车牌，使用红色框标记并显示，同时截取车牌部分将图像编码之后上传至服务器，服务器上的LPRNet模型识别之后将车牌字符返回，然后客户端将字符显示出来。

#### 需要改进的地方

1. 服务端处理接受到的图片

   * <font color=#FFA07A>**<u>原始</u>**</font>：原始方法将得到的图像base64编码解码后将图片保存到本地，然后传给getPlate函数一个图片路径，getPlate函数再使用pillow模块打开图像进行识别

   ```python
   img_data = base64.b64decode(request.POST.get('img'))
   
   with open(img_path, 'wb') as f:
       f.write(img_data)
   plate = getPlate(img_path)
   ```

   * <font color=#00FF7F>**<u>解决方案</u>**</font>：优化后的方法直接将图像的base64编码解码后直接读取为pillow图像对象然后传入getPlate函数进行识别。

   ```python
   img_data = base64.b64decode(request.POST.get('img'))
   pilimage = Image.open(BytesIO(img_data))
   
   plate = getPlate(pilimage)
   ```

2. 客户端界面卡顿，CPU占用高
   * <font color=#FFA07A>**<u>原始</u>**</font>：所有函数都在一个线程，其中YoLo模型检测车牌，上传图片然后接受返回信息都是耗时操作。造成客户端卡顿且CPU占用高！
   * <font color=#00FF7F>**<u>解决方案</u>**</font>：将YoLo模型检测车牌和上传图像接受返回信息这两个操作放到子线程，每隔0.5s检测一帧图像，然后上传接收。

<iframe 
        src="//player.bilibili.com/player.html?aid=290828963&bvid=BV1yf4y1h7Zb&cid=345265126&page=1" 
		width=800
        height=600
        scrolling="no" 
        border="0" 
        frameborder="no" 
        framespacing="0" 
        allowfullscreen="true"> 
</iframe>

### 桌面端V1.0

#### 介绍

- [x] 改变服务端处理接受图片的方式
- [x] 将客户端的单线程版本改为多线程

1.0版本将之前版本的两个问题进行了优化，第一个问题就是服务端处理接受图片的方式。具体提升效果如下表所示：

|   获取图片方式   |   时间    |
| :--------------: | :-------: |
|   使用文件写读   | 3.8819384 |
| 使用字节流直接读 | 3.3374874 |

解决的第二个问题是单线程问题，V0.1版本的客户端为单线程版本，将耗时操作放在了主线程，然后V1.0版本将耗时操作放到子线程，界面流畅。

<iframe 
        src="//player.bilibili.com/player.html?aid=630790943&bvid=BV1db4y1o7gS&cid=345242156&page=1" 
		height=600
        width=800
        scrolling="no" 
        border="0" 
        frameborder="no" 
        framespacing="0" 
        allowfullscreen="true"> 
</iframe>

### release信息

* 2021年5月23日：上传第一个0.1版本，本版本为单线程版本，界面卡顿，无法使用，后续会优化为多线程版本。

* 2021年5月28日：上传第二个1.0正式版本，本版本为多线程版本，可以在不同配置的计算机上使用
