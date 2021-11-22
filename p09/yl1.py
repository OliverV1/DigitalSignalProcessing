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

nullid = np.zeros((500,500),dtype=np.complex)
nullid[0][3] += 2
muutuja = np.fft.ifft2(nullid)
normaliseeritud = normaliseeri(muutuja)
cv2.imwrite("tulemus1.png", normaliseeritud)
# comp_freq = 200
# #180,3
#
# picture_size = (500, 500)
# freq_shift = 2 * np.pi  # 90, 180 või 270 kraadi
# comp1D = (np.cos(np.arange(picture_size[0]) * 2 * np.pi / comp_freq + freq_shift) + 1) / 2
# comp1D = (comp1D * 255).astype(np.uint8)
# bw_90deg = np.tile(comp1D, (picture_size[1], 1))
# cv2.imwrite("test.png", bw_90deg)



