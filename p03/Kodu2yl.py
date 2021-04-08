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

konvulutsioon_list = [1,2]
#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)
naide1=[3,4,3,9,5]
naide2=[6,8,9,4,4]
naide3=[9,4,6,3,1]
offset_et_paremini_arusaada=1
win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')
t = np.linspace(0, 1, len(naide1)+len(naide2)-1, endpoint=False)





# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)
p3 = win.addPlot(title="Kommu")
p3.addLegend()

p3.plot(x= t, y=np.convolve(naide1,naide2), name="Originaal")
p3.plot(x = t, y=np.convolve(naide2,naide1)+offset_et_paremini_arusaada, pen=(255, 0, 0), name="Muudetud tehetejärekord")
p3.setLabel('bottom', 'Aeg', 's')
p3.setLabel('left', 'Amplituut ', '(x)')
p3.showGrid(x=True, y=True)


offset_et_paremini_arusaada=20
t2 = np.linspace(0, 1, len(naide1)+len(naide2)+len(naide3)-2, endpoint=False)
p1 = win.addPlot(title="Assu")
p1.plot(x= t2, y=np.convolve(np.convolve(naide1,naide2),naide3), name="Originaal")
p1.plot(x = t2, y=np.convolve(np.convolve(naide3,naide2),naide1)+offset_et_paremini_arusaada, pen=(255, 0, 0), name="Muudetud tehetejärekord")
p1.setLabel('bottom', 'Aeg', 's')
p1.setLabel('left', 'Amplituut ', '(x)')
p1.showGrid(x=True, y=True)
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
