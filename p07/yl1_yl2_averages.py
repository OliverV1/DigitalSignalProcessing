#!/usr/bin/python3
# -*- coding: utf-8 -*-
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
class LWMA:
    def __init__(self,window_size):  # Konstruktorisse tuleb ise lisada vajalikud argumendid.
        # TODO
        self.window_size = window_size
        self.data = []

    # Funktsioon, mis teostab kaalutud liikuva keskmise operatsiooni.
    def average(self, data_in):
        # Muutke järgnevat rida, teostades korrektne arvutus.
        # TODO
        self.data.append(data_in)
        summa = 0
        lugeja = 0
        if len(self.data) > self.window_size:
            for i in range(0,self.window_size,1):
                summa +=i+1
                lugeja += (i+1)*self.data[i]
            data_out = lugeja/summa
            self.data.pop(0)
        else:
            for i in range(0,len(self.data),1):
                summa +=i+1
                lugeja += (i+1)*self.data[i]
            data_out = lugeja/summa
        return data_out

# Ülesanne 2.3:

# Exponential moving average - eksponentsiaalselt kahanevate kaaludega liikuv keskmine
class EMA:
    def __init__(self,alpha):  # Konstruktorisse tuleb ise lisada vajalikud argumendid.
        self.alpha = alpha
        self.data = []
        self.eelmineväärtus = 0

    # Funktsioon, mis teostab kaalutud liikuva keskmise operatsiooni.
    def average(self, data_in):
        # Muutke järgnevat rida, teostades korrektne arvutus.
        # TODO

        self.data.append(data_in)

        if len(self.data)==1:
            data_out = data_in
            self.eelmineväärtus = data_out
        if len(self.data)>1:
            data_out = data_in * self.alpha + (1-self.alpha) * self.eelmineväärtus
            self.eelmineväärtus = data_out
        return data_out


def main():

    # Juhuslik andmestik, mille peal testida liikuvate keskmiste toimimist.
    signal_in = np.random.rand(250)

    # Loome valmis massiivid, kuhu salvestada keskmistamise tulemused.
    SMA_result = np.zeros_like(signal_in)
    ESMA_result = np.zeros_like(signal_in)
    LWMA_result = np.zeros_like(signal_in)
    EMA_result = np.zeros_like(signal_in)

    # Loome kõik liikuva keskmise sooritamise isendid.
    # TODO oma implementatsiooni katsetamisel tuleb lisada konstruktoritele kõik vajalikud parameetrid.
    test_SMA = SMA(10)
    test_ESMA = ESMA(10)
    test_LWMA = LWMA(10)
    test_EMA = EMA(0.6)

    # Keskmistame oma andmed kasutades kõiki implementeeritud keskmise leidmise meetodeid
    for index, elem in enumerate(signal_in):
        SMA_result[index] = test_SMA.average(elem)
        ESMA_result[index] = test_ESMA.average(elem)
        LWMA_result[index] = test_LWMA.average(elem)
        EMA_result[index] = test_EMA.average(elem)

    # Tulemuste kuvamine graafikul
    win = pg.GraphicsLayoutWidget(show=True, title="Moving average demo")

    data_plot = win.addPlot()
    data_plot.addLegend(brush=0.0)

    data_plot.plot(SMA_result, name="SMA", pen=pg.mkPen('r', width=1.2))
    data_plot.plot(ESMA_result, name="ESMA", pen=pg.mkPen('g', style=QtCore.Qt.DotLine))
    data_plot.plot(LWMA_result, name="LWMA", pen=pg.mkPen('b'))
    data_plot.plot(EMA_result, name="EMA", pen=pg.mkPen('y'))
    data_plot.plot(signal_in, name="Original", pen=pg.mkPen('w'))
    QtGui.QApplication.instance().exec_()


if __name__ == "__main__":
    main()
