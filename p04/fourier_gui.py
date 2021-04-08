#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSlider, QFrame, QSizePolicy, QTextEdit, \
    QVBoxLayout, QWidget, QSpacerItem
from pyqtgraph.graphicsItems import PlotItem

g_intro_str = """
Käesolev tarkvara võimaldab lähendada signaale mitme sinusoidi summana.\n
Allpool eraldusjoont on n sinusoidi, mille parameetreid saad muuta kasutades kõrval olevaid liugureid.\n
Sinusoidid liidetakse elementhaaval kokku ja kuvatakse kõige ülemisel graafikul kollase joonena.\n
Eesmärk on komponentide parameetreid sättides panna summeeritud signaal kattuma algsignaaliga.
"""

class QHSeperationLine(QFrame):
  def __init__(self):
    super().__init__()
    self.setMinimumWidth(1)
    self.setFixedHeight(20)
    self.setFrameShape(QFrame.HLine)
    self.setFrameShadow(QFrame.Sunken)
    self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
    return

class Slider(QWidget):
    def __init__(self, minimum, maximum, parent=None, label_text="notext", start_value=0):
        super(Slider, self).__init__(parent=parent)
        self.verticalLayout = QHBoxLayout(self)
        self.label = QLabel(self)
        self.label_text = label_text
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()

        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.slider.setValue(start_value)
        self.horizontalLayout.addWidget(self.slider)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.resize(self.sizeHint())

        self.slider.valueChanged.connect(self.setLabelValue)
        self.x = None
        self.setLabelValue(self.slider.value())

    def setLabelValue(self, value):
        self.x = value
        self.label.setText(self.label_text + ": {0:.4g}".format(self.x))

class SliderGraph(QWidget):
    def __init__(self, x_values, parent=None, plot_title = "No name plot", plot_name = None):
        super(SliderGraph, self).__init__(parent=parent)
        self.mainLayout = QHBoxLayout(self)
        self.sliderLayout = QVBoxLayout(self)
        self.magnitudeLabel = QLabel()
        self.magnitudeLabel.setText("Magnitude:")
        self.sliders = []
        self.x = x_values

        self.mainLayout.addLayout(self.sliderLayout)
        self.mainLayout.addWidget(self.magnitudeLabel)
        self.win = pg.GraphicsLayoutWidget(title=plot_title)
        self.mainLayout.addWidget(self.win)
        self.plot = self.win.addPlot(name=plot_name,title=plot_title, row=0, col=1)
        self.plot.setYRange(-30, 30)
        self.plot.addLegend()
        self.curve = self.plot.plot(name=plot_name,pen='y')
        self.init_sliders()
        self.update_plot()

    def init_sliders(self):
        return

    def add_slider(self, start, stop, func, label_text="notext", start_value=0):
        w1 = Slider(start, stop, label_text=label_text, start_value=start_value)
        w1.slider.valueChanged.connect(func)
        self.sliders.append(w1)
        self.sliderLayout.addWidget(w1)

    def update_plot(self):
        return

class BaseSignal(QWidget):
    def __init__(self, combo_graph, data, parent=None):
        self.combo_graph = combo_graph
        self.data=data
        super().__init__(parent=parent)
        self.update_plot()

    def update_plot(self):
        self.combo_graph.update_original_plot(self.data)

class ComponentSum(QWidget):
    def __init__(self, combo_graph, parent=None):
        self.components = []
        self.combo_graph = combo_graph
        self.sum_func = lambda signals: signals[0] # Vaikimisi võtab lihtsalt esimese massiivi

    def add_component(self, component):
        self.components.append(component)

    def update_plot(self):
        if len(self.components):
            data = self.sum_func([comp.data for comp in self.components])
            self.combo_graph.update_sum_plot(data)

