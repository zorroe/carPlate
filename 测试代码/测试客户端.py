import glob
import os
import shutil

import cv2
import json
import base64
import requests
import random

from plateDetect import yolo

labels = ["京", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "皖", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂",
          "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A",
          "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
          "Y", "Z", "-"]
provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣",
             "鲁", "豫", "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "-"]
alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z', '-']
ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
       'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']


# 获取每个省的车牌
def get_all_province():
    return 0
    pre_src = 'E:/spm/最终测试环节/测试代码/CCPD2019'
    pre_dirs = os.listdir(pre_src)
    other_province_list = []
    for i in pre_dirs:
        plate_dir = pre_src + '/' + i
        car_img_list = os.listdir(plate_dir)
        for filename in car_img_list:
            img_path = plate_dir + '/' + filename
            dst_path = 'E:/spm/最终测试环节/测试代码/car_img/' + filename
            anno_str = img_path.split("-")
            label = list(map(int, anno_str[4].split('_')))
            if label[0] != 0:
                other_province_list.append(img_path)
                shutil.copyfile(img_path, dst_path)
        break


# 根据图片名解析真实车牌字符
def get_plate(img_path):
    anno_str = img_path.split("-")
    label = list(map(int, anno_str[4].split('_')))
    label_char = []
    label_char.append(provinces[label[0]])
    label_char.append(alphabets[label[1]])
    for i in label[2:]:
        label_char.append(ads[i])
    return ''.join(label_char)


# 从测试图像中随机获取500张含有车牌字符的图片，将其放到列表中
def get_random_car_img(num):
    car_all_list = os.listdir('car_img/')
    random.shuffle(car_all_list)
    return car_all_list[:num]


# 检测Yolo模型效果
def test_yolo():
    count = 0
    num = 100
    car_img_save = 'car_img/'
    plate_save = 'plate/'
    net = yolo()
    car_img_list = get_random_car_img(num)
    shutil.rmtree(plate_save)
    os.mkdir(plate_save)
    for car_img in car_img_list:
        car_src = car_img_save + car_img
        img = cv2.imread(car_src)
        _, plates = net.return_frame(img)
        for plate in plates:
            count += 1
            cv2.imwrite(plate_save + car_img, plate)
    print('从{}张图像中获取到了{}张车牌图像'.format(num, count))


# 测试客户端发送图像
request_url = "http://139.196.240.235:10000/"
headers = {'content-type': 'application/x-www-form-urlencoded',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.41'}


# 评估预测出来的结果
def evaluate_predict(predict_list, true_list):
    correct = 0
    all = len(predict_list)
    for pre, tru in zip(predict_list, true_list):
        if pre == tru:
            correct += 1
    print(correct / all)


# 测试发送到服务端进行预测然后服务端返回字符
def test_send_plate():
    plate_save = 'plate/'
    predict_list, true_list = [], []
    plate_list = os.listdir(plate_save)
    for plate in plate_list:
        plate_src = plate_save + plate
        image = cv2.imread(plate_src)
        image = cv2.imencode('.jpg', image)[1]
        base64_data = str(base64.b64encode(image))[2:-1]
        params = {'img': base64_data}
        response = requests.post(request_url, data=params, headers=headers)
        predict_plate = ''
        true_plate = get_plate(plate_src)
        if len(json.loads(response.text)['plate']) > 0:
            predict_plate += response.json()['plate']
        predict_list.append(predict_plate)
        true_list.append(true_plate)
        print('预测:{},真实:{}'.format(predict_plate, true_plate))
    evaluate_predict(predict_list, true_list)


if __name__ == '__main__':
    # get_all_province()
    test_yolo()
    # test_send_plate()
