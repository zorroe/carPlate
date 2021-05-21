# 欢迎使用车牌识别系统


# 车牌识别客户端
# 车牌识别服务端[点击](https://github.com/LiXuuuu/carPlateServer)

# 项目计划书[点击](http://139.196.240.235:10000/schedule)


桌面的开发步骤主要分为以下几步：

首先是从文件中加载UI，从UI中定义动态，创建一个相应的窗口。

然后调用本地摄像头，并打开摄像头，对视频流按帧读取，将图片传送至服务器，服务器对其进行识别，接受服务器的返回信息，并将其显示在屏幕上。

1、 打开摄像头

2、 获取图像

3、 图像压缩、编码

image = cv2.imencode('.jpg', plate)[1]

base64_data = str(base64.b64encode(image))[2:-1]

params = {'img': base64_data}

4、 上传至服务器

服务端的地址：self.request_url = "http://139.196.240.235:10000/"

服务端对上传过来的图片信息进行识别处理

response = requests.post(self.request_url, data=params, headers=self.headers)

5、 接受服务器的返回信息

测试的车牌图片：

<img src="https://github.com/LiXuuuu/carPlate/blob/main/Image/car.jpeg" width="300" height="300" alt="车牌"/><br/>

图形化窗口：

<img src="https://github.com/LiXuuuu/carPlate/blob/main/Image/1.jpg" width="300" height="300" alt="图形化窗口"/><br/>

识别效果：
<img src="https://github.com/LiXuuuu/carPlate/blob/main/Image/2.jpg" width="300" height="300"  alt="识别效果"/><br/>

