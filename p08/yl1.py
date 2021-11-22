#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from filters import create_lowpass
from filters import filter_in_frequecy, plot_filter_freq, plot_filter_time,create_blackmann_window

def main():
    # Siin failis tuleks luua ja visualiseerida 1. ülesandes nõutud parameetritega madalpääsfilter.
    # Näidisena on toodud ühe madalpääsfiltri loomine ja visualiseerimine.

    win = pg.GraphicsLayoutWidget(show=True, title="Filtrid")

    example_lowpass = create_lowpass(0.25, 0.05)
    example_lowpass_freq = filter_in_frequecy(example_lowpass)



    tulemus = np.multiply(example_lowpass,create_blackmann_window(81))
    tulemus = tulemus / np.sum(tulemus)
    blackman = filter_in_frequecy(tulemus)




    p1 = win.addPlot()
    plot_filter_time(p1, example_lowpass)
    win.nextRow()

    p2 = win.addPlot()
    plot_filter_freq(p2, example_lowpass_freq)
    win.nextRow()

    p3 = win.addPlot()
    plot_filter_freq(p3, example_lowpass_freq, dB_scale=True)
    win.nextRow()



    p4 = win.addPlot()
    plot_filter_time(p4, tulemus)
    win.nextRow()

    p5 = win.addPlot()
    plot_filter_freq(p5, blackman)
    win.nextRow()

    p6 = win.addPlot()
    plot_filter_freq(p6, blackman, dB_scale=True)
    win.nextRow()

    QtGui.QApplication.instance().exec_()

if __name__ == "__main__":
    main()
