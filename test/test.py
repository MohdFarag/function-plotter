import numpy as np
import matplotlib.pyplot as plt
from math import *

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


try:
    eq = "e**x"    
    min,max=-10,50
    x,y = functionTranslator(eq,min,max)
    plt.plot(x,y)
    plt.show()
except Exception as e:
    print(e)    
