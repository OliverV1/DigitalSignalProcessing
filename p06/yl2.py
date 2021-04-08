#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cmath

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

from sample_signal import test_signal
#https://inst.eecs.berkeley.edu/~ee123/sp16/Sections/FFT_Demo.html
N = len(test_signal)


def plot_stem(plot, y, x=None, **kwargs):
  y = np.array(y)
  if x is None: x = np.arange(y.size)
  y0_pairs = np.dstack((np.zeros(y.shape[0]), y)).flatten()
  plot.plot(x=np.repeat(x, 2), y=y0_pairs, connect='pairs', pen=(255, 0, 0), **kwargs)
  plot.plot(y, pen=None, symbol='o',symbolBrush="r")


def myfft(x):
    """A recursive implementation of the 1D Cooley-Tukey FFT"""
    N = len(x)

    if N <= 2:  # this cutoff should be optimized
        return fft(x)
    else:
        X_even = myfft(x[::2])
        X_odd = myfft(x[1::2])
        n_idx = np.arange(N)
        factor = W_N(N, n_idx, 1)
        return np.concatenate([X_even + factor[:N // 2] * X_odd,

                               X_even + factor[N // 2:] * X_odd])
def W_N(N,k,n):
    return np.exp(-1j * 2 * np.pi * k * n / N)

def fft(x):
    """Returns the 1D DFT of x using matrix-vector multiplication"""
    N = len(x)
    n_idx = np.arange(N)
    k_idx = n_idx[:, None]
    return np.dot(W_N(N,k_idx,n_idx), x)

def ifft(x):
    return np.real(np.conjugate(fft(np.conjugate(x)))/len(x))


def exponent_to_algebraic(c):
    """
    Funktsioon, mis võtab sisendiks kompleksarvu eksponentkujul
    ning tagastab sama arvu algebralisel kujul.

    Sisend: tuple kujul (kompleksarvu magnituud, kompleksarvu faas)

    Väljund: complex tüüpi arv
    """
    return complex(c[0]*np.cos(c[1]),c[0]*np.sin(c[1]))
def main():


    win = pg.GraphicsLayoutWidget(show=True, title="FFT ja IFFT")
    signal_plot = win.addPlot()
    signal_plot.setTitle("Esialgne signaal")
    plot_stem(signal_plot, test_signal)

    win.nextRow()
    p1 = win.addPlot(title="Implementeeritud FFT ")
    p1.addLegend()
    X = myfft(test_signal)
    magnituud = np.abs(X)
    plot_stem(p1, magnituud)

    win.nextRow()
    p2 = win.addPlot(title="Implementeeritud FFT  Faas")
    p2.addLegend()
    X = myfft(test_signal)
    muutuja = 0
    testimiseks = []
    for i in X:
        if muutuja%2 == 1:
            testimiseks.append(np.angle(i))
        else:
            testimiseks.append(0)
        muutuja+=1
    plot_stem(p2, testimiseks)

    win.nextRow()
    p3 = win.addPlot(title="Numpy FFT")
    p3.addLegend()
    fft_main = np.fft.fft(test_signal)
    plot_stem(p3, np.abs(fft_main))

    win.nextRow()
    p4 = win.addPlot(title="Implementeeritud IFFT")
    p4.addLegend()
    plot_stem(p4,ifft(fft_main))

    QtGui.QApplication.instance().exec_()

if __name__ == "__main__":
    main()
