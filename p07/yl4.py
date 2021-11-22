#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import serial

data_line = None
data_line2= None
listikene=[]
i=0
data = []
listikene2 = []

eelmineväärtus = 0
def on_update():
    global data_line
    global data_line2
    global i
    # Implementeerige siia Arduinost andmete küsimise ja kuvamise loogika
    ser = serial.Serial('/dev/ttyUSB0')
    ser_bytes = ser.readline()
    originaal = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))

    decoded_bytes = int(average(int(originaal)))

    if (len(listikene)<500):
        listikene.append(decoded_bytes)

    else:
        listikene.pop(0)
        listikene.append(decoded_bytes)

    if (len(listikene2)<500):
        listikene2.append(originaal)

    else:
        listikene2.pop(0)
        listikene2.append(originaal)

    data_line2.setData(listikene2)

    data_line.setData(listikene)

def average(data_in):
    global eelmineväärtus
    alpha = 0.1
    data.append(data_in)
    if len(data)==1:
        data_out = data_in
        eelmineväärtus = data_out
    if len(data)>1:
        data_out = data_in * alpha + (1-alpha) * eelmineväärtus
        eelmineväärtus = data_out

    return data_out

def main():
    global data_line
    global data_line2
    win = pg.GraphicsLayoutWidget(show=True, title="Real time data plotting")

    start_x = 0
    start_y = -5
    view_width = 500
    view_height = 1200
    data_plot = win.addPlot()
    data_plot.setRange(QtCore.QRectF(start_x, start_y, view_width, view_height))
    data_line = data_plot.plot(pen='y')
    data_line2 = data_plot.plot(pen="r")

    # Loob taimeri, mis kutusb välja funktsiooni on_update() 10 korda sekundis
    timer = QtCore.QTimer()
    timer.timeout.connect(on_update)
    timer.start(10)
    QtGui.QApplication.instance().exec_()


if __name__ == "__main__":
    main()
