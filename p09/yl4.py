import os
import numpy as np
import cv2
import sys


def normaliseeri(pilt):
    miinimum = np.amin(np.real(pilt))
    maksimum = np.amax(np.real(pilt))
    #
    # for i in range(len(pilt)):
    #     i = np.real(pilt[i])
    #     print(i[10])
    for i in range(np.size(pilt,0)):
        for n in range(np.size(pilt,1)):
            pilt[i][n]=((np.real(pilt[i][n])-miinimum)*255)/(maksimum-miinimum)
    pilt = pilt.astype(np.uint8)
    return pilt
def distance(point1,point2): # pole siin vaja
    return np.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def lowpass(D0,imgShape): #pole siin vaja
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            if distance((y,x),center) < D0:
                base[y,x] = 1
    return base

# nullid = np.zeros((500,500),dtype=np.complex)
# for i in range(1,70,2):
#     nullid[3*i][0] += -1j/(i**10)
# muutuja = np.fft.ifft2(nullid)
# normaliseeritud = normaliseeri(muutuja)

img = cv2.imread("task_4_noisy_cat.png",0)
f = np.fft.fft2(np.float32(img))
f_shift = np.fft.fftshift(f)
f_complex = f_shift

f_complex[120][122] = 0
f_complex[204][202] = 0
f_complex = np.fft.ifftshift(f_complex)
f_complex = np.fft.ifft2(f_complex)

# f_bounded = np.abs(f_complex) + 1 # lie between 1 and 1e6
#
# f_img = 255 * f_bounded / np.max(f_bounded)
f_img = f_complex.astype(np.uint8)


cv2.imwrite("yl4tulemus.png", f_img)


print("done")