import os
import numpy as np
import cv2
import sys
def callback(data):
    # Siin ei tehta mitte midagi, aga liuguri loomisel on vaja lisada callback funktsioon
    pass

def distance(point1,point2): # pole siin vaja
    return np.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)



# nullid = np.zeros((500,500),dtype=np.complex)
# for i in range(1,70,2):
#     nullid[3*i][0] += -1j/(i**10)
# muutuja = np.fft.ifft2(nullid)
# normaliseeritud = normaliseeri(muutuja)

img = cv2.imread("task_5_very_noisy_cat.png",0)
f = np.fft.fft2(np.float32(img))
f_shift = np.fft.fftshift(f)


trackbar_value = 255
cv2.namedWindow("Pilt")
cv2.createTrackbar("lävend", "Pilt", trackbar_value, 255, callback)
while True:
    f_complex = f_shift.copy()
    väärtused = (np.log(f_complex)/np.amax(np.log(f_complex)))*255
    f_img = f_complex
    raadius = 0

    rows, cols = np.shape(f_img)
    center = (rows / 2, cols / 2)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    for x in range(cols):
        for y in range(rows):
            if distance((y,x),center) < raadius:
                pass
            elif cv2.getTrackbarPos("lävend", "Pilt") < (väärtused[y][x]):
                print(y,x)
                f_img[y][x]=0
            else:
                pass


    f_complex = np.fft.ifftshift(f_img)
    f_complex = np.fft.ifft2(f_complex)
    f_img = f_complex.astype(np.uint8)

    # Määrame pildi iga piksli väärtuseks liuguri väärtuse
    # Kuvame pilti aknas "Pilt"
    cv2.imshow("Pilt", f_img)
    # Q-tähe vajutamise korral programm sulgub
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



print("done")