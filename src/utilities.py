# pylint: disable=C0103,W0105,E0602

import numpy as np
from math import *

COLOR1 = "#222831"
COLOR2 = "#393E46"
COLOR3 = "#00ADB5"
COLOR4 = "#EEEEEE"
COLOR5 = "#ffffff"

"""Functions
"""

def functionTranslator(equation: str, min:float, max:float) -> np.ndarray:
    try:
        eval(equation, None, {'x': 0})
    except Exception as e:
        raise e
    
    # The following operators must be supported: + - / * ^.
    equation = equation.replace("^","**") 
    x_axis = np.arange(min,max,0.01)
    y_axis = list()
    for x in x_axis:
        result = eval(equation, None, {'x': x})
        y_axis.append(result)

    return x_axis, y_axis