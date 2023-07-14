"""Main application file for the application."""

import sys
from PySide2.QtWidgets import QApplication
from .mainWindow import MainWindow
import qdarkstyle

# Importing Logging
from .log import appLogger

def main():
    """Main function for the application."""

    # Create the application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside2'))


    # Create and show the main window
    window = MainWindow()
    window.show()

    appLogger.debug("Application started successfully.")

    # Start the event loop
    sys.exit(app.exec_())