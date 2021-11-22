#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore


######### Ülesandes 1 implementeeritavad funktsioonid #########

def plot_filter_time(plot_item, data):
    # Funktsioon peab ette antud graafiku objektile kuvama filtri kerneli.
    # Samuti peab funktsioon nimetama ja skaleerima teljed.
    return plot_item.plot(data)


def plot_filter_freq(plot_item, data, dB_scale = False):
    # Funktsioon peab ette antud graafiku objektile kuvama ette antud filtri võimenduse sagedusruumis.
    # Samuti peab funktsioon nimetama ja skaleerima teljed.
    # Kui nõutakse väärtusi detsibellides, tuleb sisend kõigepealt teisendada ja seejärel kuvada.
    if dB_scale == True:
        return plot_item.plot(np.log(np.abs(data))*10,x=np.linspace(0,0.5,num=len(data)))
    else:
        return plot_item.plot(np.abs(data),x=np.linspace(0,0.5,num=len(data)))

def create_blackmann_window(window_size):
    # Funktsioon peab looma soovitud suurusega Blackmann akna
    # vastavalt valemile ja tagastama selle numpy massiivina.
    N = window_size
    if not N % 2: N += 1  # Make sure that N is odd.
    n = np.arange(N)

    w = 0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + \
        0.08 * np.cos(4 * np.pi * n / (N - 1))

    return w



def create_lowpass(cutoff_freq, transition_bw):#https://tomroelandts.com/articles/how-to-create-a-simple-low-pass-filter
    # Funktsioon peab tekitama sinc-kerneli, mis vastab argumendina saadud tingimustele.
    # Kernel tuleb tagastada numpy massiivina.
    fc = cutoff_freq  # Cutoff frequency as a fraction of the sampling rate (in (0, 0.5)).
    b = transition_bw  # Transition band, as a fraction of the sampling rate (in (0, 0.5)).
    N = int(np.ceil((4 / b)))
    if not N % 2: N += 1  # Make sure that N is odd.
    n = np.arange(N)

    # Compute sinc filter.
    h = np.sinc(2 * fc * (n - (N - 1) / 2))

    # Normalize to get unity gain.
    h = h / np.sum(h)

    return h

def filter_in_frequecy(time_kernel):
    # Funktsioon peab tagastama filtri võimenduse (komponentide magnituudid) sagedusruumis ilma aliasteta.
    # Võimendus tuleb tagastada reaalarvulise numpy massiivina.

    return np.fft.rfft(time_kernel)


######### Ülesandes 3 implementeeritavad funktsioonid #########

def create_highpass_spectral_inversion(cutoff_freq, transition_bw):
    # Kasutades abifunktsioonina madalpääsfiltri loomist, peab see funktsioon looma
    # kõrgpääsfiltri spektri inverteerimise meetodil.
    madalpääs = create_lowpass(cutoff_freq,transition_bw)
    tulemus = np.multiply(madalpääs, create_blackmann_window(len(madalpääs)))
    olemas = tulemus / np.sum(tulemus)


    tulemus  = []
    for i in olemas:
        tulemus.append(i*-1)
    muutuja = int(len(olemas) / 2)
    tulemus[muutuja]=tulemus[muutuja]+1
    return tulemus

def create_highpass_spectral_reversal(cutoff_freq, transition_bw):
    # Kasutades abifunktsioonina madalpääsfiltri loomist, peab see funktsioon looma
    # kõrgpääsfiltri spektri nihutamise meetodil.
    madalpääs = create_lowpass(cutoff_freq, transition_bw)
    tulemus = np.multiply(madalpääs, create_blackmann_window(len(madalpääs)))
    olemas = tulemus / np.sum(tulemus)
    tulemus = []
    for i in range(len(olemas)):
        tulemus.append(olemas[i]*((-1)**i))

    return tulemus


######### Ülesandes 5 implementeeritavad funktsioonid #########

def create_bandpass(low_cutoff_freq, high_cutoff_freq, transition_bw):
    # Funktsioon peab looma sobivad madal- ja kõrgpääsfiltrid ja kombineerima need üheks ribapääsfiltriks.
    high = create_highpass_spectral_inversion(low_cutoff_freq,transition_bw)

    madalpääs = create_lowpass(high_cutoff_freq, transition_bw)
    tulemus = np.multiply(madalpääs, create_blackmann_window(len(madalpääs)))

    low = tulemus / np.sum(tulemus)



    return np.convolve(high,low)

######### Ülesandes 7 implementeeritavad funktsioonid #########

def create_bandstop(low_cutoff_freq, high_cutoff_freq, transition_bw):
    high = create_highpass_spectral_inversion(high_cutoff_freq,transition_bw)

    madalpääs = create_lowpass(low_cutoff_freq, transition_bw)
    tulemus = np.multiply(madalpääs, create_blackmann_window(len(madalpääs)))

    low = tulemus / np.sum(tulemus)



    return high+low

def main():
    # Siin saab oma üksikuid funktsioone katsetada.
    # Ülesannete lahendused tuleks luua eraldi selleks ettenähtud failidesse.
    pass

if __name__ == '__main__':
    main()
