# *_*coding:utf-8 *_*
import numpy as np
import PIL


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

def write_weight(weight):
    print('weight shape is ', weight.shape)
    n, h, w, c = weight.shape
    nn, cc = n/8, c/8
    out = []
    with open('weight.coe', 'w') as f :
        for i in range(h):
            for ii in range(w):
                for nn in range(n//8):
                    if c == 1:
                        for iii in range(nn * 8, (nn + 1) * 8 - 1):  # batch
                            out.append(weight[iii][i][ii][iiii])
                            if len(out) == 64:
                                out.reverse()
                                for m in out:
                                    m = int(float_bin(m) & 0xFFFFFFFF)
                                    f.write('%02x' % m)
                                f.write(',\n')
                                out = []
                    else:
                        for cc in range(c//8):
                            for iii in range(nn*8, (nn+1)*8-1):  # batch
                                for iiii in range(cc*8, (cc+1)*8-1):    #channel
                                    out.append(weight[iii][i][ii][iiii])
                                    if len(out) == 64:
                                        out.reverse()
                                        for m in out:
                                            m = int(float_bin(m) & 0xFFFFFFFF)
                                            f.write('%02x' % m)
                                        f.write(',\n')
                                        out = []

def write_input(image,name):
    n, h, w, c = image.shape
    out = []
    image = image.astype(dtype=np.int)
    print('max is', np.max(image))
    print('image shape is',image.shape)
    with open(name + '.coe', 'w') as fp:
        for i in range(h):
            for ii in range(w):
                for iii in range(n): # batch
                    for iiii in range(c):   # channel
                        out.append(image[iii][i][ii][iiii])
                        if len(out) == 32:
                            out.reverse()
                            for m in out:
                                # m = int(float_bin(m) & 0xFFFFFFFF)
                                fp.write('%02x'%m)
                            fp.write(',\n')
                            out = []

def write_bias(bias):
    out = []
    with open('bias.coe', 'w') as f:
        for m in bias:
            out.append(m)
            if len(out) == 2:
                for m in out:
                    f.write('%04x' % m)
                f.write('\n')

def write_fake_feature(input):
    n, h, w, c = input.shape
    input = input.astype(dtype=np.int)
    with open('feature.txt', 'w') as f:
        for i in range(n):
            for ii in range(h):
                for iii in range(w):
                    for iiii in range(c):
                        f.write(str(input[i][ii][iii][iiii]))
                        f.write(' ')
                    f.write('\n')

def read_fake_feature(input):
    n, h, w, c = input
    with open('feature.txt', 'r') as f:
        for i in range(n):
            for ii in range(h):
                for iii in range(w):
                    line = f.readline().split(' ')
                    for iiii in range(c):
                        input[i][ii][iii][iiii] = line[iiii]
