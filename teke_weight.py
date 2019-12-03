# *_*coding:utf-8 *_*

from tflite_take import take_one





def float_bin(s): # s是对应每个数，decimal是10
    den = 0
    if s >= pow(2, 7):
        s = pow(2, 7) - 1
    if s < -pow(2, 7):
        s = -pow(2, 7)
    if s < 0:
        den = (s + pow(2, int(8))) #% pow(2, int(8))
    else:
        den = s
    return int(den)

# ========  1x1卷积核输出
def write_weight(weight):
    print('weight shape is ', weight.shape)
    n, h, w, c = weight.shape
    nn, cc = n/8, c/8
    out = []
    with open('weight.coe', 'w') as f :
        for nn in range(n//8):
            for i in range(h):
                for ii in range(w):
                    for iii in range((nn-1)*8, nn*8):
                        for iiii in range(c):
                            out.append(weight[iii][i][ii][iiii])
                            if len(out) == 64:
                                out.reverse()
                                for m in out:
                                    m = int(float_bin(m) & 0xFFFFFFFF)
                                    f.write('%02x'%m)
                                f.write(',\n')
                                out = []
        out.reverse()
        for m in out:
            m = int(float_bin(m) & 0xFFFFFFFF)
            f.write('%02x' % m)
        f.write(',\n')
        out = []



weight_name = 'model_1/conv2d/Conv2D/ReadVariableOp'
weight = take_one(weight_name)
write_weight(weight)


# def conv2d(input_, output_dim,  wei, bia, stride=1):
#     weight = take_one(wei)
#     print('weight shape is ', weight.shape)
#     weight = np.array(weight_add_zero(weight))
#     print('weight[0][0][0][0] is ',weight[0][0][0])
#     weight = weight.transpose(1, 2, 3, 0)
#     print('weight shape is ', weight.shape)
#
#     conv = tf.nn.conv2d(input_, weight, strides=[1, stride, stride, 1], padding='SAME')
#     biases = take_one(bia)
#     conv = tf.reshape(tf.nn.bias_add(conv, biases), conv.get_shape())
#     conv = (conv * scale_conv * scale_input) #/ scale_output
#     #conv = float_int(conv)
#     return conv
#
#
#
# if __name__ == "__main__":
#     shape = (1, 416, 416, 4)
#     image = take_image(0, shape)
#     image = tf.cast(image, tf.float32)
#     weight_name = 'model_1/conv2d/Conv2D/ReadVariableOp'
#     biases_name = 'model_1/conv2d/Conv2D_bias'
#     scale_name = 'model_1/batch_normalization/FusedBatchNormV3'
#     #write_first_para2bin(weight_name, biases_name, scale_name)
#     print('image shape is', image.get_shape())
#     conv = conv2d(image, 16, weight_name, biases_name, stride=2)
#     print('conv type is ', type(conv))
#     print('conv shape is ', conv.shape)
#     array = conv.numpy()
#     print('array type is ', type(array))
#     array = np.int8(array)
#     print('=' * 20)
#     print(' is', conv)