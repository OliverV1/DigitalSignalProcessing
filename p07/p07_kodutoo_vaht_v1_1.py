#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

# Ülesanne 1:

# Standard moving average - Standardne, võrdsete kaaludega liikuv keskmine
class SMA:

    # Klassi konstruktor.
    # Keskmistamise isendi loomisel tuleks konstruktorile anda kõik selle muudetavad parameetrid.
    # Tavalise liikuva keskmise puhul on selleks akna suurus.
    def __init__(self, window_size):
        self.window_size = window_size  # Kasutame argumendina saadud suurust, et väärtustada vastav isendiväli.
        # Siin tuleks algväärtustada ka kõik ülejäänud vajalikud isendiväljad. Antud juhul on vaja andmestruktuuri kuhu koguda eelmiseid andmeid.
        self.sissetulev = []
        self.asukoht = 0


    # Funktsioon, mis teostab keskmistamise operatsiooni vastavalt keskmistamise valemile naiivsel kujul.

    def average(self, data_in):
        # Muutke järgnevat rida, teostades korrektne arvutus.
        # TODO
        data_out = 0
        self.sissetulev.append(data_in)
        self.asukoht +=1

        if self.asukoht >self.window_size:
            self.sissetulev.pop(0)

        data_out = sum(self.sissetulev) / len(self.sissetulev)
        return data_out

# Ülesanne 2.1:

# Efficient standard moving average - efektiivne versioon tavalisest ühtlaste kaaludega liikuvast keskmisest
class ESMA:
    def __init__(self,window_size):  # Konstruktorisse tuleb ise lisada vajalikud argumendid.
        self.window_size = window_size
        self.list = []

    # Funktsioon, mis teostab keskmistamise operatsiooni tõhusamalt, arvutamata kogu akna summat uuesti elementhaaval.
    def average(self, data_in):
        # Muutke järgnevat rida, teostades korrektne arvutus.

        self.list.append(data_in)

        if len(self.list) > self.window_size:
            self.data_out = ((self.list[self.window_size]-self.list[0])/self.window_size)+self.data_out
            self.list.pop(0)
        else:
            self.data_out = sum(self.list)/len(self.list)

        return self.data_out

# Ülesanne 2.2:

# Weighted moving average - lineaarselt muutuvate kaaludega liikuv keskmine.

def main():
    tulemuse_SMA=[]
    tulemuse_ESMA = []

    for i in range(100,60000,1000):

        # Juhuslik andmestik, mille peal testida liikuvate keskmiste toimimist.
        signal_in = np.random.rand(i)

        # Loome valmis massiivid, kuhu salvestada keskmistamise tulemused.
        SMA_result = np.zeros_like(signal_in)
        ESMA_result = np.zeros_like(signal_in)


        # Loome kõik liikuva keskmise sooritamise isendid.
        # TODO oma implementatsiooni katsetamisel tuleb lisada konstruktoritele kõik vajalikud parameetrid.
        test_SMA = SMA(10)
        test_ESMA = ESMA(10)


        # Keskmistame oma andmed kasutades kõiki implementeeritud keskmise leidmise meetodeid
        a = time.time()
        for index, elem in enumerate(signal_in):
            SMA_result[index] = test_SMA.average(elem)
        b = time.time()
        tulemuse_SMA.append(b-a)
        for index, elem in enumerate(signal_in):
            ESMA_result[index] = test_ESMA.average(elem)
        c = time.time()
        tulemuse_ESMA.append(c-b)



    # Tulemuste kuvamine graafikul
    win = pg.GraphicsLayoutWidget(show=True, title="Moving average demo")

    data_plot = win.addPlot()
    data_plot.addLegend(brush=0.0)

    data_plot.plot(tulemuse_SMA,x=np.arange(100,60000,1000), name="SMA", pen="r")
    data_plot.plot(tulemuse_ESMA,x=np.arange(100,60000,1000), name="ESMA",pen="y")
    QtGui.QApplication.instance().exec_()


if __name__ == "__main__":
    main()
