import PySide2

from PySide2.QtGui import QIcon
from PySide2 import QtGui
from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader

import os
from plateDetect import yolo

net = yolo()

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class CarPlates:
    def __init__(self):
        # 从文件中加载ui
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        self.ui = QUiLoader().load('carPlateRec.ui')
        self.ui.start.clicked.connect(self.get_video)
        self.ui.end.clicked.connect(self.change_is_cap)
        self.ui.car.setText('摄像头未打开')
        self.is_cap = 1
        self.headers = {'content-type': 'application/x-www-form-urlencoded',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.41'}
        self.request_url = "http://139.196.240.235:10000/"


app = QApplication([])
# 加载 icon
app.setWindowIcon(QIcon('logo.png'))
carPlate = CarPlates()
carPlate.ui.show()
app.exec_()
