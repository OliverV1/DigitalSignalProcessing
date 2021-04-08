#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

# Kasutage seda funktsiooni oma impulsside kujutamiseks
def plot_stem(plot, y, x=None, **kwargs):
    if x is None: x = np.arange(y.size)
    y0_pairs = np.dstack((np.zeros(y.shape[0]), y)).flatten()
    plot.plot(x=np.repeat(x, 2), y=y0_pairs, connect='pairs', pen=pg.mkPen('w', width=3), **kwargs)
    plot.plot(y, pen=None, symbol='o',symbolBrush="r")

def funktsioon(pikkus = 0,nihe=999999999,amplituut=999999999):
    if nihe <999999999:
        if amplituut<999999999:
            return np.insert(np.zeros(pikkus-1),nihe*-1,amplituut)
        return np.insert(np.zeros(pikkus-1),nihe*-1,1)
    return np.insert(np.zeros(pikkus-1),0,1)






def main():

    rng = np.random.default_rng()
    win = pg.GraphicsLayoutWidget(show=True, title="Impulside summa")
    pikkus = 7

    p1 = win.addPlot()
    print(funktsioon(5,-1,-3))
    print("tere")

    n=0
    tulemus = np.zeros(pikkus)
    tulemus += funktsioon(pikkus,n-1,-2)+funktsioon(pikkus,n,4)+funktsioon(pikkus,n-2,3)+funktsioon(pikkus,n-1,4)+funktsioon(pikkus,n-2,1)+funktsioon(pikkus,n,-1)
    

    

    plot_stem(p1, funktsioon(pikkus,n-1,-2))
    
    
    
   

    p2 = win.addPlot()
    plot_stem(p2, funktsioon(pikkus,n,4))

    p3 = win.addPlot()
    plot_stem(p3, funktsioon(pikkus,n-2,3))
    win.nextRow()

    p4 = win.addPlot()
    plot_stem(p4, funktsioon(pikkus,n-1,4))

    p5 = win.addPlot()
    plot_stem(p5, funktsioon(pikkus,n-2,1))

    p6 = win.addPlot()
    plot_stem(p6, funktsioon(pikkus,n,-1))
    win.nextRow()

    p7 = win.addPlot(colspan=3)
    plot_stem(p7, tulemus )#funktsioon(pikkus,n-1,-2)+funktsioon(pikkus,n,4)+funktsioon(pikkus,n-2,3)+funktsioon(pikkus,n-1,4)+funktsioon(pikkus,n-2,1)-funktsioon(pikkus,n,-1)

    QtGui.QApplication.instance().exec_()

if __name__ == "__main__":
    main()
