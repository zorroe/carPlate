import cv2 as cv
import numpy as np


class yolo:
    def __init__(self):
        # Initialize the parameters
        self.confThreshold = 0.5  # Confidence threshold
        self.nmsThreshold = 0.4  # Non-maximum suppression threshold

        # self.inpWidth = 416  # 608
        # self.inpHeight = 416  # 608
        self.inpWidth = 320  # 608
        self.inpHeight = 320  # 608

        self.modelConfiguration = 'yolov3-KD.cfg'
        self.modelWeights = 'yolov3-KD_last.weights'

        self.net = cv.dnn.readNetFromDarknet(self.modelConfiguration, self.modelWeights)

        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
        # self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        # self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    def getOutputsNames(self, net):
        layersNames = net.getLayerNames()
        return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    def drawPred(self, left, top, right, bottom, frame):
        """
        绘制车牌框
        :param left: 左边界
        :param top: 上边界
        :param right: 右边界
        :param bottom: 下边界
        :param frame: 图像
        :return: 返回在frame上根据四个坐标画好轮廓的图像
        """
        frame = cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)
        return frame


    def returnPred(self, frame, left, top, right, bottom):
        """
        返回车牌图像
        :param frame: 图像
        :param left: 左边界
        :param top: 上边界
        :param right: 右边界
        :param bottom: 下边界
        :return: 返回对图像按照边界切割后的车牌图像
        """
        targ = frame[top:bottom, left:right]
        return targ


    def postprocess(self, frame, outs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        classIds = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        plate_list = []
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            frame = self.drawPred(left, top, left + width, top + height, frame)
            plate_list.append(self.returnPred(frame, left, top, left + width, top + height))
        return frame, plate_list

    def return_frame(self, frame):
        """
        接收图像,返回标记车牌后的图像以及车牌图像列表
        :param frame: 摄像头捕获的一帧图像
        :return:
            self.postprocess()函数运行之后返回两个数据：标记车牌后的图像以及车牌图像列表
        """
        blob = cv.dnn.blobFromImage(frame, 1 / 255, (self.inpWidth, self.inpHeight), [0, 0, 0], 1, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.getOutputsNames(self.net))
        return self.postprocess(frame, outs)
