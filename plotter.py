# importing numpy
import numpy as np

# matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.colors as mcolors
mplColorsList = list(mcolors.CSS4_COLORS)

from utilities import *

class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, title="Plotter"):
        # Variables
        self.title = title
        self.lines = []
        self.x_arrays = []        
        self.y_arrays = []
        self.labels = []
        self.colors = []
        
        self.fig = Figure(facecolor="#222831")
        self.axes = self.fig.add_subplot(111)
        
        self.clear_plot()
        
        super(MplCanvas, self).__init__(self.fig)

    def plot_all_data2(self):
        self.clear_plot()
        
        i = 0
        for x, y in zip(self.x_arrays, self.y_arrays):
            if self.colors[i] == "":
                self.axes.plot(x, y, color='w', label=self.labels[i])
            else:
                self.axes.plot(x, y, color=self.colors[i], label=self.labels[i])
            i += 1
                        
        self.draw()
        
    def plot_all_data(self, x, y, label, color="red"):
        self.clear_plot()
        
        self.x_arrays.append(x)
        self.y_arrays.append(y)
        self.labels.append(label)
        self.colors.append(mplColorsList[len(self.x_arrays)-1])
        
        i = 0
        for x, y in zip(self.x_arrays, self.y_arrays):
            if self.colors[i] == "":
                self.axes.plot(x, y, color='w', label=self.labels[i])
            else:
                self.axes.plot(x, y, color=self.colors[i], label=self.labels[i])
            i += 1
            
        self.draw()
       
    def plot_data(self, x, y, label):
        self.clear_plot()
        self.axes.plot(x, y, label=label)
        self.set_x_limits(x)
        self.draw()

    def set_x_limits(self, x):
        min_x = np.min(x)
        max_x = np.max(x)
        if min_x >= 0: min_x*0.9
        else: min_x*1.1
        
        if max_x >= 0: max_x*1.1 
        else: max_x*0.9
        
        self.axes.set_xlim([min_x, max_x])
       
    def clear_plot(self):
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