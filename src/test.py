import numpy as np
import matplotlib.pyplot as plt
from math import *
import pytest
from .utilities import functionTranslator

class TestClass:
    min_val, max_val, step = -20, 20, 0.001
    x = np.arange(min_val, max_val, step)
    def test_first_arg(self):
        Fx = "x"
        tested_x = functionTranslator(Fx,self.min_val, self.max_val, self.step)[0]
        assert  tested_x == pytest.approx(self.x)

    def test(self):
        Fx = "5 + 10"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx((5+10) * self.x**0)
        
    def test_x(self):
        Fx = "x"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(self.x)

    def test_1DivideX(self):
        Fx = "1/x"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(1/self.x)

    def test_xPlus5(self):
        Fx = "x+5"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(self.x+5)

    def test_xPlus5MinusX2(self):
        Fx = "x+5-x^2"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(self.x+5-self.x**2)
        
    def test_2x(self):
        Fx = "2*x"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(2*self.x)

    def test_10x(self):
        Fx = "10*x"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(10*self.x)
        
    def test_x2(self):
        Fx = "x^2"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(self.x**2)

    def test_5x6(self):
        Fx = "5*x^6"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(5*self.x**6)

    def test_sinX_DivideX(self):
        Fx = "sin(x)/(5*x)"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(np.sin(self.x)/(5*self.x))
    
    def test_5cosX2(self):
        Fx = "5*cos(x^2)"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(5*np.cos(self.x**2))

    def test_5tanX(self):
        Fx = "5*tan(x)"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(5*np.tan(self.x))
        
    def test_ePowX(self):
        Fx = "e^x"
        tested_y = functionTranslator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(e**self.x)
