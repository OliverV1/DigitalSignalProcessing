#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

def callback(data):
    # Siin ei tehta mitte midagi, aga liuguri loomisel on vaja lisada callback funktsioon
    pass

def main():
    # Loome tühja pildi
    img = np.zeros((100, 100), dtype=np.uint8)
    # Loome muutuja, kus hoida liuguri väärtust
    trackbar_value = 0
    # Loome akna, kus pilti ja liugurit kuvada
    cv2.namedWindow("Pilt")
    # Lisame aknasse liuguri, mis muudab muutuja trackbar_value väärtust
    # Liuguri maksimumväärtus on 255
    cv2.createTrackbar("lävend", "Pilt", trackbar_value, 255, callback)

    # Selleks, et jooksvaid muutusi kuvada, on mõistlik kasutada tsüklit.
    # Tasub mõelda, milline osa programmist peab olema tsükli sees
    # ja mida on tarvis teha vaid ühe korra (mis ei sõltu lävendist).
    while True:
        # Määrame pildi iga piksli väärtuseks liuguri väärtuse
        img[:] = cv2.getTrackbarPos("lävend", "Pilt")
        # Kuvame pilti aknas "Pilt"
        cv2.imshow("Pilt", img)
        # Q-tähe vajutamise korral programm sulgub
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Programmi lõpus suletakse kõik aknad
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

