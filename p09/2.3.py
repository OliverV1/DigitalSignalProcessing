import os
import numpy as np
import cv2
import sys

import numpy as np
import cv2


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

nullid = np.zeros((500,500),dtype=np.complex)
for i in range(1,70,2):
    nullid[3*i][0] += -1j/(i**10)
muutuja = np.fft.ifft2(nullid)
normaliseeritud = normaliseeri(muutuja)




cv2.imwrite("23tulemus.png", normaliseeritud)
print("done")


# picture_size = (500, 500)
# comp_freq = 150
#
#
# freq_shift = 3 * np.pi / 2  # 90, 180 või 270 kraadi
# comp1D = (np.cos(np.arange(picture_size[0]) * 2 * np.pi / comp_freq + freq_shift) + 1) / 2
# comp1D = (comp1D * 255).astype(np.uint8)
# ch_90deg = np.tile(comp1D, (picture_size[1], 1))
# ch_90deg = np.transpose(ch_90deg)
# color_90deg = np.dstack((np.zeros(picture_size, dtype=np.uint8), np.zeros(picture_size, dtype=np.uint8), ch_90deg))
# cv2.imwrite("21tulemus.png", color_90deg)

