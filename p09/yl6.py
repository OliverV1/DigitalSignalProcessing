import os
import numpy as np
import cv2
import sys
from time import*
def callback(data):
    # Siin ei tehta mitte midagi, aga liuguri loomisel on vaja lisada callback funktsioon
    pass

def distance(point1,point2): # pole siin vaja
    return np.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def normaliseeri(pilt):
    miinimum = np.amin(np.real(pilt))
    maksimum = np.amax(np.real(pilt))
    #
    # for i in range(len(pilt)):
    #     i = np.real(pilt[i])
    #     print(i[10])
    for i in range(np.size(pilt,0)):
        for n in range(np.size(pilt,1)):
            pilt[i][n]=((np.real(pilt[i][n])-miinimum))/(maksimum-miinimum)
    return pilt

# nullid = np.zeros((500,500),dtype=np.complex)
# for i in range(1,70,2):
#     nullid[3*i][0] += -1j/(i**10)
# muutuja = np.fft.ifft2(nullid)
# normaliseeritud = normaliseeri(muutuja)

img = cv2.imread("task_6-7_noisy.png",0)
f = np.fft.fft2(np.float32(img))
f_shift = np.fft.fftshift(f)


trackbar_value = 179
trackbar_value_diameeter = 12
trackbar_value_halve = 92
B_G = 156
cv2.namedWindow("Pilt")
cv2.createTrackbar("lävend", "Pilt", trackbar_value, 255, callback)
cv2.createTrackbar("Diameeter", "Pilt", trackbar_value_diameeter, 255, callback)
cv2.createTrackbar("Hälve", "Pilt", trackbar_value_halve, 100, callback)
cv2.createTrackbar("Väärtus", "Pilt", B_G, 255, callback)

while True:
    f_complex = f_shift.copy()
    väärtused = (np.log(f_complex)/np.amax(np.log(f_complex)))*255
    f_img = f_complex

    rows, cols = np.shape(f_img)
    kerneli_suurus_odd = int(np.ceil(cv2.getTrackbarPos("Diameeter", "Pilt")) // 2 * 2 + 1)

    filter = cv2.getGaussianKernel(ksize=kerneli_suurus_odd,sigma=np.log10(cv2.getTrackbarPos("Hälve", "Pilt"))) #log vajalik et saaksime standardhälvet sujuvamalt muuta
    #filter = cv2.getGaussianKernel(ksize=kerneli_suurus_odd,sigma=1) #log vajalik et saaksime standardhälvet sujuvamalt muuta
    filter = np.matmul(filter,np.transpose(filter)) #loome õige suurusega filtri
    filter = normaliseeri(filter)
    filter = np.abs(1-filter)  #vastandväärtus filtrist

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%") #senini kontrollitud ja õige
    offset = int(np.floor(kerneli_suurus_odd/2)) #leiame offseti null punktist nii paremale kui ka üles alla
    summa = 1   #vahepealne muutuja nullide välistamiseks
    mask = np.ones_like(f_img)
    koopia_väärtused = väärtused.copy()
    for x in range(cols):
        for y in range(rows):
            try:
                if cv2.getTrackbarPos("lävend", "Pilt") < (väärtused[y][x]):
                    summa = 1
                    for i in mask[y - offset:y + offset + 1,x - offset:x + offset + 1]:
                        for j in i:
                            summa*=j
                    if summa !=0:
                        f_img[y - offset:y + offset + 1,x - offset:x + offset + 1] *= filter
                        mask[y - offset:y + offset + 1,x - offset:x + offset + 1 ] = 0



                else:
                    pass
            except:
                pass

    #logaritm = np.log(f_img)
    #normaliseerimine = np.log(koopia_väärtused+0.00001)
    #normaliseerimine = (np.abs(normaliseerimine)/(np.amax(np.abs(normaliseerimine))))*255
    #f_img = koopia_väärtused.astype(np.uint8)


    f_complex = np.fft.ifftshift(f_img)
    f_complex = np.fft.ifft2(f_complex)
    #normaliseerimine = (np.abs(f_complex) / (np.amax(np.abs(f_complex)))) * 255
    f_img = f_complex.astype(np.uint8)
    f_img = np.where(f_img<cv2.getTrackbarPos("Väärtus", "Pilt"),f_img*0,(f_img*0)+255)  # see on 9.7 osa
    cv2.imshow("Pilt", f_img)
    # Määrame pildi iga piksli väärtuseks liuguri väärtuse
    # Kuvame pilti aknas "Pilt"
    #cv2.imshow("Pilt", f_img)
    # Q-tähe vajutamise korral programm sulgub
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("yl6tulemus.png", f_img)
        break



print("done")