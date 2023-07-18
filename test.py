# Math imports
import numpy as np
from math import *

import pytest
import pytestqt

from utilities import function_translator
from mainWindow import MainWindow

# Importing Qt widgets
from PySide2 import QtCore
from PySide2.QtWidgets import *

class TestClass:
    min_val, max_val, step = -20, 20, 0.001
    x = np.linspace(min_val,max_val,int(1/step)+1)
    def test_first_arg(self):
        Fx = "x"
        tested_x = function_translator(Fx,self.min_val, self.max_val, self.step)[0]
        assert  tested_x == pytest.approx(self.x)

    def test(self):
        Fx = "5 + 10"
        tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx((5+10) * self.x**0)
        
    def test_x(self):
        Fx = "x"
        tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(self.x)

    def test_1DivideX(self):
        Fx = "1/x"
        tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(1/self.x)

    def test_xPlus5(self):
        Fx = "x+5"
        tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(self.x+5)

    def test_xPlus5MinusX2(self):
        Fx = "x+5-x^2"
        tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(self.x+5-self.x**2)
        
    def test_2x(self):
        Fx = "2*x"
        tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(2*self.x)

    def test_10x(self):
        Fx = "10*x"
        tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(10*self.x)
        
    def test_x2(self):
        Fx = "x^2"
        tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(self.x**2)

    def test_5x6(self):
        Fx = "5*x^6"
        tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(5*self.x**6)
   
    def test_5cosX2(self):
        Fx = "5*cos(x^2)"
        tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(5*np.cos(self.x**2))

    def test_5tanX(self):
        Fx = "5*tan(x)"
        tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(5*np.tan(self.x))
        
    def test_ePowX(self):
        Fx = "e^x"
        tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]
        assert tested_y == pytest.approx(e**self.x)

    # Test for Exceptions and Warnings
    def test_wrongEquation(self):
        with pytest.raises(Exception) as e_info:
            Fx = "1/x*"
            tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]        
    
    def test_wrongEquation2(self):
        with pytest.raises(Exception) as e_info:
            Fx = "(1/(x))/(x)+(x^(2*x+x)))"
            tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]        
    
    def test_wrongEquation3(self):
        with pytest.raises(Exception) as e_info:
            Fx = "X"
            tested_y = function_translator(Fx,self.min_val, self.max_val, self.step)[1]        

# Test for QT
@pytest.fixture
def app(qtbot):
    test_app = MainWindow()
    qtbot.addWidget(test_app)
    return test_app

def check_inputs_at_start(app):
    assert app.equation_field.text() == ''
    assert app.min_field.text() == ''
    assert app.max_field.text() == ''

def test_enter_valid_input(app, qtbot):
    '''
    test to ensure basic find files functionality is working. 
    '''
    qtbot.keyClicks(app.equation_field, 'x')
    qtbot.keyClicks(app.min_field, '-5')
    qtbot.keyClicks(app.max_field, '5')

    assert app.equation_field.text() == 'x'
    assert app.min_field.text() == '-5'
    assert app.max_field.text() == '5'

    qtbot.mouseClick(app.add_equation_button, QtCore.Qt.LeftButton)
        
    assert app.equation_field.text() == ''
    assert app.min_field.text() == ''
    assert app.max_field.text() == ''
    
def test_enter_invalid_input(app, qtbot):
    '''
    test to ensure basic find files functionality is working. 
    '''
    qtbot.keyClicks(app.equation_field, 'x*')
    qtbot.keyClicks(app.min_field, '-5')
    qtbot.keyClicks(app.max_field, '5')
    assert app.add_equation_button.isEnabled() is False

def test_enter_invalid_input2(app, qtbot):
    '''
    test to ensure basic find files functionality is working. 
    '''
    qtbot.keyClicks(app.equation_field, 'x^2')
    qtbot.keyClicks(app.min_field, '-5')
    qtbot.keyClicks(app.max_field, '')
    assert app.add_equation_button.isEnabled() == False

def test_enter_invalid_input3(app, qtbot):
    '''
    test to ensure basic find files functionality is working. 
    '''
    qtbot.keyClicks(app.equation_field, 'x')
    qtbot.keyClicks(app.min_field, '')
    qtbot.keyClicks(app.max_field, '5')
    assert app.add_equation_button.isEnabled() == False

def test_enter_invalid_input4(app, qtbot):
    '''
    test to ensure basic find files functionality is working. 
    '''
    qtbot.keyClicks(app.equation_field, 'x')
    qtbot.keyClicks(app.min_field, '5')
    qtbot.keyClicks(app.max_field, '5')
    assert app.add_equation_button.isEnabled() == False
