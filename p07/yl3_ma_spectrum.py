#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from yl1_yl2_averages import SMA, ESMA, LWMA, EMA

def plot_stem(plot, y, x=None, **kwargs):
  y = np.array(y)
  if x is None: x = np.arange(y.size)
  y0_pairs = np.dstack((np.zeros(y.shape[0]), y)).flatten()
  plot.plot(x=np.repeat(x, 2), y=y0_pairs, connect='pairs', pen=(255, 0, 0), **kwargs)
  plot.plot(y, pen=None, symbol='o',symbolBrush="r")

def main():

    # Juhuslikud sisendandmed.
    signal_in = np.random.rand(1000)

    # Loome valmis massiivi, kuhu salvestada keskmistamise tulemused.
    MA_result = np.zeros_like(signal_in)

    # Loome kõik liikuva keskmise sooritamise isendi.
    # TODO lisada vajalikud parameetrid vastavalt oma implementatsioonile.
    test_MA = ESMA(10)  # või SMA() LWMA() EMA()

    # Keskmistame oma sisendandmed.
    for index, elem in enumerate(signal_in):
        MA_result[index] = test_MA.average(elem)

    # TODO viige sagedusruumi nii algne kui keskmistatud signaal ja
    # kuvage graafikutel nii kummagi signaali sagedusruumi punktid kui ka nende suhe.

    win = pg.GraphicsLayoutWidget(show=True, title="FFT ja IFFT")
    signal_plot = win.addPlot()
    signal_plot.setTitle("yl3")
    signal_plot.addLegend()
    # signal_plot.plot(signal_in,pen="r",name="esialgne")
    # signal_plot.plot(MA_result,pen="b",name = "keskmistatud")


    signal_plot.plot(np.abs(np.fft.fft(signal_in)),name = "Sagedusruumi esialgne",pen = (255,143,123))
    signal_plot.plot(np.abs(np.fft.fft(MA_result)),name = "sagedusruumi keskmistatud",pen = "g")
    win.nextRow()
    uus = win.addPlot()
    uus.setTitle("yl3")
    uus.addLegend()
    uus.plot(np.abs(np.fft.fft(MA_result)/np.fft.fft(signal_in)),name = " suhe" , pen = "r")


    QtGui.QApplication.instance().exec_()

if __name__ == "__main__":
    main()
