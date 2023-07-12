# importing Qt widgets
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

# importing numpy
import numpy as np

# matplotlib
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from .utilities import *

class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None,title="Plotter"):
        
        self.y = [0]
        self.x = np.linspace(-np.pi/2, np.pi/2, 1000)
        
        self.fig = Figure(facecolor=f"{COLOR1}")

        self.axes = self.fig.add_subplot(111)
        self.axes.set_title(title, fontweight ="bold", color=f"{COLOR4}")
        
        self.axes.set_xlabel("Time", color=f"{COLOR4}")
        self.axes.set_ylabel("Amplitude", color=f"{COLOR4}")
        
        self.axes.set_facecolor(f"{COLOR1}")
        
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['bottom'].set_color(f"{COLOR4}")
        self.axes.spines['left'].set_color(f"{COLOR4}")

        self.axes.tick_params(axis='x', colors=f"{COLOR4}")
        self.axes.tick_params(axis='y', colors=f"{COLOR4}")
        
        super(MplCanvas, self).__init__(self.fig)


    def set_data(self, x, y):
        self.x = x
        self.y = y

    def plotSignal(self):
        self.clearSignal()
        self.axes.plot(self.x, self.y)
        self.draw()

    def clearSignal(self):
        self.axes.clear()
        self.axes.set_xlim([min(self.x), max(self.x)])
        self.axes.set_ylim([min(self.y), max(self.y)+1])