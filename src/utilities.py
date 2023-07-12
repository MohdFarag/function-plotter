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

def eval_expression(input_string,x):
     # Step 1
     allowed_names = {
        "x": x,
        "sin": sin,
        "cos": cos,
        "tan":tan,
        "sinh": sinh,
        "cosh": cosh,
        "tanh": tanh,
        "e": e,
        "arcsin":asin,
        "arccos":asin,
        "arctan":atan,
        "arcsinh":asinh,
        "arccosh":asinh,
        "arctanh":atanh,
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
    try:
         eval_expression(f"{equation}",0)
    except ZeroDivisionError:
        pass
    except Exception as e:
        raise Exception("Invalid Equation")
            
    equation = equation.replace("^","**") 
    x = np.arange(min,max,step)
    y = []
    try:
        y = eval_expression(f"{equation}*x**0",x)
    except Exception as e:
        x_array = x
        for x in x_array:
            try:
                result = eval_expression(equation,x)
                y.append(result)
            except ZeroDivisionError:
                y.append(0)
        x = x_array
        
    return x, y
