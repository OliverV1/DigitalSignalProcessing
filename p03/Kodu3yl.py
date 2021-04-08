#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np

from yl4_2d_konvolutsioon import convolve


def box_blur(img,array ):

    return convolve(img,
                         array/array.sum())


def gaussian_blur(img,array):
    return convolve(img,
                    array / array.sum())



def main():
    # Hägustamise kernelite puhul tuleb konvolutsiooni tulemus jagada kerneli summaga.

    # NB! Selle kerneli saab luua lihtsamalt kasutades käsku np.ones((5,5))
    # Oma implementatsiooni jaoks tuleb luua sobiva suurusega kernel
    simple_blur_5x5 = np.ones((11,11))

    gaussian_5x5 = np.array((
        [1,  4,  7,  4, 1],
        [4, 16, 26, 16, 4],
        [7, 26, 41, 26, 7],
        [4, 16, 26, 16, 4],
        [1,  4,  7,  4, 1]), dtype="float32")

    sharpen = np.array((
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0],
    ), dtype="float32")


    # Loeme pildi sisse ühe kanaliga (hallskaala pildina).
    # Saadav img muutuja on 2-mõõtmeline massiiv, millel saab rakendada
    # kõiki numpy massiivi töötlemise võtteid.
    img = cv2.imread("python_logo.png", cv2.IMREAD_GRAYSCALE)





    # Järgnevad käsud on vajalikud pildi kuvamiseks kasutades OpenCV teeki.
    cv2.imshow("box_blur", box_blur(img,simple_blur_5x5))
    cv2.imshow("gaussian_blur", gaussian_blur(img, sharpen))


    #cv2.imshow("sobel_y_edge", sobel_y_edge(img, sobel_y))

    #cv2.imshow("sisend",tavaline)
    #cv2.imshow("Input image", tavaline)# Kuvame loodud aknas massiivi pildina
    cv2.waitKey(0)  # Anname kontrolli OpenCV aknale. Programm blokeerub siin kuni akna sulgemiseni.
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
