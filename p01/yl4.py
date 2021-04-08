#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import serial

data_line = None
listikene=[]
i=0

def on_update():
    global data_line
    global i
    # Implementeerige siia Arduinost andmete küsimise ja kuvamise loogika
    ser = serial.Serial('/dev/ttyUSB0')
    ser_bytes = ser.readline()
    decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    if (len(listikene)<500):
        listikene.append(decoded_bytes)
    else:
        listikene.pop(0)
        listikene.append(decoded_bytes)



    data_line.setData(listikene)

def main():
    global data_line
    win = pg.GraphicsLayoutWidget(show=True, title="Real time data plotting")

    start_x = 0
    start_y = -5
    view_width = 500
    view_height = 1200
    data_plot = win.addPlot()
    data_plot.setRange(QtCore.QRectF(start_x, start_y, view_width, view_height))
    data_line = data_plot.plot(pen='y')

    # Loob taimeri, mis kutusb välja funktsiooni on_update() 10 korda sekundis
    timer = QtCore.QTimer()
    timer.timeout.connect(on_update)
    timer.start(10)
    QtGui.QApplication.instance().exec_()

    np.savetxt(fname = "andemstik",X =listikene)

if __name__ == "__main__":
    main()
