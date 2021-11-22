import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore




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

def main():
    my_file = open("hw2_electricity_price.txt", "r")
    content = my_file.read()  # loeme sisse
    content_list = content.split("\n")  # delimiter
    content_list.pop(-1)  # viimane element oleks "" seda pole vaja
    my_file.close()  # peame sulgema muidu see oleks ebalahe

    vahe_list = []  # loll viis teha stringist float
    for i in content_list:
        vahe_list.append(float(i))

    signal_in = []
    for i in range(0,len(vahe_list),24):
        if i == 0:
            signal_in.append(sum(vahe_list[0:24])/24)
        else:
            signal_in.append(sum(vahe_list[i:24+i]) / 24)



    LWMA_result = np.zeros_like(signal_in)
    test_LWMA = LWMA(100000)  # 24h ööpäevas

    # Keskmistame oma andmed kasutades kõiki implementeeritud keskmise leidmise meetodeid
    for index, elem in enumerate(signal_in):
        LWMA_result[index] = test_LWMA.average(elem)

    # Tulemuste kuvamine graafikul
    win = pg.GraphicsLayoutWidget(show=True, title="Moving average demo")
    data_plot = win.addPlot()
    data_plot.addLegend(brush=0.0)
    data_plot.plot(LWMA_result, name="LWMA", pen=pg.mkPen('b'))
    QtGui.QApplication.instance().exec_()


if __name__ == "__main__":
    main()
