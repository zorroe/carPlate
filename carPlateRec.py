import base64
import json
import os
import cv2
import time
import numpy as np
import PySide2
import requests

from threading import Thread
from PySide2 import QtGui
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from plateDetect import yolo

# 初始化一个Yolo网络
net = yolo()

# 设置pyside2临时环境变量
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class CarPlates:
    def __init__(self):
        # 从文件中加载ui
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性
        self.ui = QUiLoader().load('carPlateRec.ui')
        self.ui.start.clicked.connect(self.get_video)
        self.ui.end.clicked.connect(self.change_is_cap)
        self.ui.car.setText('摄像头未打开')
        self.is_cap = 1
        self.headers = {'content-type': 'application/x-www-form-urlencoded',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.41'}
        self.request_url = "http://139.196.240.235:10000/"
        self.frame = ''
        self.plates = []
        self.cap_url = 'http://192.168.137.136:4747/video'
        self.total_plate = ''
        self.plate_str = ''

    def get_plate(self):
        self.frame, self.plates = net.return_frame(self.img)  # frame是标记后的图像，plates是单独的车牌图像列表

    def show_str(self):
        if len(self.plates) == 1:  # 110*35
            self.total_plate = self.plates[0]
            self.total_plate = cv2.resize(self.total_plate, dsize=(110, 35))
            self.total_plate = cv2.cvtColor(self.total_plate, cv2.COLOR_BGR2RGB)
            x = self.total_plate.shape[1]
            y = self.total_plate.shape[0]
            showImage = QtGui.QImage(self.total_plate.data, x, y, x * 3, QtGui.QImage.Format_RGB888)
            self.ui.plate_img.setPixmap(QtGui.QPixmap.fromImage(showImage))
        if len(self.plates) > 1:
            self.total_plate = self.plates[0]
            self.total_plate = cv2.resize(self.total_plate, dsize=(110, 35))
            for i in range(1, len(self.plates)):
                plate = self.plates[i]
                plate = cv2.resize(plate, dsize=(110, 35))
                self.total_plate = np.vstack([self.total_plate, plate])
            self.total_plate = cv2.cvtColor(self.total_plate, cv2.COLOR_BGR2RGB)
            x = self.total_plate.shape[1]
            y = self.total_plate.shape[0]
            showImage = QtGui.QImage(self.total_plate.data, x, y, x * 3, QtGui.QImage.Format_RGB888)
            self.ui.plate_img.setPixmap(QtGui.QPixmap.fromImage(showImage))

        self.plate_str = ''
        for plate in self.plates:
            image = cv2.imencode('.jpg', plate)[1]
            base64_data = str(base64.b64encode(image))[2:-1]
            params = {'img': base64_data}
            response = requests.post(self.request_url, data=params, headers=self.headers)
            # print(response.text)
            if len(json.loads(response.text)['plate']) > 0:
                # print(response.json())
                self.plate_str += response.json()['plate']
                self.plate_str += '\n'
                # print(len(self.plate_str))
        if(len(self.plate_str) == 8):
            self.ui.plate_char.setText(self.plate_str)
            self.ui.plate_char.setStyleSheet("font-size:30")

    # 获取摄像头视频
    def get_video(self):
        self.is_cap = 1
        self.cap = cv2.VideoCapture(0)
        # self.cap = cv2.VideoCapture(self.cap_url)
        t0 = time.perf_counter()
        while (self.is_cap):
            ret, frame = self.cap.read()
            self.img = frame
            thread_get_plate = Thread(target=self.get_plate)
            thread_show_str = Thread(target=self.show_str)
            t1 = time.perf_counter()
            if t1 - t0 > 0.5:
                thread_get_plate.start()
                thread_show_str.start()
                t0 = t1
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(self.img.data, self.img.shape[1], self.img.shape[0], QtGui.QImage.Format_RGB888)
            self.ui.car.setPixmap(QtGui.QPixmap.fromImage(showImage))
            QApplication.processEvents()
        self.cap.release()
        self.ui.car.setText('摄像头未打开')

    def change_is_cap(self):
        self.is_cap = 0



if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('logo.png'))
    carPlate = CarPlates()
    carPlate.ui.show()
    app.exec_()
