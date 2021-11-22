#!/usr/bin/python3
# -*- coding: utf-8 -*-

import soundfile as sf
import numpy as np
from vocoder import Vocoder
from scipy import signal
import matplotlib.pyplot as plt

input_file = "noisy_talk.wav"
output_file = "tulemus.wav"

yl = 3

win_size = 1024
hop_size = 128
stretch = 1

def display_spectrogram(data, sr, nperseg, noverlap, compare=np.zeros(10000)):
    f, (ax, ax2) = plt.subplots(2,figsize=(12, 5))
    plt.subplots_adjust(hspace=0.3)
    freqs, times, Sx = signal.spectrogram(
        data,
        fs=sr,
        window="hanning",
        nperseg=nperseg,
        noverlap=noverlap,
        detrend=False,
        scaling="spectrum",
    )
    # Logaritmi ei saa nullist võtta
    Sx[Sx == 0] = 1e-8
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    # Ülesanne 0
    ax.set_ylim(0, 20000) # TODO muuda vastavalt ülesandele
    # TODO kasuta logaritmilist esitust magnituudidel (Sx)
    ax.pcolormesh(times, freqs, np.log(Sx), cmap="viridis", shading="auto")

    # Ülesanne 1
    # TODO tee samad muudatused, mis üleval
    freqs, times, Sx = signal.spectrogram(
        compare,
        fs=sr,
        window="hanning",
        nperseg=nperseg,
        noverlap=noverlap,
        detrend=False,
        scaling="spectrum",
    )
    # Logaritmi ei saa nullist võtta
    Sx[Sx == 0] = 1e-8
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Frequency (Hz)")
    ax2.set_ylim(0, 20000)
    ax2.pcolormesh(times, freqs, np.log(Sx), cmap="viridis", shading="auto")


    plt.show()

def read_audio():
    # TODO loe sisse audiofail, kasutades sf.read funktsiooni
    data, sr = sf.read(input_file)
    tulemus = []
    try:
        for i in data:
            tulemus.append(np.sum(i)/len(data[0]))
        data = np.array(tulemus)
    except:
        data=data

    data = data/np.amax(np.abs(data))
    return data, sr


def main():
    data, sr = read_audio()

    vocoder = Vocoder(win_size, hop_size)
    vocoder.run(data, yl)
    # TODO Normaliseeri vocoder.output (yl 1)
    normalisseri = np.array(vocoder.output)/np.amax(np.abs(np.array(vocoder.output)))
    # TODO kirjuta väljund faili, kasutades sf.write (yl 1)
    sf.write(output_file, normalisseri, sr)
    # TODO kuva spektrogramm (yl 0)
    display_spectrogram(data,sr,win_size,hop_size,normalisseri)

if __name__ == "__main__":
    main()