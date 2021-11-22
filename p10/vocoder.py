#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

class Vocoder:
    def __init__(self, win_size, analysis_hop_size, stretch=1.0):
        self.output = None
        self.win_size = win_size
        self.analysis_hop_size = analysis_hop_size
        self.analysis_idx = 0
        self.synthesis_hop_size = int(analysis_hop_size * stretch)
        self.synthesis_idx = 0
        self.stretch = stretch

    def analysis(self, data):
        # TODO tagasta akendatud lõigust võetud FFT
        hanning = np.hanning(len(data[self.analysis_idx:self.win_size+self.analysis_idx]))
        das = data[self.analysis_idx:self.win_size+self.analysis_idx]*hanning
        fft_ = np.fft.fft(das)
        return fft_

    def synthesis(self, processed_fft):
        tulemus = np.fft.ifft(processed_fft).real
        tulemus = tulemus * np.hanning(len(tulemus))
        #self.output[self.analysis_idx:self.win_size+self.analysis_idx] += tulemus.real
        try:
            self.output[self.synthesis_idx:self.win_size + self.synthesis_idx] += tulemus.real
        except:
            pass
    def processing(self, signal_fft, yl):
        if yl == 1:
            return self.sanity_check(signal_fft)
        elif yl == 2.1:
            return self.robotize(signal_fft)
        elif yl == 2.2:
            return self.whisperize(signal_fft)
        elif yl == 3:
            return self.noise_cancellation(signal_fft)
        elif yl == 4:
            return self.time_stretch(signal_fft)
        else:
            return signal_fft

    def sanity_check(self, fft_):
        # TODO Eralda signaalis magnituud ja faas

        magnitude = np.abs(fft_)
        faas = np.angle(fft_)
        # Signaali töötlemine toimub siin vahel

        # TODO Vii magnituud ja faas tagasi kompleksarvuks
        nullid = np.zeros_like(fft_)
        for i in range(len(magnitude)):
            nullid[i]=complex(magnitude[i] * np.cos(faas[i]), magnitude[i] * np.sin(faas[i]))
        fft_=nullid

        return fft_

    def robotize(self, fft_):
        magnitude = np.abs(fft_)
        faas = np.angle(fft_)*0

        nullid = np.zeros_like(fft_)
        for i in range(len(magnitude)):
            nullid[i] = complex(magnitude[i] * np.cos(faas[i]), magnitude[i] * np.sin(faas[i]))
        fft_ = nullid

        return fft_

    def whisperize(self, fft_):
        # TODO Eralda signaalis magnituud ja faas
        magnitude = np.abs(fft_)
        nullid = np.zeros_like(fft_)
        faas = np.angle(fft_)

        suurus = int(np.size(fft_)/2)
        esimene_pool = np.pi*np.random.uniform(-1,1,(1,suurus))
        teine_pool= np.flip(esimene_pool)*-1

        faas = np.append(esimene_pool,teine_pool)
        faas = np.insert(faas,0,faas[0])
        # TODO täida faasiinfo suvaliste väärtustega õiges vahemikus
        # TODO Vii magnituud ja faas tagasi kompleksarvuks
        for i in range(len(magnitude)):
            nullid[i]=complex(magnitude[i] * np.cos(faas[i]), magnitude[i] * np.sin(faas[i]))
        fft_=nullid
        return fft_

    def noise_cancellation(self, fft_):
        magnitude = np.abs(fft_)
        print(np.amax(magnitude))
        faas = np.angle(fft_)
        pos_arv=0.00001
        magnitude= (magnitude/(magnitude+pos_arv))*magnitude

        nullid = np.zeros_like(fft_)
        for i in range(len(magnitude)):
            nullid[i] = complex(magnitude[i] * np.cos(faas[i]), magnitude[i] * np.sin(faas[i]))
        fft_ = nullid
        return fft_

    def time_stretch(self, fft_):
        return fft_

    def run(self, data, yl):
        #self.output = np.zeros_like(data)
        self.output = np.zeros_like(data)*self.stretch
        for i in range(int(len(data)/self.analysis_hop_size)):
            analüüs = self.analysis(data)
            protsessimine = self.processing(analüüs,yl)
            self.synthesis(protsessimine)
            self.analysis_idx+=self.analysis_hop_size
            self.synthesis_idx += self.synthesis_hop_size # süntees

        