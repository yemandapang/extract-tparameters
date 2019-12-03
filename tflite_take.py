# -*- coding: utf-8 -*-
import numpy as np
np.set_printoptions(threshold=np.inf)
import tensorflow as tf
import cv2 as cv
import os

#提取序号和名称对应关系
def take_para():
    Tensor_name_sequence = {}
    for i in range(277):
        output_data = tflite_model.get_tensor(i)
        output_data1 = tflite_model._get_tensor_details(i)  # _get_tensor_details 可以按照序号取对应的tensor 详情
        output_data_name = tflite_model._interpreter.TensorName(i)
        Tensor_name_sequence[output_data_name] = i
        #print(output_data)
        # print("out_class")
        # print(output_data.shape)
        # print(output_data1)
        # print(output_data_name)
        # print(i)
    print(Tensor_name_sequence)
    return Tensor_name_sequence

def float_bin_int16(s): # s是对应每个数，decimal是10
    temp = float(s) * pow(2, int(10))
    den = 0
    if s >= pow(2, 15):
        s = pow(2, 15) - 1
    if s < -pow(2, 15):
        s = -pow(2, 15)
    if s < 0:
        den = (s + pow(2, int(16))) % pow(2, int(16))
    else:
        den = s

    return int(den)


# 将提取出的对应关系写入txt
def write_Tensor_name_sequence(Tensor_name_sequence):
    Tensor_name_sequence = take_para()
    with open('Yolo_Tensor_name_sequence.txt', 'w') as f:
        for k, v in Tensor_name_sequence.items():  # 遍历字典中的键值
            s2 = str(v)  # 把字典的值转换成字符型
            f.write(k)  # 键和值分行放，键在单数行，值在双数行
            f.write(':')
            f.write(s2 + '\n')


def read_write_Tensor_name_sequence():
    Tensor_name_sequence = {}
    if not os.path.exists('Yolo_Tensor_name_sequence.txt'):
        write_Tensor_name_sequence(Tensor_name_sequence)

    with open('Yolo_Tensor_name_sequence.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            Tensor_name_sequence[line.split(':')[0]] = line.split(':')[1]
    return Tensor_name_sequence


#  输出想要层的 tensor    one: name
def take_one(one, scale=False):
    Tensor_name_sequence = read_write_Tensor_name_sequence()
    name = Tensor_name_sequence[one]
    output_data_name = tflite_model._get_tensor_details(name)  #int(Tensor_name_sequence[name])
    print('=' * 20)
    print('The layer output tensor details is ', output_data_name)
    #print('The layer output tensor is ', tflite_model.get_tensor(name))
    if scale:
        return tflite_model.get_tensor(int(name)),  output_data_name
    return tflite_model.get_tensor(int(name))

def image_zeros(res_img):
    # set all pixel to default
    for j in range(res_img.shape[0]):
        for jj in range(res_img.shape[1]):
            for jjj in range(res_img.shape[2]):
                if (jjj == 0):
                    res_img[j][jj][jjj] = 1
                else:
                    res_img[j][jj][jjj] = 0
    return res_img

def bring_para(name_order):
    print('here')
    sorted(name_order.items(), key=lambda x: x[0], reverse=False)
    print('name_order is ', name_order)
    if name_order[275].split('/')[-1] == 'ReadVariableOp':
        print('heree')
        for c in range(277):
            if c in name_order:
                weigth_tensor = take_one(name_order[c])
                shape = weigth_tensor.shape
                print('weigth_tensor shape is', shape)
                weigth_tensor = np.int8(weigth_tensor)
                with open('weight_para.txt', 'w') as fp:
                    for i in range(shape[1]):
                        for ii in range(shape[2]):
                            for iii in range(shape[0]):
                                for iiii in range(shape[3]):
                                    temp_wei = float_bin_int16(weigth_tensor[iii][i][ii][iiii])
                                    if(temp_wei > 8):
                                        print('超出')
                                        fp.write(str(name_order[c]) + ':')
                                        fp.write(str(temp_wei))
                                        fp.write('\n')
                                    else:
                                        print('不到')

    elif name_order[0].split('/')[-1] == 'Conv2D_bias':
        print('hereeeee')
        for i in len(name_order):
            bias_tensor = take_one(name_order[i])
            shape = bias_tensor.shape
            print('bias_tensor shape is', shape)
            with open('bias_tensor.txt', 'w') as fp:
                for i in range(shape[0]):
                    fp.write(bias_tensor[i])

#def take_scale():


def take_weight():
    Tensor_name_sequence = read_write_Tensor_name_sequence()
    weight_name_order = {}
    bias_name_order = {}
    for para_name, key in Tensor_name_sequence.items():
        para_name_temp = para_name.split('/')[-1]
        if para_name_temp == 'ReadVariableOp':
            weight_name_order[int(key)] = para_name
        if para_name_temp == 'Conv2D_bias':
            bias_name_order[int(key)] = para_name
    bring_para(weight_name_order)
    #bring_para(bias_name_order)

def write_compare(the_tensor_1, the_tensor_2):
    with open("Compare.txt", 'w') as f:
        for i in range(0, 416):
            for ii in range(0, 416):
                f.write('\n' + 'input_1         is ' + '*' * 10)
                for iii in range(0, 3):
                    data_0 = str(int(the_tensor_1[0][i][ii][iii]))
                    # data_0 = str(int(1))
                    f.write(data_0 + '  ')
                f.write('\n')
                f.write('input_1_int8  is ' + '*' * 10)
                for iii in range(0, 3):
                    data_1 = str(the_tensor_2[0][i][ii][iii])
                    f.write(data_1 + '  ')
                f.write('\n')
                f.write('=' * 30)
                f.write('\n')


def main(one, true):

    #image = cv.imread("image.jpg")
    #res_img = cv.resize(image, (416, 416), interpolation=cv.INTER_CUBIC)
    #res_img = image_zeros(res_img)
    #input_data = np.reshape(res_img, shape)
    #input_data = np.array(input_dat, dtype=np.float32)  # 输入
    # print(input_data.shape)

    # 传值
    #tflite_model.set_tensor(input_details[0]['index'], input_data)
    # take_weight()
    # if not true:
    #     return the_tensor
    take_one(one)


tflite_model = tf.lite.Interpreter(model_path="/home/dapang/workspace/mobilenetv3_yolo3_quantized.tflite")  # .contrib
tflite_model.allocate_tensors()
tflite_model.invoke()



if __name__ == "__main__":
    one = 'model_1/activation_25/truediv'
    main(one, 1)
    #Tensor_name_sequence = write_Tensor_name_sequence()