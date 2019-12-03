#!/usr/bin/env python

import struct

import numpy as np
from PIL import Image
import os

np.set_printoptions(threshold=np.inf)


def read(image_path):
    img = Image.open(image_path)
    img = img.resize((416, 416), Image.ANTIALIAS)
    imge = np.array(img)
    imge = imge[:, :, 0:3]
    return imge


def prewhiten(x): # x是read的结果
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0 / np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1 / std_adj)
    return y


def float_bin(s, decimal): # s是对应每个数，decimal是10
    temp = float(s) * pow(2, int(decimal))
    den = 0
    if temp >= pow(2, 7):
        temp = pow(2, 7) - 1
    if temp < -pow(2, 7):
        temp = -pow(2, 7)
    if temp < 0:
        den = (temp + pow(2, int(8))) % pow(2, int(8))
    else:
        den = temp

    return int(den)

def float_bin_int8(s): # s是对应每个数，decimal是10


    #截断 -128---- 127


    #temp = float(s) * pow(2, int(decimal))
    den = 0
    if s >= pow(2, 7):
        s = pow(2, 7) - 1
    if s < -pow(2, 7):
        s = -pow(2, 7)
    if s < 0:
        den = (s + pow(2, int(8))) % pow(2, int(8))
    else:
        den = s

    return int(den)



def get_image(num,shape):   #读取num张图片
	input_data = []
	for i in range(shape[0]):   # 图片数遍历
		name = './test' + str(i) + '.jpg'
		image = read(name)
		zeros = np.zeros((416, 416, 1), dtype=np.uint8)
		input_data.append(np.append(image, zeros, axis=2))
		#input_data[i] = prewhiten(input_data[i])     //  白化
		#input_data.append(image)
		#input_data = np.array(input_data)
		#np.append(input_data, zeros, axis=1)
	input_data = np.reshape(input_data, shape)
	input_data = np.array(input_data)
	print('input_data.shape is', input_data.shape)
	return input_data


def get_image_test(num,shape):   #读取num张图片
	input_data = np.zeros(shape, dtype=np.int32)
	#input_data = []
	for i in range(input_data.shape[0]):	# 对图片遍历
		for ii in range(input_data.shape[3]):		# 对通道遍历
			for iii in range(input_data.shape[1]):
				for iiii in range(input_data.shape[2]):
					if (i == 0):		# 第一张图片对应的R通道置为1
						input_data[i][iii][iiii][0] = 1
					if (i == 1):		# 第二张图片对应的G通道置为1
						input_data[i][iii][iiii][1] = 1
					if (i == 2):		# 第三张图片对应的B通道置为1
						input_data[i][iii][iiii][2] = 1
					if (i == 3):		# 第四张图片对应的全通道置为1
						input_data[i][iii][iiii][ii] = 1
	return input_data


def main(true, shape):
	image_num = 4
	image = get_image(image_num, shape)

	image_1 = image
	#image = image - 128
	#image = np.int8(image)
	#print(image)
	out = []
	with open("image.coe", "w") as fp:
		for i in range(shape[1]):#列
			for ii in range(shape[2]):#行
				for iii in range(shape[0]):# 图片数
					for iiii in range(shape[3]):
						out.append(image[iii][i][ii][iiii])
						if len(out) == 32:
							out.reverse()
							for m in out:
								#m = int(float_bin(m) & 0xFFFFFFFF)
								fp.write('%02x'%m)
							fp.write(',\n')
							out = []
						# temp = float_bin_int8(temp)
						# temp -= 128
						#temp = struct.pack("i", int(temp))   #每个数放在0
						#fp.write(temp_bin)
	#测试
	with open("test_1.txt", "w") as fp:
		for a in range(shape[1]):  # 列
			for i in range(shape[2]):  # 行
				for k in range(shape[3]):  #
					for j in range(shape[0]):
						# temp = float_bin(image[j][a][i][k], 2)
						temp = image[j][a][i][k]
						#temp = float_bin_int8(temp)
						temp -= 128
						#temp = struct.pack("i", int(temp))  # 每个数放在0
						fp.write(str(temp))
						fp.write('  ')
					fp.write('\n')
						# fp.write(temp_bin)

	if not true:
		return image

if __name__ == "__main__":
    shape = (4, 416, 416, 4)
    main(1, shape)

