# pylint: disable=C0103,W0105,E0602

import numpy as np
from math import *
import warnings
import random

COLOR1 = "#222831"
COLOR2 = "#393E46"
COLOR3 = "#00ADB5"
COLOR4 = "#EEEEEE"
COLOR5 = "#ffffff"

"""Functions
"""

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
