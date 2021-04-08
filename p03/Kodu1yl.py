# -*- coding: utf-8 -*-
"""
This example demonstrates many of the 2D plotting capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with
the left/right mouse buttons. Right click on any plot to show a context menu.
"""



from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from scipy import signal


#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')
t = np.linspace(0, 1, 500, endpoint=False)



# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)
p3 = win.addPlot(title="Kodutoo")
p3.addLegend()

p3.plot(y=signal.square(2 * np.pi  * 5*t)+1, name="SAMPLE1")
p3.plot(y=signal.square(2 * np.pi  * 2*t)+1,name="SAMPLE2",pen=(255, 255, 0))
p3.plot(y=np.convolve(signal.square(2 * np.pi * 5* t), signal.square(2 * np.pi  * 2*t)), pen=(255, 0, 0), name="Konvuleeritud")
p3.setLabel('bottom', 'Aeg', 's')
p3.setLabel('left', 'Amplituut ', '(x)')
p3.showGrid(x=True, y=True)


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
