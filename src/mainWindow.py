# Math
import numpy as np

# Importing sys package
import sys

# Import Classes
from .utilities import *

# Importing Qt widgets
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


# Matplotlib
from .plotter import *

# Importing Logging
from .log import appLogger

# Window class
class MainWindow(QMainWindow):
    """Main Window"""
    def __init__(self, *args, **kwargs):
        """Initializer."""
        super(MainWindow, self).__init__(*args, **kwargs)

        ### Variables
        self.equations = list()

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
        
        graph = MplCanvas(None,"Plotter")
        
        # Left layout
        leftLayout = QVBoxLayout()
        leftWidget = QWidget()
        leftWidget.setLayout(leftLayout)
        mainInput = self.addInput("Add Equation...")
        addField = QPushButton("Add Equation")
        addField.setStyleSheet(f"""border:1px solid {COLOR1}; 
                                    height:18px; 
                                    padding:3px; 
                                    border-radius:2px; 
                                    font-size:16px;""")
        
        leftLayout.addLayout(mainInput)
        leftLayout.addWidget(addField)
        leftLayout.addStretch()
        
        mainSplitter = QSplitter(Qt.Horizontal)
        mainSplitter.addWidget(leftWidget)
        mainSplitter.addWidget(graph)
        
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
    def addInput(self, placeholderText):
        inputWidget = QHBoxLayout()
        
        inputField = QLineEdit()
        inputField.setPlaceholderText(placeholderText)
        inputField.setStyleSheet(f"""border:1px solid {COLOR1}; 
                                    height:18px; 
                                    padding:3px; 
                                    border-radius:2px; 
                                    font-size:16px;""")
        
       
        inputWidget.addWidget(inputField)

        return inputWidget
                  
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
