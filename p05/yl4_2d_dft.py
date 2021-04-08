#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QPalette
from PyQt5.QtCore import QPointF, Qt
from pyqtgraph.Qt import QtCore
from collections import namedtuple
from yl1_phasor_sum import PhasorSumVisualizer
from yl3_dft_algorithm import dft_trig
from sample_signals import signal1, signal2, signal3, signal4

faasorite_formaat = namedtuple('Phasor', 'frequency magnitude phase')

class Main(QWidget):
  WINDOW_WIDTH  = 1080
  WINDOW_HEIGHT = 600
  G_SCALER = 1

  WAVE_MAX_LENGTH = 1000    # Maksimaalne arv lõppsignaali punkte, mida kuvame
  X_POS_INCREMENT = 0    # x-telje nihutamise samm

  DELTA_ANGLE = 0.005    # Diskreetimise samm
  nr_of_terms = 1        # Mitu sageduskomponenti välja arvutame
  current_angle = 0      # Praegune ajahetk
  ROTATION_OFFSET = 0
  path = []


  def add_point(self, point):
    qpoint = QPointF(point[0], point[1])
    self.path = [QPointF(point.x() + self.X_POS_INCREMENT, point.y()) for point in self.path]
    self.path.insert(0, qpoint)
    self.path = self.path[:self.WAVE_MAX_LENGTH]


  def drawPath(self, qp):
    for i, point in enumerate(self.path):
      if i != len(self.path) - 1:
        qp.drawLine(point, self.path[i+1])


  def initUI(self):
    self.setGeometry(300, 300, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
    self.setWindowTitle('Faasorid')
    # set black background
    pal = self.palette()
    pal.setColor(QPalette.Background, Qt.black)
    self.setAutoFillBackground(True)
    self.setPalette(pal)
    self.show()


  def __init__(self, signal1, signal2) -> None:
    super().__init__()

    # Arvuta sisendsignaalidest signal1 ja signal2 DFT
    self.fourier_x = dft_trig(signal1)
    self.fourier_y = dft_trig(signal2)

    self.fourier_x = sorted(self.fourier_x, key=lambda x: x.magnituud, reverse=True)
    self.fourier_y = sorted(self.fourier_y, key=lambda x: x.magnituud, reverse=True)
    self.DELTA_ANGLE = 2 * np.pi / 100
    self.x_psv = PhasorSumVisualizer(self,CIRCLE_START_X=540, CIRCLE_START_Y=100)
    self.y_psv = PhasorSumVisualizer(self,CIRCLE_START_X=150, CIRCLE_START_Y=360, ROTATION_OFFSET=-np.pi/2)

    #faasorite_formaat = tes

    for i in range(len(self.fourier_x)):
      self.x_psv.phasors.append(faasorite_formaat(frequency= self.fourier_x[i].sagedus,magnitude=self.fourier_x[i].magnituud,phase=self.fourier_x[i].faas))
      self.y_psv.phasors.append(faasorite_formaat(frequency= self.fourier_y[i].sagedus,magnitude=self.fourier_y[i].magnituud,phase=self.fourier_y[i].faas))
    self.initUI()


  def paintEvent(self, e):
    qp = QPainter()
    qp.begin(self)
    self.x_psv.paint(qp) # Joonista x-telje faasorite summa
    self.y_psv.paint(qp) # Joonista y-telje faasorite summa
    qp.setPen(QPen(Qt.red, 3))
    self.drawPath(qp)
    # Joonista jooned faasorite summa tippudest lõppsignaalini
    # TODO
    qp.drawLine(int(self.x_psv.x_pos), int(self.x_psv.y_pos),int(self.x_psv.x_pos),int(self.y_psv.y_pos))
    qp.drawLine(int(self.y_psv.x_pos), int(self.y_psv.y_pos), int(self.x_psv.x_pos),int(self.y_psv.y_pos))
    qp.end()


  def update(self):
    self.x_psv.calculatePhasors(self.current_angle)
    self.y_psv.calculatePhasors(self.current_angle)
    self.add_point((self.x_psv.x_pos,self.y_psv.y_pos))
    self.current_angle += (2*np.pi)/len(self.fourier_x)
    super().update() # Trigger paintEvent


def create_circular_signal(scaler=50):
    x = np.arange(0,2*np.pi,(2*np.pi)/100)
    y = np.arange(0,2*np.pi,(2*np.pi)/100)
    return scaler*x,scaler*y


def main():
  app = QApplication(sys.argv)
  test_signal1, test_signal2 = create_circular_signal()
  main = Main(signal1, signal2)

  timer = QtCore.QTimer()
  timer.timeout.connect(main.update)
  timer.start(5)
  sys.exit(app.exec_())


if __name__=="__main__":
  main()

