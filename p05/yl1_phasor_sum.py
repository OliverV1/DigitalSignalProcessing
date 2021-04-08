#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPalette
from PyQt5.QtCore import QPointF, Qt
from pyqtgraph.Qt import QtGui, QtCore
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square
from scipy.integrate import quad
from math import*

Phasor = namedtuple('Phasor', 'frequency magnitude phase') # Ühe faasori omadused

class PhasorSumVisualizer(QWidget):

  def __init__(self, parent, CIRCLE_START_X=250, CIRCLE_START_Y=250,ROTATION_OFFSET=0) -> None:
    super().__init__(parent=parent)
    self.G_SCALER = parent.G_SCALER
    self.CIRCLE_START_X = CIRCLE_START_X
    self.CIRCLE_START_Y = CIRCLE_START_Y


    # Need on x,y stardipositsioonid, kuhu hakatakse igal uuendamisel liitma
    #   sageduskomponentide avaldatavat x,y positsioonide nihet.
    self.x_pos = CIRCLE_START_X
    self.y_pos = CIRCLE_START_Y
    self.ROTATION_OFFSET = ROTATION_OFFSET      # Faasinihe kõikidele sageduskomponentidele
    self.phasors = []             # Järjend faasoritest, mille elemendid on kujul namedtuple("frequency", "magnitude")
    self.circles = []             # Järjend faasorite ringidest, mille elemendid on kujul [[x, y], raadius]


  def paint(self, qp):
    """
    See funktsioon joonistab faasorid praegusel ajahetkel.

    Sisendid:
    qp: QPainter objekt, millega saab joonistada

    Vaata https://doc.qt.io/qt-5/qpainter.html#drawEllipse-2
      ja  https://doc.qt.io/qt-5/qpainter.html#drawLine-2
    """
    # Joonista algpunkt

    # Ülesanne 2:
    # Joonista iga faasori ring ja vektor
    # TODO
    qp.setPen(QPen(Qt.red, 1))
    qp.drawEllipse(self.CIRCLE_START_X, self.CIRCLE_START_Y, 3, 3)

    for i in range(0,len(self.circles)):
      qp.setPen(QPen(Qt.white, 1))
      qp.drawEllipse(QPointF(self.circles[i][0][0], self.circles[i][0][1]), self.circles[i][1], self.circles[i][1])
      qp.setPen(QPen(Qt.white, 1))
      try :
        qp.drawLine(int(self.circles[i][0][0]), self.circles[i][0][1], int(self.circles[i+1][0][0]), int(self.circles[i+1][0][1]))
      except :
        qp.drawLine(int(self.circles[i][0][0]), self.circles[i][0][1], int(self.x_pos), int(self.y_pos))

  def calculatePhasors(self, angle):
    """
    See funktsioon arvutab välja faasorite väärtused ajahetkel n ja summeerib nende mõju.

    Sisendid:
    n: ajahetk/nurk radiaanides

    """
    self.x_pos = self.CIRCLE_START_X
    self.y_pos = self.CIRCLE_START_Y
    self.circles.clear()
    for i in range(len(self.phasors)):
      sagedus = self.phasors[i][0]
      amplituud= self.phasors[i][1]
      self.circles.append([[self.x_pos, self.y_pos], amplituud * self.G_SCALER])
      x = amplituud*np.cos(sagedus*angle+self.phasors[i][2]+self.ROTATION_OFFSET)*self.G_SCALER #viimane yl
      y = -amplituud * np.sin(sagedus*angle+self.phasors[i][2]+self.ROTATION_OFFSET)*self.G_SCALER  # kuidas rakendada faasinihet
      self.x_pos += x
      self.y_pos += y






    # Ülesanne 2:


    # Käi läbi iga faasor ja arvuta selle mõju algpositsioonile
    # Salvesta lõplikud koordinaadid väljadesse self.x_pos ja self.y_pos (korruta enne G_SCALER-iga läbi)
    # Salvesta self.circles järjendisse kõikide faasorite keskpunktide koordinaadid ja raadiused

    # TODO


