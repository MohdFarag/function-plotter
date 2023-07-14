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
import matplotlib.colors as mcolors
mplColorsList = list(mcolors.CSS4_COLORS)

from .utilities import *


class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, title="Plotter"):
        # Variables
        self.title = title
        self.lines = []
        self.X = []        
        self.Y = []
        self.labels = []
        self.colors = []
        
        self.fig = Figure(facecolor=f"{COLOR1}")
        self.axes = self.fig.add_subplot(111)
        
        self.clearPlot()
        
        super(MplCanvas, self).__init__(self.fig)

    def plotAllData2(self):
        self.clearPlot()
        
        i = 0
        for x, y in zip(self.X, self.Y):
            if self.colors[i] == "":
                self.axes.plot(x, y, color='w', label=self.labels[i])
            else:
                self.axes.plot(x, y, color=self.colors[i], label=self.labels[i])
            i += 1
                        
        self.draw()
        
    def plotAllData(self, x, y, label, color="red"):
        self.clearPlot()
        
        self.X.append(x)
        self.Y.append(y)
        self.labels.append(label)
        self.colors.append(mplColorsList[len(self.X)-1])
        
        i = 0
        for x, y in zip(self.X, self.Y):
            if self.colors[i] == "":
                self.axes.plot(x, y, color='w', label=self.labels[i])
            else:
                self.axes.plot(x, y, color=self.colors[i], label=self.labels[i])
            i += 1
            
        self.draw()
       
    def plotOneData(self, x, y, label):
        self.clearPlot()
        self.axes.plot(x, y, label=label)
        self.setxLimits(x)
        self.draw()

    def setxLimits(self, x):
        minX = np.min(x)
        maxX = np.max(x)
        if minX >= 0: minX*0.9
        else: minX*1.1
        
        if maxX >= 0: maxX*1.1 
        else: maxX*0.9
        
        self.axes.set_xlim([minX, maxX])
       
    def clearPlot(self):
        self.axes.clear()
        self.axes.set_title(self.title, fontweight ="bold", color=f"{COLOR4}")
        
        self.axes.axhline(0, color='grey', linestyle='--', linewidth=0.75, alpha=0.75)
        self.axes.axvline(0, color='grey', linestyle='--', linewidth=0.75, alpha=0.75)
        self.axes.grid(True,which='both', color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
        
        self.axes.set_xlabel("x", color=f"{COLOR4}", fontweight ="bold")
        self.axes.set_ylabel("f (x)", color=f"{COLOR4}", fontweight ="bold")
        
        self.axes.set_facecolor(f"{COLOR1}")
        
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['bottom'].set_color(f"{COLOR4}")
        self.axes.spines['left'].set_color(f"{COLOR4}")

        self.axes.tick_params(axis='x', colors=f"{COLOR4}")
        self.axes.tick_params(axis='y', colors=f"{COLOR4}")