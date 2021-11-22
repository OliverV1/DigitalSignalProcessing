#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
from scipy.io.wavfile import read, write
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from filters import create_bandpass
from filters import filter_in_frequecy, plot_filter_freq, plot_filter_time

def main():
    win = pg.GraphicsLayoutWidget(show=True, title="Filtrid")
    oss_sisse = read("yl6.wav")
    oss_sisse = np.array(oss_sisse[1], dtype=np.float32)
    filter_peamine = create_bandpass(0.000002,0.0005 ,0.0001 )

    p1 = win.addPlot()

    plot_filter_time(p1, np.convolve(oss_sisse,filter_peamine))

    QtGui.QApplication.instance().exec_()

if __name__ == "__main__":
    main()