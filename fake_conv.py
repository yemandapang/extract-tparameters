# *_*coding:utf-8 *_*
import numpy as np
from functools import reduce
from operator import mul
from tflite_take import take_one
from utils import *
from PIL import Image
np.set_printoptions(threshold=np.inf)

def weight_add_zero(weight):
    zeros = np.zeros((weight.shape[1],weight.shape[2],1))
    zeros = np.int8(zeros)
    array = []
    for i in range(weight.shape[0]):
        temp = np.append(weight[i], zeros, axis=2)
        array.append(temp)
    return np.array(array)

def take_image(image_path, image_shape):
    out = []
    zeros = np.zeros((image_shape[1],image_shape[2], 1))
    for i in range(4):
        img = Image.open(image_path + 'test' + str(i) + '.jpg')
        img = img.resize((image_shape[1],image_shape[2]), Image.ANTIALIAS)
        image = np.array(img)
        image = image[:, :, 0:3]
        print('iamge.shape', image.shape)
        image = np.append(image, zeros, axis=2)
        print('iamge.shape', image.shape)
        out.append(image)
    print('np.array(out)', np.array(out).shape)
    out = np.array(out)
    print('out.shape', out.shape)
    return out

def take_feature(image_shape, generate=0):
    if generate:
        input = np.random.randint(0, 255, image_shape).astype(dtype=np.float) #255:uint8
    else:
        input = read_fake_feature(image_shape)  # read a fake pic
    print('input.shape is', input.shape)
    return  input

def im2con(input, k_size, padding, stride):
    out_size = (input.shape[2] - k_size + 2 * padding) // stride + 1
    print('out_size shape is', out_size)
    out = []
    for i in range(input.shape[0]):
        for ii in range(1, out_size + 1):
            for iii in range(1, out_size + 1):
                a = input[i:i+1, (ii - 1)*stride:k_size+(ii - 1)*stride, (iii - 1)*stride:k_size+(iii - 1)*stride, :]
                # a = input[i:i+1, ii+inter:k_size+(ii*inter), iii*inter:k_size+(iii*inter), :]
                a = a.reshape(input.shape[3] * k_size *k_size)
                out.append(a)
    return out

def Conv2d(input, weight, bias, padding=0, stride=1):
    image = im2con(input, weight.shape[2], padding, stride)
    image = np.array(image)
    weight = np.reshape(weight, (-1, weight.shape[0]))

    print('weigth max ', np.max(weight))
    print('images changed shape is ', image.shape)
    print('weight changed shape is ', weight.shape)
    print('weight dtype is ', weight.dtype)
    print('image  dtype is ', image.dtype)

    result = np.dot(image, weight)
    print('result shape is', result.shape)
    print('result dtype is', result.dtype)
    result = np.reshape(result, (input.shape[0], 208, 208, -1)).astype(dtype=np.int)
    write_input(result, '2_result_no_bias')

    # 计算biase
    # result = result.transpose(1,2,3,0)
    # result = result + bias
    # result = result.transpose(3,0,1,2)
    # write_input(result, '2_result_yes_bias')

    return result

# def take_scale():


def main():
    # 提取特征图
    image_shape = (4, 208, 208, 16)
    # image_path = '/home/dapang/workspace/'
    # input =  take_image(image_path, image_shape)  # read real pic
    input =  take_feature(image_shape, generate=0)             # make a fake pic  1:生成新的feature

    # 提取weight
    weight_name = 'model_1/conv2d_1/Conv2D/ReadVariableOp'
    weight = take_one(weight_name)
    #weight = weight_add_zero(weight) # 第一层卷积需要调用此函数
    #weight_shape = [4, 3, 3, 16]
    #weight  = np.random.randint(0,576,weight_shape)

    # 提取bias
    bias_name = 'model_1/conv2d_1/Conv2D_bias'
    bias = take_one(bias_name)

    # 写coe文件
    # write_weight(weight)
    # write_input(input, 'input')
    # write_bias(bias)

    # 计算
    padding = 0
    stride = 1
    result = Conv2d(input, weight, bias, padding=padding, stride=stride)
    return result

if __name__ == '__main__':
    result = main()
    b = np.max(result)
    print('result max is', b)