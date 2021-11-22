#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
from scipy.io.wavfile import read, write
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from filters import create_highpass_spectral_reversal, create_highpass_spectral_inversion
from filters import filter_in_frequecy, plot_filter_freq, plot_filter_time,create_lowpass,create_bandstop,create_bandpass

def overlap_add(s1, s2):

    convolve_segment_length = 2**(int(np.log2(len(s1)))+2)

    result = np.zeros(len(s1) + len(s2) - 1)

    s2_segment_length = convolve_segment_length - len(s1) + 1

    s1 = np.pad(s1,(0,convolve_segment_length-len(s1)))

    signaal1 = np.fft.fft(s1)




      # Kui pikk on kahe signaali konvolutsioon?


    for i in range(0, len(s2), s2_segment_length):

        #s2_segment = np.zeros(convolve_segment_length)
        s2_segment = s2[i:i+s2_segment_length]
        s2_segment = np.pad(s2_segment,(0,convolve_segment_length-len(s2_segment)))

        # Signaal2 sagedusruumi
        signaal2 = np.fft.fft(s2_segment)



        convolve_segment =np.real(np.fft.ifft(np.multiply(signaal1,signaal2)))

        if len(convolve_segment)< len(result[i:]):
            result[i:i + convolve_segment_length] += convolve_segment[0:convolve_segment_length]
        else:
            result[i:i + convolve_segment_length] += convolve_segment[0:len(result) - i]


    return result

def plot_stem(plot, y, x=None, **kwargs):
  y = np.array(y)
  if x is None: x = np.arange(y.size)
  y0_pairs = np.dstack((np.zeros(y.shape[0]), y)).flatten()
  plot.plot(x=np.repeat(x, 2), y=y0_pairs, connect='pairs', pen=(255, 0, 0), **kwargs)
  plot.plot(y, pen=None, symbol='o',symbolBrush="r")


def main():


    win = pg.GraphicsLayoutWidget(show=True, title="Filtrid")
    # Siin failis tuleks luua sobiv kõrgpääsfilter helifaili `yl4_in.wav` filtreerimiseks
    # ja seda seejärel helifailil rakendada ning filtreeritud fail peale normaliseerimist salvestada.
    kitarr = read("kodu1_in.wav")
    kitarr = np.array(kitarr[1], dtype=np.float32)

    #ribafilter = create_bandstop(0.006,0.007390,0.001)
    ribafilter = create_bandstop(0.0589569, 0.13605, 0.001)
    ribafilter2 = create_bandstop(0.317460, 0.340136, 0.001)
    ribafilter = np.convolve(ribafilter2,ribafilter)
    print(len(kitarr))
    array = np.arange(0,44100, 44100/len(kitarr))

    sagedus_graafik = win.addPlot()
    sagedus_graafik.addLegend()
    fft = np.fft.fft(kitarr)
    sagedus_graafik.plot(y=(np.abs(fft) / len(fft)), x=array, pen="r")

    win.nextRow()
    filter = win.addPlot()
    filter.addLegend()
    riba = filter_in_frequecy(ribafilter)
    plot_filter_freq(filter, riba)

    tulemus = overlap_add(kitarr,ribafilter)
    win.nextRow()
    p2 = win.addPlot()
    sageduseks = filter_in_frequecy(tulemus)
    p2.plot(np.abs(sageduseks),x=array[0:112251])



    tulemus = tulemus.astype(np.float32)

    write('kodu_filtreeritud.wav', 44100, tulemus)
    QtGui.QApplication.instance().exec_()
if __name__ == "__main__":
    main()
