# Importing sys package
import sys

# Importing Qt widgets
from PySide2.QtWidgets import QMainWindow, QWidget, QSplitter, QFrame, QVBoxLayout, QHBoxLayout, QToolBar, QAction, QMenu, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide2.QtGui import QIcon, QPixmap, QFont, QFontDatabase, QCursor
from PySide2.QtCore import Qt
import pyqtgraph as pg

# Import Classes
from utilities import *
from QtUtilities import *

# Matplotlib
from plotter import *

# Importing Logging
from log import appLogger

# Global Variables
STEP = 0.001

# Window class
class MainWindow(QMainWindow):
    """Main Window"""
    def __init__(self, theme='dark', *args, **kwargs):
        """Initializer."""
        super(MainWindow, self).__init__(*args, **kwargs)
        
        ### Adding Fonts
        QFontDatabase.addApplicationFont("./assets/fonts/AccanthisADFStd-Regular.otf")
        QFontDatabase.addApplicationFont("./assets/fonts/OpenSans.ttf")
        QFontDatabase.addApplicationFont("./assets/fonts/Enagol-Math-Medium.ttf")

        ### Setting title
        self.setWindowTitle("Function Plotter")
        self.plots_number = 0
        self.theme = theme

        ### Setting Icon
        self.setWindowIcon(QIcon("./assets/icons/function.png"))
        self.setMinimumSize(1000,600)

        ### UI contents
        self.create_actions()
        self.create_menu_bar()
        self.create_status_bar()

        # Central area
        self.init_ui()
   
    ##########################################
    ##########################################

    # Actions
    def create_actions(self):
        # Actions
        self.file_actions()        
        self.help_actions()

    # File Actions
    def file_actions(self):
        # Open Action
        self.open_action = QAction(QIcon(":Open"), "&Open", self)
        # Set Open function to the triggered signal
        self.open_action.triggered.connect(self.open_data)
        self.open_action.setStatusTip('Open file')
        
        # Exit Action
        self.exit_action = QAction(QIcon(":exit"), "&Exit", self)
        # Set exit function to the triggered signal
        self.exit_action.triggered.connect(self.exit)
        self.exit_action.setStatusTip('Exit application')

    # Help Actions
    def help_actions(self):
        self.help_content_action = QAction("&Help Content", self)
        self.help_content_action.setStatusTip('Help')
        
        self.check_updates_action = QAction("&Check For Updates", self)
        self.check_updates_action.setStatusTip('Check Updates')
        
        self.about_action = QAction("&About", self)
        self.about_action.setStatusTip('About')
   
    ##########################################
    
    # Add separator
    def addSeparator(self, parent):
        # Creating a separator action
        separator = QAction(self)
        separator.setSeparator(True)
        parent.addAction(separator)

    # Creating Menu Bar
    def create_menu_bar(self):
        
        # Tool bar
        tool_bar = QToolBar("Toolbar")
        self.addToolBar(tool_bar)

        # Creating menus using a QMenu object
        menu_bar = self.menuBar()

        ## File Menu        
        file_menu = QMenu("&File", self)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.exit_action)

        ## Help Menu
        help_menu = QMenu("&Help", self)
        help_menu.addAction(self.help_content_action)
        help_menu.addSeparator()
        help_menu.addAction(self.check_updates_action)
        help_menu.addSeparator()
        help_menu.addAction(self.about_action)

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(help_menu)
        
    # Context Menu Event
    def context_menu_event(self, event):
        # Creating a menu object with the central widget as parent
        menu = QMenu(self)
        
        # Populating the menu with actions
        menu.addAction(self.open_action)
        self.addSeparator(menu)
        menu.addAction(self.help_content_action)
        menu.addAction(self.check_updates_action)
        menu.addAction(self.about_action)
        self.addSeparator(menu)
        menu.addAction(self.exit_action)
        # Launching the menu
        menu.exec_(event.globalPos())
    
    ##########################################

    # GUI
    def init_ui(self):
        # Main window widget
        central_main_window = QWidget(self)
        self.setCentralWidget(central_main_window)

        # Outer Layout
        outer_layout = QHBoxLayout()
        
        # Graph / Plotter
        self.graph = MplCanvas(None, "Plotter")
        
        # Left layout
        left_layout = QVBoxLayout()
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        
        # Layout that added equations will be in it 
        self.equations_layout = QVBoxLayout()
        self.equations_widget = QFrame()
        self.equations_widget.hide()
        
        self.equations_widget.setLayout(self.equations_layout)
        left_layout.addWidget(self.equations_widget)
        left_layout.addWidget(QHLine())    

        self.add_input_fields(left_layout)
        self.add_equation_button = QPushButton()
        self.add_equation_button.setIcon(QIcon("./assets/icons/add.png"))
        self.add_equation_button.setStyleSheet("""font-size:24px;
                                   border-radius: 6px;
                                   padding: 5px 15px; 
                                   background: #272C3D;
                                   color: #fff;""")

        self.add_equation_button.setEnabled(False)
        self.add_equation_button.setCursor(QCursor(Qt.PointingHandCursor))

        self.add_equation_button.clicked.connect(lambda: self.add_function_to_graph(self.equations_layout))
        left_layout.addWidget(self.add_equation_button)
        left_layout.addStretch()
        
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(self.graph)
        main_splitter.setStretchFactor(0, 2)
        main_splitter.setStretchFactor(1, 4)     
        outer_layout.addWidget(main_splitter)
                
        ### GUI ###
        central_main_window.setLayout(outer_layout)

    # Status Bar
    def create_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("""font-size:15px;
                                 padding: 4px;
                                 color:#fff;
                                 background: #222831;""")
        self.status_bar.showMessage("Ready", 3000)

        # Adding a permanent message
        self.status_bar.addPermanentWidget(QLabel("Function Plotter"))
     
    # Add input
    def add_input_fields(self, parent):
        # Inputs Widget
        inputs_widget = QHBoxLayout()
        
        self.status_image = QLabel()
        self.status_image.setPixmap(QPixmap("./assets/icons/warn.png").scaled(35,35))

        fx_label =QLabel("f(x) = ")
        fx_label.setFont(QFont("arial",16))
        
        self.equation_field = QLineEdit()
        self.equation_field.setPlaceholderText("Add Function...")
        self.equation_field.setStyleSheet("""border:1px solid #222831; 
                                    height:18px; 
                                    padding:4px; 
                                    border-radius:1px; 
                                    font-size:14px;""")

        self.min_field = QLineEdit()
        self.min_field.setPlaceholderText("min")
        self.min_field.setStyleSheet("""border:1px solid #222831; 
                                    height:18px; 
                                    padding:4px; 
                                    border-radius:1px; 
                                    font-size:14px;""")
        self.max_field = QLineEdit()
        self.max_field.setPlaceholderText("max")
        self.max_field.setStyleSheet("""border:1px solid #222831; 
                                    height:18px; 
                                    padding:4px; 
                                    border-radius:1px; 
                                    font-size:14px;""")

        self.equation_field.textChanged.connect(lambda: self.validate_input(self.equation_field.text(), self.min_field.text(), self.max_field.text()))
        self.min_field.textChanged.connect(lambda: self.validate_input(self.equation_field.text(), self.min_field.text(), self.max_field.text()))
        self.max_field.textChanged.connect(lambda: self.validate_input(self.equation_field.text(), self.min_field.text(), self.max_field.text()))

        # Connect to draw function on text change in input field or min/max fields
        self.equation_field.textChanged.connect(lambda: self.draw_equation(self.equation_field.text(), self.min_field.text(), self.max_field.text()))
        self.min_field.textChanged.connect(lambda: self.draw_equation(self.equation_field.text(), self.min_field.text(), self.max_field.text()))
        self.max_field.textChanged.connect(lambda: self.draw_equation(self.equation_field.text(), self.min_field.text(), self.max_field.text()))
        
        inputs_widget.addWidget(self.status_image,1)
        inputs_widget.addWidget(QVLine(),1)
        inputs_widget.addWidget(fx_label,1)
        inputs_widget.addWidget(self.equation_field,10)
        inputs_widget.addWidget(self.min_field,2)
        inputs_widget.addWidget(self.max_field,2)

        parent.addLayout(inputs_widget)

    # Add Function to Graph
    def add_function_to_graph(self, parent:QVBoxLayout):
        self.plots_number += 1
        self.equations_widget.show()
        
        if self.validate_input(self.equation_field.text(), self.min_field.text(), self.max_field.text()) == False:
            return
        
        self.add_equation_widget(parent, self.equation_field.text(), self.min_field.text(), self.max_field.text(), len(self.graph.x_arrays))
        
        x_array, y_array = function_translator(self.equation_field.text(), float(self.min_field.text()), float(self.max_field.text()), STEP)
        self.graph.plot_all_data(x_array,y_array, self.equation_field.text())
        self.reset_inputs()

    # Add function text
    def add_equation_widget(self, parent:QVBoxLayout, text:str, min:str, max:str, id:int):

        equation_text_widget = QHBoxLayout()
        children = []

        # input label
        input_label = QLabel()
        label = mathTex_to_QPixmap(text,[min , max])
        input_label.setPixmap(label)
        input_label.setCursor(QCursor(Qt.PointingHandCursor))
        
        if self.theme == 'dark':
            input_label.setStyleSheet(f"""color:#393E46; font-family: "arial"; font-size: 20px""")
        else:
            input_label.setStyleSheet(f"""color:#2d2d2d; font-family: "arial"; font-size: 20px""")
            
        input_label.setWordWrap(True)
        input_label.mousePressEvent = lambda event: self.draw_equation(text, float(min), float(max), errors=False)
        
        # Color of line
        color_input = pg.ColorButton(color=mplColorsList[id])
        color_input.sigColorChanging.connect(lambda: self.change_line_color(id, color_input.color().name()))
        
        # Delete Icon        
        delete_image = QLabel()
        delete_image.setPixmap(QPixmap("./assets/icons/delete.png").scaled(20,20))
        delete_image.setCursor(QCursor(Qt.PointingHandCursor))
        delete_image.mousePressEvent = lambda event: self.remove_equation(widget=equation_text_widget, items=children, id=id)
        
        equation_text_widget.addWidget(input_label, 8)
        children.append(input_label)
        equation_text_widget.addWidget(color_input,1, Qt.AlignRight)
        children.append(color_input)
        equation_text_widget.addWidget(delete_image,1, Qt.AlignRight)
        children.append(delete_image)
        
        parent.addLayout(equation_text_widget)    
    
    def change_line_color(self, id, color):
        self.graph.colors[id] = color
        self.graph.plot_all_data2()
    
    # TODO: Browse Function 
    def open_data(self):
        pass
    
    # Remove Function
    def remove_equation(self, widget:QLayout, items:list(), id:int):
        for item in items:
            widget.removeWidget(item)
            item.deleteLater()
            item = None
        widget.deleteLater()
            
        self.graph.x_arrays[id] = []
        self.graph.y_arrays[id] = []
        self.graph.labels[id] = ""
        self.graph.colors[id] = ""
        
        self.graph.plot_all_data2()
        self.plots_number -= 1
        
        if self.plots_number == 0:
            self.equations_widget.hide()
    
    # Validate Equations on Input Field
    def validate_input(self, text:str, min:float, max:float, errors:bool=True):
        if errors:
            errors_function = self.disable_add_field_button
        else:
            errors_function = lambda: None

        if text == "" or min == "" or max == "":
            self.status_bar.showMessage("Please fill all the fields")
            errors_function(warning=True)
            return False

        try:
            function_translator(text, float(min), float(max), STEP)
        except Exception as e:
            self.status_bar.showMessage(str(e))
            errors_function()
            return False
        
        try:
            float(min)
            float(max)
        except:
            self.status_bar.showMessage("Please enter a valid number")
            errors_function()
            return False
        
        if float(min) >= float(max):
            self.status_bar.showMessage("Please enter a valid range")
            errors_function()
            return False
        
        if errors:
            self.add_equation_button.setEnabled(True)
            self.status_bar.showMessage("Ready")
            self.status_image.setPixmap(QPixmap("./assets/icons/ok.png").scaled(35,35))
            
        return True

    # Disable Add Field Button
    def disable_add_field_button(self, warning=True):
        self.graph.plot_all_data2()
        self.add_equation_button.setEnabled(False)
        if warning:
            self.status_image.setPixmap(QPixmap("./assets/icons/warn.png").scaled(35,35))
        else:
            self.status_image.setPixmap(QPixmap("./assets/icons/wrong.png").scaled(35,35))
    
    # Draw Function
    def draw_equation(self, text, xMin, xMax, errors=True):
        if self.validate_input(text, xMin, xMax, errors) == False:
            return
        
        x, y = function_translator(text, float(xMin), float(xMax), STEP)
        self.graph.plot_data(x, y, text)

    # Reset Inputs
    def reset_inputs(self):
        self.equation_field.setText("")
        self.min_field.setText("")
        self.max_field.setText("")
                    
    # Exit the application
    def exit(self):
        exit_dialog = QMessageBox.critical(self,
        "Exit the application",
        "Are you sure you want to exit the application?",
        buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        defaultButton=QMessageBox.StandardButton.Yes)

        if exit_dialog == QMessageBox.StandardButton.Yes:
            # Exit the application
            sys.exit()