class Component(SliderGraph):
    def __init__(self, x_values, parent=None, compsum=None, plot_title = "No name plot", plot_name=None, hide_sliders=[]):
        self.frequency = 1
        self.scaler = 1
        self.phase = 0
        self.shift = 0
        self.f_x = lambda a,b,c,d,e : a
        self.f_compare = lambda a,b : 0
        if compsum:
            self.compsum = compsum
            self.compsum.components.append(self)
        super().__init__(x_values, parent=parent, plot_title=plot_title, plot_name=plot_name)
        self.hide_sliders(hide_sliders)

    def update_plot(self):
        self.frequency = self.sliders[0].x
        self.scaler = self.sliders[1].x
        self.phase = self.sliders[2].x*np.pi/180
        self.shift = self.sliders[3].x
        self.data = self.f_x(self.x, self.frequency, self.scaler, self.phase, self.shift)
        self.curve.setData(self.data)
        if self.compsum:
            self.compsum.update_plot()
            self.magnitudeLabel.setText("Skalaarkorrutis: " + str(int(self.f_compare(self.data, self.compsum.combo_graph.orig_data))))

    def init_sliders(self):
        self.add_slider(0, self.x.shape[0], self.update_plot, label_text="Sagedus [k]")
        self.add_slider(0, 20, self.update_plot, label_text="Amplituud [a]", start_value=1)
        self.add_slider(0, 360, self.update_plot, label_text="Faasinihe [φ]")
        self.add_slider(0, 20, self.update_plot, label_text="Vertikaalnihe [b]")

    def hide_slider(self, index):
        self.sliders[index].hide()

    def hide_sliders(self, indexes):
        for i in indexes:
            self.hide_slider(i)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.mainLayout = QVBoxLayout(self)

    def add_slider_graph(self, slider_graph):
        self.mainLayout.addWidget(slider_graph)

class ComboGraph(QWidget):
    def __init__(self, x, parent=None):
        super(ComboGraph, self).__init__(parent=parent)
        self.mainLayout = QHBoxLayout(self)
        self.sliders = []
        self.x = x

        self.textbox = QTextEdit()
        self.textbox.setReadOnly(True)
        self.textbox.setFont(QFont("Arial", 12))

        self.textbox.setText(g_intro_str)
        self.mainLayout.addWidget(self.textbox)
        self.mainLayout.addSpacing(60)

        self.combo_plot = pg.PlotWidget(title="Algsignaal ja summeeritud signaal")
        self.combo_plot.addLegend(offset=(20,0))
        self.plot_original = self.combo_plot.plot(name="Algsignaal", pen='c')
        self.plot_sum = self.combo_plot.plot(name="Summeeritud signaal", pen='y')
        self.combo_plot.plot()
        self.mainLayout.addWidget(self.combo_plot)
        self.orig_data = None

    def add_slider_graph(self, slider_graph):
        self.mainLayout.addWidget(slider_graph)

    def update_original_plot(self, new_data):
        self.plot_original.setData(new_data)
        self.orig_data = new_data

    def update_sum_plot(self, new_data):
        self.plot_sum.setData(new_data)

class InputFunctionHandler():
    def __init__(self, compsum) -> None:
        self.compsum = compsum
        self.freq_func = lambda x, y: 0

    def set_component_function(self, func):
        for comp in self.compsum.components:
            comp.f_x = func
            comp.update_plot()
        self.compsum.update_plot()

    def set_compare_function(self, func):
        for comp in self.compsum.components:
            comp.f_compare = func
            comp.update_plot()
        self.compsum.update_plot()

    def set_sum_function(self, sum_func):
        self.compsum.sum_func = sum_func

    def set_frequency_finder(self, freq_func):
        self.freq_func=freq_func

if __name__ == '__main__':
    app = QApplication(sys.argv)

    x = np.arange(0, 4*np.pi, 0.02)
    mw = MainWindow()
    cg = ComboGraph(x)
    w = BaseSignal(cg, 5*np.cos(x*2))
    cs = ComponentSum(cg)
    mw.add_slider_graph(cg)
    mw.add_slider_graph(w)
    mw.add_slider_graph(QHSeperationLine())

    ifh = InputFunctionHandler(cs)
    ifh.set_compare_function(lambda a,b: np.sum(a*b))
    ifh.set_component_function(lambda a,b,c,d,e: c*np.sum(b*a+d) + e)

    plot_name = "a*cos(k*x + rad(alpha))+b"
    mw.add_slider_graph(Component(x, compsum=cs, plot_title="Summeeritav signaal f[x]", plot_name=plot_name))
    mw.add_slider_graph(Component(x, compsum=cs, plot_title="Summeeritav signaal g[x]", plot_name=plot_name))
    mw.add_slider_graph(Component(x, compsum=cs, plot_title="Summeeritav signaal k[x]", plot_name=plot_name))

    mw.show()
    sys.exit(app.exec_())
