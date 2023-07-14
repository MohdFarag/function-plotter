# pylint: disable=C0103,W0105,E0602
import warnings

import numpy as np
import scipy.special
from math import *

import random
import ast
from .latex import LatexVisitor

# Importing Matplotlib
import matplotlib.pyplot as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasAgg

# Importing PySide2
from PySide2.QtGui import *

# Colors
COLOR1 = "#222831"
COLOR2 = "#393E46"
COLOR3 = "#00ADB5"
COLOR4 = "#EEEEEE"
COLOR5 = "#ffffff"


"""Functions"""

def eval_expression(input_string,x):
     # Step 1
     allowed_names = {
        "x": x,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "sinh": np.sinh,
        "cosh": np.cosh,
        "tanh": np.tanh,
        "e": e,
        "arcsin": np.arcsin,
        "arccos": np.arccos,
        "arctan": np.arctan,
        "arcsinh": np.arcsinh,
        "arccosh": np.arcsinh,
        "arctanh": np.arctanh,
        "log": np.log,
        "fact": scipy.special.factorial,
    }
     # Step 2
     code = compile(input_string, "<string>", "eval")
     # Step 3
     for name in code.co_names:
         if name not in allowed_names:
             # Step 4
             raise NameError(f"Use of {name} not allowed")
     return eval(code, {"__builtins__": {}}, allowed_names)

def functionTranslator(equation: str, min:float, max:float, step:float) -> np.ndarray:   
    # The following operators must be supported: + - / * ^.
    equation = equation.replace("^","**") 

    try:
        eval_expression(f"{equation}",random.random()*100)
    except Exception as e:
        raise Exception("Invalid Equation")
            
    x = np.linspace(min,max,int(1/step)+1)
    y = np.array([])
    with np.errstate(divide='ignore', invalid='ignore'):
        y = eval_expression(f"{equation}*x**0", x)

    return x, y

def py2tex(expr):
    expr = expr.replace('^', '**')
    pt = ast.parse(expr)
    txt = LatexVisitor().visit(pt.body[0].value)
    return txt

def mathTex_to_QPixmap(mathTex, range, fs=16):
    # Python to Latex
    mathTex = py2tex(mathTex)
    
    #---- set up a mpl figure instance ----

    fig = mpl.figure()
    fig.patch.set_facecolor('none')
    fig.set_canvas(FigureCanvasAgg(fig))
    renderer = fig.canvas.get_renderer()

    #---- plot the mathTex expression ----

    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.patch.set_facecolor('none')
    
    if range:
        t = ax.text(0, 0, 'f(x) = '+'$%s$' %mathTex + f' [{range[0]} , {range[1]}]', ha='left', va='bottom', fontsize=fs)
    else:
        t = ax.text(0, 0, '$%s$' %mathTex, ha='left', va='bottom', fontsize=fs)

    #---- fit figure size to text artist ----

    fwidth, fheight = fig.get_size_inches()
    fig_bbox = fig.get_window_extent(renderer)

    text_bbox = t.get_window_extent(renderer)

    tight_fwidth = text_bbox.width * fwidth / fig_bbox.width
    tight_fheight = text_bbox.height * fheight / fig_bbox.height

    fig.set_size_inches(tight_fwidth, tight_fheight)

    #---- convert mpl figure to QPixmap ----

    buf, size = fig.canvas.print_to_buffer()
    qimage = QImage.rgbSwapped(QImage(buf, size[0], size[1],
                                                  QImage.Format_ARGB32))
    qpixmap = QPixmap(qimage)

    return qpixmap
