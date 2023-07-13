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
        self.setWindowIcon(QIcon(":icon"))
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
        # Exit Action
        self.exitAction = QAction(QIcon(":exit"), "&Exit", self)
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
        # Menu bar
        menuBar = self.menuBar()

    # Context Menu Event
    def contextMenuEvent(self, event):
        # Creating a menu object with the central widget as parent
        menu = QMenu(self)
        # Populating the menu with actions
        menu.addAction(self.openAction)
        menu.addAction(self.saveAction)
        self.addSeparator(menu)
        menu.addAction(self.clearAction)
        self.addSeparator(menu)
        menu.addAction(self.helpContentAction)
        menu.addAction(self.checkUpdatesAction)
        menu.addAction(self.aboutAction)
        # Launching the menu
        menu.exec(event.globalPos())
    
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
        self.addFieldBtn = QPushButton("Add Function")
        self.addFieldBtn.setStyleSheet(f"""border:1px solid {COLOR1}; 
                                    height:18px; 
                                    padding:3px; 
                                    border-radius:2px; 
                                    font-size:16px;""")
        self.addFieldBtn.clicked.connect(lambda: self.addFunctionToGraph(equationsLayout))
        leftLayout.addWidget(self.addFieldBtn)
        leftLayout.addStretch()
        
        mainSplitter = QSplitter(Qt.Horizontal)
        mainSplitter.addWidget(leftWidget)
        mainSplitter.addWidget(self.graph)
        mainSplitter.setStretchFactor(0, 2)
        mainSplitter.setStretchFactor(1, 4)
        # mainSplitter.setSizes([100,600])
        
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
        self.statusImg.setPixmap(QPixmap("./src/assets/icons/wrong.png").scaled(35,35))

        fxLabel =QLabel("f(x) = ")
        fxLabel.setFont(QFont("arial",16))
        
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Add Function...")
        self.inputField.setStyleSheet(f"""border:1px solid {COLOR1}; 
                                    height:18px; 
                                    padding:3px; 
                                    border-radius:2px; 
                                    font-size:16px;""")

        self.minField = QLineEdit()
        self.minField.setPlaceholderText("min")
        self.minField.setStyleSheet(f"""border:1px solid {COLOR1}; 
                                    height:18px; 
                                    padding:3px; 
                                    border-radius:2px; 
                                    font-size:16px;""")
        self.maxField = QLineEdit()
        self.maxField.setPlaceholderText("max")
        self.maxField.setStyleSheet(f"""border:1px solid {COLOR1}; 
                                    height:18px; 
                                    padding:3px; 
                                    border-radius:2px; 
                                    font-size:16px;""")

        
        self.inputField.textChanged.connect(lambda: self.validateInput(self.inputField.text(), self.minField.text(), self.maxField.text()))
        self.minField.textChanged.connect(lambda: self.validateInput(self.inputField.text(), self.minField.text(), self.maxField.text()))
        self.maxField.textChanged.connect(lambda: self.validateInput(self.inputField.text(), self.minField.text(), self.maxField.text()))

        # Connect to draw function on text change in input field or min/max fields
        self.inputField.textChanged.connect(lambda: self.drawFunction(self.inputField.text(), self.minField.text(), self.maxField.text()))
        self.minField.textChanged.connect(lambda: self.drawFunction(self.inputField.text(), self.minField.text(), self.maxField.text()))
        self.maxField.textChanged.connect(lambda: self.drawFunction(self.inputField.text(), self.minField.text(), self.maxField.text()))
        
        inputWidget.addWidget(self.statusImg,1)
        inputWidget.addWidget(QVLine())
        inputWidget.addWidget(fxLabel,1)
        inputWidget.addWidget(self.inputField,6)
        inputWidget.addWidget(self.minField,1)
        inputWidget.addWidget(self.maxField,1)

        parent.addLayout(inputWidget)

    def addFunctionToGraph(self, parent:QVBoxLayout):
        if self.validateInput(self.inputField.text(), self.minField.text(), self.maxField.text()) == False:
            return

        functionLabelWidget = QHBoxLayout()
        children = []

        id = len(self.graph.X)
        inputLabel = QLabel(f"f(x) = {self.inputField.text()} | [{self.minField.text()} , {self.maxField.text()}]")
        inputLabel.setStyleSheet(f"""color:{COLOR2}; font-family: "arial"; font-size: 20px""")
        # inputLabel.setAlignment(Qt.AlignCenter)
        
        inputLabel.setWordWrap(True)       
        functionLabel = self.inputField.text()
        min = self.minField.text()
        max = self.maxField.text()
               
        inputLabel.mousePressEvent = lambda event: self.drawFunction(functionLabel, float(min), float(max), errors=False)

        deleteIcon = QLabel()
        deleteIcon.setPixmap(QPixmap("./src/assets/icons/delete.png").scaled(20,20))
        functionLabelWidget.addWidget(inputLabel,8)
        children.append(inputLabel)
        functionLabelWidget.addWidget(deleteIcon,1, Qt.AlignRight)
        children.append(deleteIcon)
        deleteIcon.mousePressEvent = lambda event: self.removeFunction(widget=functionLabelWidget, items=children, id=id)
        
        parent.addLayout(functionLabelWidget)
                
        x,y = functionTranslator(self.inputField.text(), float(self.minField.text()), float(self.maxField.text()), STEP)
        self.graph.plotAllData(x,y)
        self.resetInputs()
    
    def removeFunction(self,widget:QLayout, items:list(), id:int):
        for item in items:
            widget.removeWidget(item)
            item.deleteLater()
            item = None
        widget.deleteLater()
            
        self.graph.X[id] = []
        self.graph.Y[id] = []
        self.graph.plotAllData2()
    
    def validateInput(self, text, min, max, errors=True):
        if errors:
            errorsFunction = self.disableAddFieldBtn
        else:
            errorsFunction = lambda: None
        if text == "" or min == "" or max == "":
            self.statusbar.showMessage("Please fill all the fields")
            errorsFunction()
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

    def disableAddFieldBtn(self):
        self.graph.plotAllData2()
        self.addFieldBtn.setEnabled(False)
        self.statusImg.setPixmap(QPixmap("./src/assets/icons/wrong.png").scaled(35,35))
    
    def drawFunction(self, text, xMin, xMax, errors=True):
        if self.validateInput(text, xMin, xMax, errors) == False:
            return
        
        x, y = functionTranslator(text, float(xMin), float(xMax), STEP)
        self.graph.plotOneData(x, y)

    def resetInputs(self):
        self.inputField.setText("")
        self.minField.setText("")
        self.maxField.setText("")
                
    # Exit the application
    def exit(self):
        exitDialog = QMessageBox.critical(self,
        "Exit the application",
        "Are you sure you want to exit the application?",
        buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        defaultButton=QMessageBox.StandardButton.Yes)

        if exitDialog == QMessageBox.StandardButton.Yes.value:
            # Exit the application
            sys.exit()
