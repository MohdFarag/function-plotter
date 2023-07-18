"""Main application file for the application."""

import sys
from PySide2 import QtWidgets
from qdarktheme import load_stylesheet
from mainWindow import MainWindow

# Importing Logging
from log import appLogger

def main():
    """Main function for the application."""

    # Create the application
    app = QtWidgets.QApplication(sys.argv)
    theme = "light"
    app.setStyleSheet(load_stylesheet(theme=theme))
    
    # Create and show the main window
    window = MainWindow(theme=theme)
    window.show()

    appLogger.debug("Application started successfully.")

    # Start the event loop
    sys.exit(app.exec_())