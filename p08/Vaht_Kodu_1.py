#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from filters import create_bandstop
from filters import filter_in_frequecy, plot_filter_time, plot_filter_freq


def main():
    win = pg.GraphicsLayoutWidget(show=True, title="Filtrid")

    ribafilter = create_bandstop(0.05, 0.15, 0.02)

    ribafilter2 = create_bandstop(0.25, 0.35, 0.02)

    ribafilter3 = create_bandstop(0.45, 0.5, 0.02)

    ribafilter = np.convolve(ribafilter, ribafilter2)
    ribafilter = np.convolve(ribafilter, ribafilter3)
    print(len(ribafilter))
    riba = filter_in_frequecy(ribafilter)

    p1 = win.addPlot()
    p1.setLabel('bottom', 'Sagedus murdosa samplimiskiirusest')
    p1.setLabel('left', ' Filtrivõimendus')
    plot_filter_freq(p1, riba)
    win.nextRow()

    QtGui.QApplication.instance().exec_()


if __name__ == "__main__":
    main()