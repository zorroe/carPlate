
# 车牌识别客户端


# 车牌识别服务端[点击](https://github.com/LiXuuuu/carPlateServer)



# 项目计划书[点击](http://139.196.240.235:10000/schedule)



### 桌面端V0.1介绍

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

   * <font color=#00FF7F>**<u>解决方案</u>**</font>：优化后的方法直接将图像的base64编码解码后直接读取为pillow图像对象然后传入getPlate函数进行识别。节省IO操作耗费的时间

   ```python
   img_data = base64.b64decode(request.POST.get('img'))
   pilimage = Image.open(BytesIO(img_data))
   
   plate = getPlate(pilimage)
   ```

2. 客户端界面卡顿，CPU占用高
   * <font color=#FFA07A>**<u>原始</u>**</font>：所有函数都在一个线程，其中YoLo模型检测车牌，上传图片然后接受返回信息都是耗时操作。造成客户端卡顿且CPU占用高！
   * <font color=#00FF7F>**<u>解决方案</u>**</font>：将YoLo模型检测车牌和上传图像接受返回信息这两个操作放到子线程，每隔0.5s检测一帧图像，然后上传接收。

![车牌](https://typora-lixuan.oss-cn-shanghai.aliyuncs.com/car.jpeg)

图形化窗口：

![图形化窗口](https://typora-lixuan.oss-cn-shanghai.aliyuncs.com/1.jpg)

识别效果：

![识别效果](https://typora-lixuan.oss-cn-shanghai.aliyuncs.com/2.jpg)

### release信息

* 2021年5月23日：上传第一个0.1版本，本版本为单线程版本，界面卡顿，无法使用，后续会优化为多线程版本。
