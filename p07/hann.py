#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pyvisa
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtCore import QTimer,QDateTime
global waveform_datapoints 
listikene = []
#hello

def decode_waveform_preamble(waveform_preamble: str) -> dict:
    """
    Query and return all the waveform parameters.

    Args:
        waveform_preamble (str): string that contains the 10 waveform parameters separated by ","

    Returns:
        A dictionary that contains the following:
            int:   wav_format where 0 (BYTE), 1 (WORD) or 2 (ASC)
            int:   wav_type where 0 (NORMal), 1 (MAXimum) or 2 (RAW).
            int:   wav_points is an integer between 1 and 24000000 denoting the number of points you can read with a data request
            int:   wav_count is the number of averages in the average sample mode and 1 in other modes.
            float: x_increment is the time difference between two neighboring points in the X direction in seconds.
            float  x_origin is the start time of the waveform data in the X direction.
            int:   x_reference is the reference time of the data point in the X direction.
            float: y_increment is the waveform increment in the Y direction.
            int:   y_origin is the vertical offset relative to the "Vertical Reference Position" in the Y direction.
            int:   y_reference is the vertical reference position in the Y direction.
    """
    waveform_preamble = waveform_preamble.split(",")
    assert len(waveform_preamble) == 10
  

    wav_format, wav_type, wav_points, wav_count, x_reference, y_origin, y_reference = (
        int(val) for val in waveform_preamble[:4] + waveform_preamble[6:7] + waveform_preamble[8:10]
    )
    x_increment, x_origin, y_increment = (
        float(val) for val in waveform_preamble[4:6] + waveform_preamble[7:8]
    )
    return {
        "format": wav_format,
        "type": wav_type,
        "nr_of_points": wav_points,
        "nr_of_avg": wav_count,
        "x_increment": x_increment,
        "x_origin": x_origin,
        "x_reference": x_reference,
        "y_increment": y_increment,
        "y_origin": y_origin,
        "y_reference": y_reference,
    }

def update():
    global waveform_datapoints
    global waveform_dict
    global inst
    global data_line
    global data_line2
    global p2
    global p3
    global p4

    inst.write('WAV:SOUR CHAN2') # Valime kanali andmepunktide salvestamiseks.
    inst.write(':WAV:MODE NORM') # Loeme ainult andmed, mis on ekraanil (Ekraanile mahub 1200 punkti)
    inst.write(':WAV:FORM BYTE') # Ühe sisendsignaali punkt on mahub ühte baiti kuna DS1054Z on 8-bitine ostsilloskoop.
    inst.write(':WAV:START 1')   # Salvestatud signaali esimene punkt, mida lugeda.
    inst.write(':WAV:STOP 1200') # Salvestatud signaali viimane punkt, mida lugeda.

    
   
    waveform_datapoints = inst.query_binary_values(':WAV:DATA?', datatype="B", container=np.array).astype(np.float32)
    waveform_dict = decode_waveform_preamble(inst.query(":WAVEFORM:PREAMBLE?"))
    y = ((waveform_datapoints-waveform_dict["y_origin"]-waveform_dict["y_reference"])*waveform_dict["y_increment"])
    x = np.arange(start = waveform_dict["x_origin"],step=waveform_dict["x_increment"],stop = waveform_dict["x_origin"]+(waveform_dict["x_increment"]*waveform_dict["nr_of_points"]))
    
    
    data_line.setData(x,y)

    p3.clear()
    plot_stem(p3,np.abs(np.fft.fft(y)))
    
    

    M= len(y)
    n = np.arange(1-M, M, 2)
    muutuja=0.5 + 0.5*np.cos(np.pi*n/(M-1))
    
    y=np.array(y)*muutuja

    data_line2.setData(x,y)

    p4.clear()
    plot_stem(p4,np.abs(np.fft.fft(y)))


    


    

    
    

def plot_stem(plot, y, x=None, **kwargs): # Pltoime stemidena, olemas varasemast koodist
  y = np.array(y)
  if x is None: x = np.arange(y.size)
  y0_pairs = np.dstack((np.zeros(y.shape[0]), y)).flatten()
  plot.plot(x=np.repeat(x, 2), y=y0_pairs, connect='pairs', pen=(255, 0, 0), **kwargs)
  plot.plot(y, pen=None, symbol='o',symbolBrush="r")
    
def main():
    global waveform_datapoints
    global waveform_dict
    global inst
    global data_line
    global data_line2
    global p2
    global p3
    global p4
    #rm = pyvisa.ResourceManager()
    #inst = rm.open_resource('TCPIP::TYTI-136-DS1054::INSTR', read_termination="\n", write_termination="\n")
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('TCPIP::TYTI-136-DS1054::INSTR', read_termination="\n", write_termination="\n")
    win = pg.GraphicsLayoutWidget(show=True, title="Ostsilloskoobi andmed")

    
   
    #win = pg.GraphicsLayoutWidget(show=True, title="Ostsilloskoobi andmed")
   
 
    p1 = win.addPlot()  #filtreerimata kuvamine
    data_line = p1.plot(pen='y')
    
    data_line2 = p1.plot(pen='r') #filtreeritud kuvamine filtreerimata peale
    

    p3= win.addPlot()

    p4= win.addPlot()

    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(200)

    QtGui.QApplication.instance().exec_()

    inst.close()

   

if __name__ == "__main__":
  main()

