from numpy.ma.core import masked_greater
from fourier_gui import *
import numpy as np


class StudentRandomizer():
    def __init__(self, studybook_nr, task_nr = 1) -> None:
        self.seed = int(studybook_nr[1:])*task_nr
        self.random = np.random.RandomState(self.seed)

class Task():
    def __init__(self, x=None, studybook_nr=0, task_nr = 1, subtask=1) -> None:
        if x.any():
            self.x=x
        else:
            self.x = np.arange(0, 2*np.pi, 0.02)
        self.sbnr = studybook_nr
        self.sr = StudentRandomizer(self.sbnr, task_nr)
        self.cg = ComboGraph(self.x)
        for i in range(subtask):
            self.w = BaseSignal(self.cg, self.generate_base_data())
        self.mw = MainWindow()
        self.cs = ComponentSum(self.cg)
        self.mw.add_slider_graph(self.cg)
        self.mw.add_slider_graph(self.w)
        self.mw.add_slider_graph(QHSeperationLine())

        self.ifh = InputFunctionHandler(self.cs)
    def show(self):
        self.mw.show()
    def generate_base_data(self):
        return
    def rint(self, start, stop):
        return self.sr.random.randint(start, stop)

class Task1(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=1, subtask=subtask)
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal f[x]", plot_name=plot_name))

    def generate_base_data(self):
        return self.rint(2, 20)*np.cos(self.x*self.rint(2, 10)*np.pi*2)

class Task2(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=2, subtask=subtask)
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal f[x]", plot_name=plot_name))
    def generate_base_data(self):
        return self.rint(3, 20)*np.cos(self.x*self.rint(1, 15)*np.pi*2 + self.rint(30, 300)) + self.rint(5, 15)

class Task3(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=3, subtask=subtask)
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal f[x]", plot_name=plot_name))
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal g[x]", plot_name=plot_name))
    def generate_base_data(self):
        return self.rint(10, 20)*np.cos(self.x*self.rint(2, 9)*np.pi*2) + \
            self.rint(2, 9)*np.cos(self.x*self.rint(10, 20)*np.pi*2)
class Task4(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=4, subtask=subtask)
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal f[x]", plot_name=plot_name))
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal g[x]", plot_name=plot_name))
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal k[x]", plot_name=plot_name))
    def generate_base_data(self):
        return self.rint(30, 50)*np.cos(self.x*self.rint(2, 9)*np.pi*2 + self.rint(30, 300)) + self.rint(30, 50)
class Task5(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=4, subtask=subtask)
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal f[x]", plot_name=plot_name))
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal g[x]", plot_name=plot_name))
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal k[x]", plot_name=plot_name))
    def generate_base_data(self):
        return self.rint(10, 20)*np.cos(self.x*self.rint(2, 9)*np.pi*2 + self.rint(30, 300)) + \
            self.rint(2, 9)*np.cos(self.x*self.rint(10, 20)*np.pi*2 + self.rint(30, 300)) + \
            self.rint(2, 20)*np.cos(self.x*self.rint(21, 30)*np.pi*2 + self.rint(30, 300)) + self.rint(10, 20)
class Task6(Task):
    def __init__(self, x=None, studybook_nr=0, plot_name=None, subtask=1) -> None:
        super().__init__(x=x, studybook_nr=studybook_nr, task_nr=4, subtask=subtask)
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal f[x]", plot_name=plot_name))
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal g[x]", plot_name=plot_name))
        self.mw.add_slider_graph(Component(self.x, compsum=self.cs, plot_title="Summeeritav signaal k[x]", plot_name=plot_name))
        self.cg.textbox.hide()
        self.cg.mainLayout.itemAt(0).widget().setParent(None) # Delete spacing
        self.cg.mainLayout.addSpacing(20)
        self.dft_plot = pg.PlotWidget(title="Sagedused", row=0, col=0, show=False)
        self.cg.mainLayout.insertWidget(0, self.dft_plot)

    def generate_base_data(self):
        return self.rint(10, 20)*np.cos(self.x*self.rint(2, 9)*np.pi*2 + self.rint(30, 300)) + \
            self.rint(2, 9)*np.cos(self.x*self.rint(10, 20)*np.pi*2 + self.rint(30, 300)) + \
            self.rint(2, 20)*np.cos(self.x*self.rint(10, 20)*np.pi*2 + self.rint(30, 300)) + self.rint(10, 20)
    def show(self):
        self.dft_result = self.ifh.freq_func(self.x, self.w.data)
        self.magnitudes = np.squeeze(self.dft_result[:, [0]])
        self.phases = np.squeeze(self.dft_result[:, [1]]) # Set phase to 0 if magnitude negligible

        x = np.arange(self.magnitudes.size)

        # Create a companion for every y value at y=0
        y0_pairs = np.dstack((np.zeros(self.magnitudes.shape[0]), self.magnitudes)).flatten()
        self.dft_plot.plot(x=np.repeat(x, 2), y=y0_pairs, connect='pairs', pen=pg.mkPen('w', width=3))
        self.dft_plot.plot(self.magnitudes, pen=None, symbol='o',symbolBrush="r")

        for i, phase in np.ndenumerate(self.phases):
            if self.magnitudes[i] > 1:
                text = pg.TextItem()
                text.setText("φ="+str(phase))
                self.dft_plot.addItem(text)
                text.setPos(i[0], self.magnitudes[i])

        super().show()

tasklist = [Task1, Task2, Task3, Task4, Task5, Task6]