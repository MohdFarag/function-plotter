# Math
import numpy as np

# Importing sys package
import sys

# Import Classes
from .utilities import *
from .QtUtilities import *

# Importing Qt widgets
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import pyqtgraph as pg

# Matplotlib
from .plotter import *

# Importing Logging
from .log import appLogger

# Global Variables
STEP = 0.001

# Window class
class MainWindow(QMainWindow):
    """Main Window"""
    def __init__(self, *args, **kwargs):
        """Initializer."""
        super(MainWindow, self).__init__(*args, **kwargs)
        QFontDatabase.addApplicationFont("./src/assets/fonts/AccanthisADFStd-Regular.otf")
        QFontDatabase.addApplicationFont("./src/assets/fonts/OpenSans.ttf")
        QFontDatabase.addApplicationFont("./src/assets/fonts/Enagol-Math-Medium.ttf")

        ### Setting title
        self.setWindowTitle("Function Plotter")

        ### Setting Icon
        self.setWindowIcon(QIcon("./src/assets/icons/function.png"))
        self.setMinimumSize(1000,600)

        ### UI contents
        self._createActions()
        self._createMenuBar()
        self._createStatusBar()

        # Central area
        self._initUI()

        # Connect signals
        self._connect()
   
    ##########################################
    ##########################################

    # Actions
    def _createActions(self):
        # Actions
        self.fileActions()
        
        self.helpActions()
        self.setShortcuts()

    # File Actions
    def fileActions(self):
        # Open Action
        self.openAction = QAction(QIcon(":Open"), "&Open", self)
        # Set Open function to the triggered signal
        self.openAction.triggered.connect(self.openFunction)
        self.openAction.setStatusTip('Open file')
        
        # Exit Action
        self.exitAction = QAction(QIcon(":exit"), "&Exit", self)
        # Set exit function to the triggered signal
        self.exitAction.triggered.connect(self.exit)
        self.exitAction.setStatusTip('Exit application')

    # Help Actions
    def helpActions(self):
        self.helpContentAction = QAction("&Help Content", self)
        self.helpContentAction.setStatusTip('Help')
        
        self.checkUpdatesAction = QAction("&Check For Updates", self)
        self.checkUpdatesAction.setStatusTip('Check Updates')
        
        self.aboutAction = QAction("&About", self)
        self.aboutAction.setStatusTip('About')

    # Shortcuts
    def setShortcuts(self):
        pass
    
    ##########################################
    
    # Add separator
    def addSeparator(self, parent):
        # Creating a separator action
        self.separator = QAction(self)
        self.separator.setSeparator(True)
        parent.addAction(self.separator)

    # Menu
    def _createMenuBar(self):
        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)
        # Menu bar
        menuBar = self.menuBar()
        
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.exitAction)

        """Help"""
        helpMenu = QMenu("&Help", self)
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addSeparator()
        helpMenu.addAction(self.checkUpdatesAction)
        helpMenu.addSeparator()
        helpMenu.addAction(self.aboutAction)

        menuBar.addMenu(fileMenu)
        menuBar.addMenu(helpMenu)
        
    # Context Menu Event
    def contextMenuEvent(self, event):
        # Creating a menu object with the central widget as parent
        menu = QMenu(self)
        # Populating the menu with actions
        menu.addAction(self.openAction)
        self.addSeparator(menu)
        menu.addAction(self.helpContentAction)
        menu.addAction(self.checkUpdatesAction)
        menu.addAction(self.aboutAction)
        self.addSeparator(menu)
        menu.addAction(self.exitAction)
        # Launching the menu
        menu.exec_(event.globalPos())
    
    ##########################################

    # GUI
    def _initUI(self):
        centralMainWindow = QWidget(self)
        self.setCentralWidget(centralMainWindow)

        # Outer Layout
        outerLayout = QHBoxLayout()
        
        self.graph = MplCanvas(None, "Plotter")
        
        # Left layout
        leftLayout = QVBoxLayout()
        leftWidget = QWidget()
        leftWidget.setLayout(leftLayout)
        
        equationsLayout = QVBoxLayout()
        equationsWidget = QWidget()
        
        # equationTitle = QLabel("f(x)")
        # equationTitle.setStyleSheet(f"""color:{COLOR2}; font-family: "arial"; font-size: 40px""")
        # equationTitle.setAlignment(Qt.AlignCenter)        

        equationsWidget.setLayout(equationsLayout)
        leftLayout.addWidget(equationsWidget)
        leftLayout.addWidget(QHLine())    

        self.addInput(leftLayout)
        self.addFieldBtn = QPushButton()
        self.addFieldBtn.setIcon(QIcon("./src/assets/icons/add.png"))

        self.addFieldBtn.setStyleSheet(f"""font-size:24px;
                                   border-radius: 6px;
                                   padding: 5px 15px; 
                                   background: #272C3D;
                                   color: {COLOR5};""")

        self.addFieldBtn.setEnabled(False)
        self.addFieldBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.addFieldBtn.clicked.connect(lambda: self.addFunctionToGraph(equationsLayout))
        leftLayout.addWidget(self.addFieldBtn)
        leftLayout.addStretch()
        
        mainSplitter = QSplitter(Qt.Horizontal)
        mainSplitter.addWidget(leftWidget)
        mainSplitter.addWidget(self.graph)
        mainSplitter.setStretchFactor(0, 2)
        mainSplitter.setStretchFactor(1, 4)     
        outerLayout.addWidget(mainSplitter)
                
        ### GUI ###
        centralMainWindow.setLayout(outerLayout)

    # Status Bar
    def _createStatusBar(self):
        self.statusbar = self.statusBar()
        self.statusbar.setStyleSheet(f"""font-size:15px;
                                 padding: 4px;""")
        self.statusbar.showMessage("Ready", 3000)

        # Adding a permanent message
        self.statusbar.addPermanentWidget(QLabel("Function Plotter"))
    
    # Connect
    def _connectActions(self):
        pass
    
    def _connect(self):
        self._connectActions()

    # Add input
    def addInput(self, parent):
        inputWidget = QHBoxLayout()
        
        self.statusImg = QLabel()
        self.statusImg.setPixmap(QPixmap("./src/assets/icons/warn.png").scaled(35,35))

        fxLabel =QLabel("f(x) = ")
        fxLabel.setFont(QFont("arial",16))
        
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Add Function...")
        self.inputField.setStyleSheet(f"""border:1px solid {COLOR1}; 
                                    height:18px; 
                                    padding:4px; 
                                    border-radius:1px; 
                                    font-size:14px;""")

        self.minField = QLineEdit()
        self.minField.setPlaceholderText("min")
        self.minField.setStyleSheet(f"""border:1px solid {COLOR1}; 
                                    height:18px; 
                                    padding:4px; 
                                    border-radius:1px; 
                                    font-size:14px;""")
        self.maxField = QLineEdit()
        self.maxField.setPlaceholderText("max")
        self.maxField.setStyleSheet(f"""border:1px solid {COLOR1}; 
                                    height:18px; 
                                    padding:4px; 
                                    border-radius:1px; 
                                    font-size:14px;""")

        
        self.inputField.textChanged.connect(lambda: self.validateInput(self.inputField.text(), self.minField.text(), self.maxField.text()))
        self.minField.textChanged.connect(lambda: self.validateInput(self.inputField.text(), self.minField.text(), self.maxField.text()))
        self.maxField.textChanged.connect(lambda: self.validateInput(self.inputField.text(), self.minField.text(), self.maxField.text()))

        # Connect to draw function on text change in input field or min/max fields
        self.inputField.textChanged.connect(lambda: self.drawFunction(self.inputField.text(), self.minField.text(), self.maxField.text()))
        self.minField.textChanged.connect(lambda: self.drawFunction(self.inputField.text(), self.minField.text(), self.maxField.text()))
        self.maxField.textChanged.connect(lambda: self.drawFunction(self.inputField.text(), self.minField.text(), self.maxField.text()))
        
        inputWidget.addWidget(self.statusImg,1)
        inputWidget.addWidget(QVLine(),1)
        inputWidget.addWidget(fxLabel,1)
        inputWidget.addWidget(self.inputField,10)
        inputWidget.addWidget(self.minField,2)
        inputWidget.addWidget(self.maxField,2)

        parent.addLayout(inputWidget)

    # Add Function to Graph
    def addFunctionToGraph(self, parent:QVBoxLayout):
        if self.validateInput(self.inputField.text(), self.minField.text(), self.maxField.text()) == False:
            return

        self.addFunctionText(parent, self.inputField.text(), self.minField.text(), self.maxField.text(), len(self.graph.X))
        
        x, y = functionTranslator(self.inputField.text(), float(self.minField.text()), float(self.maxField.text()), STEP)
        self.graph.plotAllData(x,y, self.inputField.text())
        self.resetInputs()

    # Add function text
    def addFunctionText(self, parent:QVBoxLayout, text:str, min:str, max:str, id:int):

        functionTextWidget = QHBoxLayout()
        children = []

        # input label
        label = mathTex_to_QPixmap(text,[min , max])
        inputLabel = QLabel()
        inputLabel.setPixmap(label)
        inputLabel.setCursor(QCursor(Qt.PointingHandCursor))
        inputLabel.setStyleSheet(f"""color:{COLOR2}; font-family: "arial"; font-size: 20px""")
        inputLabel.setWordWrap(True)
        inputLabel.mousePressEvent = lambda event: self.drawFunction(text, float(min), float(max), errors=False)
        
        # Color of line
        colorInput = pg.ColorButton(color=mplColorsList[id])
        colorInput.sigColorChanging.connect(lambda: self.changeLineColor(id, colorInput.color().name()))
        
        # Delete Icon        
        deleteIcon = QLabel()
        deleteIcon.setPixmap(QPixmap("./src/assets/icons/delete.png").scaled(25,25))
        deleteIcon.setCursor(QCursor(Qt.PointingHandCursor))
        deleteIcon.mousePressEvent = lambda event: self.removeFunction(widget=functionTextWidget, items=children, id=id)
        
        functionTextWidget.addWidget(inputLabel, 8)
        children.append(inputLabel)
        functionTextWidget.addWidget(colorInput,1, Qt.AlignRight)
        children.append(colorInput)
        functionTextWidget.addWidget(deleteIcon,1, Qt.AlignRight)
        children.append(deleteIcon)
        
        parent.addLayout(functionTextWidget)    
    
    def changeLineColor(self, id, color):
        self.graph.colors[id] = color
        self.graph.plotAllData2()
    
    # TODO: Browse Function 
    def openFunction(self):
        pass
    
    # Remove Function
    def removeFunction(self,widget:QLayout, items:list(), id:int):
        for item in items:
            widget.removeWidget(item)
            item.deleteLater()
            item = None
        widget.deleteLater()
            
        self.graph.X[id] = []
        self.graph.Y[id] = []
        self.graph.labels[id] = ""
        self.graph.colors[id] = ""
        
        self.graph.plotAllData2()
    
    # Validate Equations on Input Field
    def validateInput(self, text, min, max, errors=True):
        if errors:
            errorsFunction = self.disableAddFieldBtn
        else:
            errorsFunction = lambda: None

        if text == "" or min == "" or max == "":
            self.statusbar.showMessage("Please fill all the fields")
            errorsFunction(warning=True)
            return False

        try:
            functionTranslator(text, float(min), float(max), STEP)
        except Exception as e:
            self.statusbar.showMessage(str(e))
            errorsFunction()
            return False
        
        try:
            float(min)
            float(max)
        except:
            self.statusbar.showMessage("Please enter a valid number")
            errorsFunction()
            return False
        
        if float(min) >= float(max):
            self.statusbar.showMessage("Please enter a valid range")
            errorsFunction()
            return False
        
        if errors:
            self.addFieldBtn.setEnabled(True)
            self.statusbar.showMessage("Ready")
            self.statusImg.setPixmap(QPixmap("./src/assets/icons/ok.png").scaled(35,35))
            
        return True

    # Disable Add Field Button
    def disableAddFieldBtn(self, warning=True):
        self.graph.plotAllData2()
        self.addFieldBtn.setEnabled(False)
        if warning:
            self.statusImg.setPixmap(QPixmap("./src/assets/icons/warn.png").scaled(35,35))
        else:
            self.statusImg.setPixmap(QPixmap("./src/assets/icons/wrong.png").scaled(35,35))
    
    # Draw Function
    def drawFunction(self, text, xMin, xMax, errors=True):
        if self.validateInput(text, xMin, xMax, errors) == False:
            return
        
        x, y = functionTranslator(text, float(xMin), float(xMax), STEP)
        self.graph.plotOneData(x, y, text)

    # Reset Inputs
    def resetInputs(self):
#        self.inputField.setText("")
        # self.minField.setText("")
        # self.maxField.setText("")
        pass
                    
    # Exit the application
    def exit(self):
        exitDialog = QMessageBox.critical(self,
        "Exit the application",
        "Are you sure you want to exit the application?",
        buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        defaultButton=QMessageBox.StandardButton.Yes)

        if exitDialog == QMessageBox.StandardButton.Yes:
            # Exit the application
            sys.exit()