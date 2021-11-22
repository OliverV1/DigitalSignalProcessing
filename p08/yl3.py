#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from filters import create_highpass_spectral_inversion, create_highpass_spectral_reversal,create_lowpass,create_blackmann_window
from filters import filter_in_frequecy, plot_filter_time, plot_filter_freq

def main():
    win = pg.GraphicsLayoutWidget(show=True, title="Filtrid")

    example_lowpass = create_lowpass(0.15, 0.05)

    tulemus = np.multiply(example_lowpass, create_blackmann_window(len(example_lowpass)))
    tulemus = tulemus / np.sum(tulemus)


    inversioon = create_highpass_spectral_inversion(0.15, 0.05)

    nihutamine = create_highpass_spectral_reversal(0.15, 0.05)

    example_lowpass_freq = filter_in_frequecy(inversioon)

    nihutamine_freq = filter_in_frequecy(nihutamine)

    p1 = win.addPlot()
    plot_filter_time(p1, tulemus)
    win.nextRow()

    p2 = win.addPlot()
    plot_filter_time(p2, inversioon)
    win.nextRow()

    p3 = win.addPlot()
    plot_filter_freq(p3, example_lowpass_freq)
    win.nextRow()

    p4 = win.addPlot()
    plot_filter_freq(p4, example_lowpass_freq, dB_scale=True)
    win.nextRow()




    p5= win.addPlot()
    plot_filter_time(p5, nihutamine)
    win.nextRow()

    p6 = win.addPlot()
    plot_filter_freq(p6, nihutamine_freq)
    win.nextRow()

    p7 = win.addPlot()
    plot_filter_freq(p7, nihutamine_freq, dB_scale=True)
    win.nextRow()


    QtGui.QApplication.instance().exec_()

if __name__ == "__main__":
    main()
