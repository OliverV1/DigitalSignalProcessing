#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui


def main():
    # Loome NumPy't kasutades aja väärtuste massiivi,
    # kus väärtused on 0st 12ni, 0.03 ühikulise sammuga (kokku 400 väärtust)
    t = np.arange(0, 12, 0.03)
    pendulum1 = 5 * np.cos(t)
    pendulum2 = 5 * np.sin(t - np.pi / 2)

    # Loome graafikud kasutades PyQtGraph'i
    # Rohkem informatiooni leiab uurides dokumentatsiooni https://pyqtgraph.readthedocs.io/en/latest/plotting.html
    # ning muidugi otsides näiteid internetist https://pyqtgraph.readthedocs.io/en/latest/introduction.html#examples
    win = pg.GraphicsLayoutWidget(show=True, title="Pendlite positsioon ajas")
    # legend = pg.LegendItem(pen="r")

    #p1 = win.addPlot(title="5 * np.cos(t)", y=pendulum1, x=t, pen=(255, 0, 0),name = "test")
    p1 = win.addPlot(title="5 * np.cos(t)")
    p1.addLegend()
    p1.plot(y=pendulum1, x=t, pen=(255, 0, 0),name = "5 * np.cos(t)")
    p1.setLabel('bottom', 'Aeg', 's')
    p1.setLabel('left', 'Tasakaaluasend ', 'cm')
    p1.showGrid(x=True, y=True)
    win.nextRow()

    #p2 = win.addPlot(title="5 * np.sin(t - np.pi/2)", x=t, y=pendulum2, pen=(255, 0, 0))
    p2 = win.addPlot(title="5 * np.sin(t - np.pi/2)")
    p2.addLegend()
    p2.plot(x=t, y=pendulum2, pen=(255, 0, 0),name="5 * np.sin(t - np.pi/2)")
    p2.setLabel('bottom', 'Aeg', 's')
    p2.setLabel('left', 'Tasakaaluasend ', 'cm')
    p2.showGrid(x=True, y=True)
    win.nextRow()

    p3 = win.addPlot(title="Mõlemad koos")
    p3.addLegend()
    p3.plot(t, pendulum1, name="koosinus")
    p3.plot(t, pendulum2, pen=(255, 0, 0), name="siinus")
    p3.setLabel('bottom', 'Aeg', 's')
    p3.setLabel('left', 'Tasakaaluasend ', 'cm')
    p3.showGrid(x=True, y=True)

    # Alustame GUI peatsükliga, blokeeruv

    # legend.setParentItem(win.graphicsItem())

    QtGui.QApplication.instance().exec_()


if __name__ == "__main__":
    main()
