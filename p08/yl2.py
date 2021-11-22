#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
from scipy.io.wavfile import read, write
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from filters import create_lowpass
from filters import filter_in_frequecy, plot_filter_freq, plot_filter_time

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



def main():
    # Siin failis tuleks luua sobiv filter ostsilloskoobiga salvestatud helifaili filtreerimiseks
    # ja seda seejärel helifailil rakendada ning filtreeritud fail peale normaliseerimist salvestada.
    kitarr = read("yl2.wav")
    kitarr = np.array(kitarr[1], dtype=np.float32)

    example_lowpass = create_lowpass(0.04, 0.03)
    note = np.convolve(example_lowpass,kitarr)

    note = note.astype(np.float32)
    write('yl2_out_time.wav', 100000, note)  # sample rate 1000000000

    note = overlap_add(kitarr, example_lowpass)
    note = note.astype(np.float32)
    write('yl2_out_freq.wav', 100000, note)  # sample rate 1000000000

if __name__ == "__main__":
    main()