class Main(QWidget):
  WINDOW_WIDTH  = 1080
  WINDOW_HEIGHT = 480
  G_SCALER = 50

  WAVE_MAX_LENGTH = 1000    # Maksimaalne arv lõppsignaali punkte, mida kuvame
  X_POS_INCREMENT = 0.25    # x-telje nihutamise samm
  X_POS_OFFSET = 500     # Lõppsignaali kaugus faasoritest x-teljel

  DELTA_ANGLE = 0.005    # Diskreetimise samm
  nr_of_terms = 3        # Mitu sageduskomponenti välja arvutame
  current_angle = 0      # Praegune ajahetk

  path = []


  def __init__(self) -> None:
    super().__init__()
    self.initUI()
    self.psv = PhasorSumVisualizer(self)


  def initUI(self):
    self.setGeometry(300, 300, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
    self.setWindowTitle('Faasorid')
    pal = self.palette()
    pal.setColor(QPalette.Background, Qt.black)
    self.setAutoFillBackground(True)
    self.setPalette(pal)
    self.show()


  def paintEvent(self, e):
    """
    See funktsioon joonistab faasorid ja nende põhjal arvutatud signaali.
    """
    qp = QPainter()
    qp.begin(self)
    # Joonista faasorid
    self.psv.paint(qp)
    qp.setPen(QPen(Qt.red, 3))
    # Joonista kogu seni arvutatud signaal
    self.drawPath(qp)
    qp.drawLine(int(self.psv.x_pos), int(self.psv.y_pos), self.X_POS_OFFSET,self.psv.y_pos)

    # Joonista joon faasorite summa tipust nihutatud lõppsignaalini
    # TODO

    qp.end()


  def update(self):
    self.psv.phasors.clear()
    self.current_angle += self.DELTA_ANGLE # Liigutame aega edasi

    #self.psv.phasors.append(Phasor(1,1,0))

    # 2. Ülesanne
    # Arvuta nr_of_terms arv faasoreid ja lisa järjendisse self.psv.phasors
    # TODO
    for i in range(1,self.nr_of_terms+1):
      self.psv.phasors.append(square_wave(i))



    # 2. Ülesanne
    # TODO
    self.psv.calculatePhasors(self.current_angle)

    self.add_point([self.X_POS_OFFSET,self.psv.y_pos])

    super().update() # Trigger paintEvent


  def keyPressEvent(self, event):
    key=event.key()
    if key == Qt.Key_Up:
      self.nr_of_terms += 1
    elif key == Qt.Key_Down:
      self.nr_of_terms -= 1
    print(self.nr_of_terms)


  def add_point(self, point):
    """
    See funktsioon lisab antud punkti lõppsignaalile
    """
    qpoint = QPointF(point[0], point[1])
    self.path = [QPointF(point.x() + self.X_POS_INCREMENT, point.y()) for point in self.path]
    self.path.insert(0, qpoint)
    self.path = self.path[:self.WAVE_MAX_LENGTH]


  def drawPath(self, qp):
    """
    See funktsioon joonistab jooned seni arvutatud lõppsignaali punktide vahele
    """
    for i, point in enumerate(self.path):
      if i != len(self.path) - 1:
        qp.drawLine(point, self.path[i+1])


def square_wave(term):
  """
  See funktsioon võtab sisendiks, mitmendat ruutsignaali järku praegu arvutatakse
  ning tagastab sellele järgule vastava faasori.
  https://en.wikipedia.org/wiki/Fourier_series#Convergence
  https://www.mathsisfun.com/calculus/fourier-series.html

  Sisendid:
  term: mitmendat ruutsignaali sinusoidaalset komponenti arvutatakse

  Tagastab:
  phasor: namedtuple, mille sisuks on faasori sagedus ja magnituud
  """

  return Phasor((2*term-1)*np.pi,4/(np.pi*(2*term-1)),0)


def main():
  app = QApplication(sys.argv)
  main = Main()

  timer = QtCore.QTimer()
  timer.timeout.connect(main.update)
  timer.start(20)
  sys.exit(app.exec_())


if __name__=="__main__":
  main()
