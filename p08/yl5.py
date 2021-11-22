#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from filters import create_bandpass
from filters import filter_in_frequecy, plot_filter_time, plot_filter_freq

def main():
    win = pg.GraphicsLayoutWidget(show=True, title="Filtrid")
    ribafilter = create_bandpass(0.25,0.45 ,0.01 )

    riba = filter_in_frequecy(ribafilter)


    p1 = win.addPlot()
    plot_filter_freq(p1, riba)
    win.nextRow()

    QtGui.QApplication.instance().exec_()
if __name__ == "__main__":
    main()
