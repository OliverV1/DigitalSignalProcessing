#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from scipy import fft
from collections import namedtuple
from sample_signals import signal1, signal2


# Kasutage seda funktsiooni DFT tulemuse kujutamiseks
def plot_stem(plot, y, x=None, **kwargs):
  y = np.array(y)
  if x is None: x = np.arange(y.size)
  y0_pairs = np.dstack((np.zeros(y.shape[0]), y)).flatten()
  plot.plot(x=np.repeat(x, 2), y=y0_pairs, connect='pairs', pen=(255, 0, 0), **kwargs)
  plot.plot(y, pen=None, symbol='o',symbolBrush="r")



def dft_trig(input_signal):
  """
  See funktsioon võtab sisendiks ajadomeenis oleva reaalarvuliste väärtustega signaali
  ning rakendab sellel kompleksarvulist diskreetse Fourier' pöörde
  trigonomeetrilist vormi.

  Sisendid:
  input_signal: reaalarvuline signaal ajadomeenis

  Tagastab:
  output: namedtuple sageduskomponentidest
  """

  punktide_arv = len(input_signal)

  tulemus = []
  Faasor=namedtuple("faasor","sagedus real imaginaar magnituud faas")
  for k in range(punktide_arv):
    summa1 =0
    summa2=0
    for n in range(punktide_arv):
      summa1 += input_signal[n]*(np.cos((2*np.pi*k*n)/punktide_arv))
      summa2 += -1*input_signal[n]*(np.sin((2*np.pi*k*n)/punktide_arv))
    summa1 = summa1/punktide_arv
    summa2 = summa2 / punktide_arv
    tulemus.append(Faasor(sagedus=k,real=summa1,imaginaar=summa2,magnituud=np.sqrt(summa1**2 + summa2**2),faas=np.arctan2(summa2,summa1)))

  return tulemus


def idft_trig(input_signal):
  pikkus = len(input_signal)
  tulemus = []
  for k in range(pikkus):

    summa_realosa_cos = 0
    summa_realosa_sin = 0

    summa_imaginaar_cos = 0
    summa_imaginaar_sin = 0

    for n in range(pikkus):
      summa_realosa_cos += input_signal[n][1] * (np.cos((2 * np.pi * k * n) / pikkus))  #realosa input_signal[n][1] faasor(sagedus=0, real=-53.9679180887372, imaginaar=0.0, suur=53.9679180887372, faas=-0.0
      summa_realosa_sin += input_signal[n][1] * (np.sin((2 * np.pi * k * n) / pikkus))
    esimene_osa = summa_realosa_sin+summa_realosa_cos

    for n in range(pikkus):
      summa_imaginaar_cos += input_signal[n][2] * (np.cos((2 * np.pi * k * n) / pikkus))
      summa_imaginaar_sin += input_signal[n][2] * (np.sin((2 * np.pi * k * n) / pikkus))
    teine_osa = summa_imaginaar_sin-summa_imaginaar_cos

    tulemus.append(esimene_osa-teine_osa)

  return tulemus


def main():
  win = pg.GraphicsLayoutWidget(show=True, title="Praktikumi yl3")
  win.resize(1000, 600)
  p = win.addPlot()
  p.addLegend()
  p.plot(y = signal1, pen=(255, 0, 0))
  p.showGrid(x=True, y=True)
  p.setLabel('bottom', 'Aeg')
  p.setLabel('left', 'Väärtus(y) ')

  win.nextRow()
  p2 = win.addPlot(title="Diskreetne fourie pööre - numpy fft")
  p2.addLegend()
  numpy_fft_tulemus = np.fft.fft(signal1)
  magnituud = np.abs(numpy_fft_tulemus) / np.size(numpy_fft_tulemus)
  plot_stem(p2, magnituud)

  win.nextRow()
  p3 = win.addPlot(title="Minu tehtud ")
  p3.addLegend()
  dft_list_kokku = dft_trig(signal1)
  plottimiseks= []
  for i in range(len(signal1)):
    plottimiseks.append(dft_list_kokku[i].magnituud)
  plot_stem(p3, plottimiseks)

  win.nextRow()
  p4 = win.addPlot(title="idft minu")
  p4.addLegend()
  p4.plot(y=idft_trig(dft_list_kokku), pen=(255, 0, 0))


  win.nextRow()
  p5 = win.addPlot(title="idft originaal")
  p5.addLegend()
  p5.plot(y = signal1, pen=(255, 0, 0))




  QtGui.QApplication.instance().exec_()

if __name__ == "__main__":
  main()
