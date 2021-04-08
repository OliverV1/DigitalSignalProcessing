#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import scipy as scipy
from scipy import signal
from numpy.fft  import fft2, ifft2
import math
##https://github.com/ashushekar/image-convolution-from-scratch


"""def convolve(image, kernel):
    kernel = np.flipud(np.fliplr(kernel))
    output = np.zeros_like(image)
    image_padded = np.zeros((image.shape[0] + 2, image.shape[1] + 2))

    image_padded[1:-1, 1:-1] = image
    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            output[y, x]=(kernel * image_padded[y: y+3, x: x+3]).sum()
    return output"""

def convolve(image, kernel):
    # Flip the kernel
    kernel = np.flipud(np.fliplr(kernel))
    kernel_suurus = len(kernel)
    muutuja = (math.floor(len(kernel)/2))*2
    alustamise_kordaja = math.floor(len(kernel)/2)
    x = image.shape[0]
    y = image.shape[1]
    output = np.zeros_like(image)

    image_padded = np.zeros((x+muutuja,y+muutuja))
    image_padded[1*alustamise_kordaja:-1*alustamise_kordaja, 1*alustamise_kordaja:-1*alustamise_kordaja] = image


    # Loop over every pixel of the image
    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            # element-wise multiplication of the kernel and the image
            output[y, x] = (kernel * image_padded[y: y+kernel_suurus, x: x+kernel_suurus]).sum()

    return output

"""def convolve(image,kernel):
    return scipy.signal.convolve2d(image,kernel,mode = "same")
"""





def main():

    input_signal = np.random.randint(0, 2, (5, 5))
    # kernel = np.random.randint(1, 2, (3,3))
    # print(convolve(input_signal, kernel))



    # img = np.array((
    #     [1, 3, 3, 2],
    #     [7, 9, 8, 9],
    #     [7, 8, 6, 7],
    #     [8, 9, 9, 7]), dtype="int")
    #
    # kernel = np.array((
    #     [-1, -2, -1],
    #     [0, 0, 0],
    #     [1, 2, 1]), dtype="int")
    #
    # print(convolve(img, kernel))





if __name__ == "__main__":
    main()
