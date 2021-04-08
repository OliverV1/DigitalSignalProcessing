#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import time
import timeit

from yl1_1d_konvolutsioon import input_side_convolution


def measure_run_time(signal_in_1, signal_in_2):
    """
    Funktsioon, mis mõõdab samade sisenditega konvolutsioonile kuluvat aega nii 1. ülesandes
        implementeeritud lahenduse puhul kui ka numpy optimiseeritud implementatsiooni puhul.

    Sisendid:
    signal_in_1 - üks konvolutsiooni sisendsignaalidest
    signal_in_2 - teine konvolutsiooni sisendsignaalidest (võib võtta kui impulsskostet)

    Tagastab:
    time_own - enda implementeeritud konvolutsiooni täitmisele kulunud aeg antud sisendsignaalide korral
    time_numpy - numpy konvolutsiooni täitmisele kulunud aeg samade sisendsignaalide korral
    """

    # Funktsioonide väljakutsed, mille täitmist tuleks ajastada:
    # Aja mõõtmiseks võib kasutada vabalt valitud vahendeid.
    algus = time.time()
    input_side_convolution(signal_in_1, signal_in_2)
    keskmine = time.time()
    np.convolve(signal_in_1, signal_in_2)
    lopp = time.time()

    time_own = keskmine-algus
    time_numpy = lopp-keskmine

    return time_own, time_numpy


def main():
    # Testsignaalide loomine (argument näitab mitme elemendiga massiiv luuakse).
    # Lihtsuse jaoks suurendame mõlemat sisendsignaali sama palju (kasutame võrdse pikkusega sisendsignaale).
    signal_sizes = []
    for i in range(0,10000,100):
        signal_sizes.append(i+1)

    custom_convolution_times = []
    numpy_convolution_times = []

    # Mõõdame ajad kõigi soovitud sisendi suuruste jaoks ja salvestame järjenditesse
    
    for size in signal_sizes:
        signal1 = np.random.rand(size).tolist()  # Kasutame juhuslikke sisendeid sobiva suurusega.
        signal2 = np.random.rand(size).tolist()

        custom_time, numpy_time = measure_run_time(signal1, signal2)
        custom_convolution_times.append(custom_time)
        numpy_convolution_times.append(numpy_time)

    # Kuvame saadud ajad graafikul
    win = pg.GraphicsLayoutWidget(show=True, title="Efektiivsuse analüüs")

    p1 = win.addPlot(title = "Konvolutsiooni aja sõltuvus sisendi suurusest")
    p1.addLegend()
    p1.plot(signal_sizes, custom_convolution_times, name="oma implementatsioon", pen=(0,255,100))
    p1.plot(signal_sizes, numpy_convolution_times, name="numpy", pen=(0,0,255))
    p1.setLabels(bottom="Sisendsignaalide elementide arv", left="Konvolutsioonile kulunud aeg (s)")

    QtGui.QApplication.instance().exec_()


if __name__ == "__main__":
    main()
