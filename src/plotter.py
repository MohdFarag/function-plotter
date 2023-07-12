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
    
    def __init__(self, parent=None, title="Plotter"):
        self.X = []        
        self.Y = []
        
        self.fig = Figure(facecolor=f"{COLOR1}")

        self.axes = self.fig.add_subplot(111)
        self.axes.set_title(title, fontweight ="bold", color=f"{COLOR4}")
        
        self.axes.set_xlabel("x", color=f"{COLOR4}")
        self.axes.set_ylabel("f(x)", color=f"{COLOR4}")
        
        self.axes.set_facecolor(f"{COLOR1}")
        
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['bottom'].set_color(f"{COLOR4}")
        self.axes.spines['left'].set_color(f"{COLOR4}")

        self.axes.tick_params(axis='x', colors=f"{COLOR4}")
        self.axes.tick_params(axis='y', colors=f"{COLOR4}")
        
        super(MplCanvas, self).__init__(self.fig)

    def plotAllData2(self):
        self.clearSignal()
        for x, y in zip(self.X, self.Y):
            self.axes.plot(x, y)
        self.draw()
        
    def plotAllData(self, x, y):
        self.clearSignal()
        self.X.append(x)
        self.Y.append(y)
        for x, y in zip(self.X, self.Y):
            self.axes.plot(x, y)

        self.draw()
       
    def plotOneData(self, x, y):
        self.clearSignal()
        self.axes.plot(x, y)
        self.draw()

    def clearSignal(self):
        self.axes.clear()