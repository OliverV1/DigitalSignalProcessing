#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import numpy as np

def main():
    win = pg.GraphicsLayoutWidget(show=True, title="Sagedusvahemikud")
    signaali_graafik = win.addPlot()

    frequency = 70  # Our played note will be 440 Hz
    fs = 44100  # 44100 samples per second
    t = np.arange(0,1,1/fs)
    note = np.sin(frequency * t * 2 * np.pi)

    frequency = 80
    noot2 = np.sin(frequency * t * 2 * np.pi)

    kokku = note+noot2
    signaali_graafik.plot(kokku,x=t)

    # Looge siinused, liitke need kokku ning kujutage graafikul






    win.nextRow()
    sagedus_graafik = win.addPlot()
    sagedus_graafik.addLegend()
    fft = np.fft.fft(kokku)
    sagedus_graafik.plot((np.abs(fft)/len(kokku))[0:150],name = "41k")

    fft =  np.fft.fft(kokku[0:15000])
    sagedus_graafik.plot((np.abs(fft)/len(fft))[0:150],pen="g",name = "15k")

    fft = np.fft.fft(kokku[0:7000])
    sagedus_graafik.plot((np.abs(fft) / len(fft))[0:150],pen="r",name = "7k")

    fft = np.fft.fft(kokku[0:2000])
    sagedus_graafik.plot((np.abs(fft) / len(fft))[0:150],pen="b",name = "2k")

    fft = np.fft.fft(kokku[0:6500])
    sagedus_graafik.plot((np.abs(fft) / len(fft))[0:150], pen=(125,125,0), name="eristamiseks")

    # TODO
    # Leidke signaali sagedusvahemikud

    QtGui.QApplication.instance().exec_()

if __name__ == "__main__":
    main()
