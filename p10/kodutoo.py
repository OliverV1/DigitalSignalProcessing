import soundfile as sf
import numpy as np
from vocoder import Vocoder
from scipy import signal
import matplotlib.pyplot as plt
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
input_file="kodutoo.wav"


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
    hop_size = 128
    akna_suurus = 1024
    eelmine = 0
    analüüs=0
    tulemus = []

    viimane = 0
    for i in range(int(len(data) / hop_size)):
        hanning = np.hanning(len(data[analüüs:akna_suurus + analüüs]))
        das = data[analüüs:akna_suurus + analüüs] * hanning
        fft_ = np.fft.fft(das)

        #muu osa

        f_bin=(3*sr)/akna_suurus
        dt = hop_size/sr
        predshift = 2*np.pi*dt*f_bin
        predunwrapped = eelmine+predshift
        faas = np.angle(fft_)
        unwrapped = faas[3]
        r = unwrapped - predunwrapped
        if faas[3]<viimane:
            r = np.pi*2-np.abs(r)





        diff = (r/predshift)*f_bin
        real = f_bin+diff
        tulemus.append(real)


        #tulemus.append(fft_)
        viimane = unwrapped
        eelmine = faas[3]
        analüüs += hop_size




    x = np.arange(start = 0,stop=6,step=(6/2234))
    win = pg.GraphicsLayoutWidget(show=True, title="Plottimine")
    data_plot = win.addPlot()

    data_plot.plot(x=x,y=tulemus)

    QtGui.QApplication.instance().exec_()


if __name__ == "__main__":
    main()