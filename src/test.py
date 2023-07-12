import numpy as np
import matplotlib.pyplot as plt
from math import *
import pytest
from .utilities import functionTranslator

class TestClass:
    min_val, max_val, step = -20, 20, 0.001
    def test_first_arg(self):
        Fx = "x"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_x = functionTranslator(Fx,self.min_val, self.max_val, self.step)[0]
        assert  tested_x == pytest.approx(x)

    def test(self):
        Fx = "5 + 10"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx((5+10) * x**0)
        
    def test_x(self):
        Fx = "x"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(x)

    def test_1DivideX(self):
        Fx = "1/x"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(1/x)

    def test_xPlus5(self):
        Fx = "x+5"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(x+5)

    def test_xPlus5MinusX2(self):
        Fx = "x+5-x^2"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(x+5-x**2)
        
    def test_2x(self):
        Fx = "2*x"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(2*x)

    def test_10x(self):
        Fx = "10*x"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(10*x)
        
    def test_x2(self):
        Fx = "x^2"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(x**2)

    def test_5x6(self):
        Fx = "5*x^6"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(5*x**6)

    def test_sinX_DivideX(self):
        Fx = "sin(x)/(5*x)"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(np.sin(x)/(5*x))
    
    def test_5cosX2(self):
        Fx = "5*cos(x^2)"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(5*np.cos(x**2))

    def test_5tanX(self):
        Fx = "5*tan(x)"
        x = np.arange(self.min_val, self.max_val, self.step)
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(5*np.tan(x))