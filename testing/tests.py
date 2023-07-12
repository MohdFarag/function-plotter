
import sys
from PyQt5.QtWidgets import QApplication
# Importing Qt widgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import matplotlib.pyplot as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg


def mathTex_to_QPixmap(mathTex, fs):

    #---- set up a mpl figure instance ----
    
    fig = mpl.figure()
    fig.patch.set_facecolor('none')
    fig.set_canvas(FigureCanvasAgg(fig))
    renderer = fig.canvas.get_renderer()

    #---- plot the mathTex expression ----

    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.patch.set_facecolor('none')
    t = ax.text(0, 0, mathTex, ha='left', va='bottom', fontsize=fs)

    #---- fit figure size to text artist ----

    fwidth, fheight = fig.get_size_inches()
    fig_bbox = fig.get_window_extent(renderer)

    text_bbox = t.get_window_extent(renderer)

    tight_fwidth = text_bbox.width * fwidth / fig_bbox.width
    tight_fheight = text_bbox.height * fheight / fig_bbox.height

    fig.set_size_inches(tight_fwidth, tight_fheight)

    #---- convert mpl figure to QPixmap ----

    buf, size = fig.canvas.print_to_buffer()
    qimage = QImage.rgbSwapped(QImage(buf, size[0], size[1],
                                                  QImage.Format_ARGB32))
    qpixmap = QPixmap(qimage)

    return qpixmap


class MyQTableWidget(QTableWidget):   
    def __init__(self, parent=None):
        super(MyQTableWidget, self).__init__(parent)

        self.setHorizontalHeader(MyHorizHeader(self))

    def setHorizontalHeaderLabels(self, headerLabels, fontsize):

        qpixmaps = []
        indx = 0
        for labels in headerLabels:
            qpixmaps.append(mathTex_to_QPixmap(labels, fontsize))            
            self.setColumnWidth(indx, qpixmaps[indx].size().width() + 16)
            indx += 1

        self.horizontalHeader().qpixmaps = qpixmaps

        super(MyQTableWidget, self).setHorizontalHeaderLabels(headerLabels)


class MyHorizHeader(QHeaderView):
    def __init__(self, parent):
        super(MyHorizHeader, self).__init__(Qt.Horizontal, parent)

        self.setStretchLastSection(True)

        self.qpixmaps = []

    def paintSection(self, painter, rect, logicalIndex):

        if not rect.isValid():
            return

        #------------------------------ paint section (without the label) ----

        opt = QStyleOptionHeader()        
        self.initStyleOption(opt)

        opt.rect = rect
        opt.section = logicalIndex
        opt.text = ""

        #---- mouse over highlight ----

        mouse_pos = self.mapFromGlobal(QCursor.pos())               
        if rect.contains(mouse_pos):
            opt.state |= QStyle.State_MouseOver

        #---- paint ----

        painter.save()        
        self.style().drawControl(QStyle.CE_Header, opt, painter, self)
        painter.restore()

        #------------------------------------------- paint mathText label ----

        qpixmap = self.qpixmaps[logicalIndex]

        #---- centering ----

        xpix = int((rect.width() - qpixmap.size().width()) / 2. + rect.x())
        ypix = int((rect.height() - qpixmap.size().height()) / 2.)

        #---- paint ----

        rect = QRect(xpix, ypix, qpixmap.size().width(), qpixmap.size().height())
        painter.drawPixmap(rect, qpixmap)        

    def sizeHint(self):

        baseSize = QHeaderView.sizeHint(self)

        baseHeight = baseSize.height()
        if len(self.qpixmaps):
            for pixmap in self.qpixmaps:
               baseHeight = max(pixmap.height() + 8, baseHeight)
        baseSize.setHeight(baseHeight)

        self.parentWidget().repaint()

        return baseSize
    
# Window class
class MainWindow(QMainWindow):
    """Main Window"""
    def __init__(self, *args, **kwargs):
        """Initializer."""        
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # Outer Layout
        centralMainWindow = QWidget(self)
        self.setCentralWidget(centralMainWindow)
        
        outerLayout = QHBoxLayout()
        x = mathTex_to_QPixmap('$C_{soil}=(1 - n) C_m + \\theta_w C_w$', 20)
        z = QLabel(centralMainWindow).setPixmap(x)
        outerLayout.addWidget(z)
        centralMainWindow.setLayout(outerLayout)


def main():
    """Main function for the application."""

    # Create the application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the event loop
    sys.exit(app.exec_())
    
# main()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = MyQTableWidget()
    w.verticalHeader().hide()

    headerLabels = [
        '$C_{soil}=(1 - n) C_m + \\theta_w C_w$',
        '$k_{soil}=\\frac{\\sum f_j k_j \\theta_j}{\\sum f_j \\theta_j}$',
        '$\\lambda_{soil}=k_{soil} / C_{soil}$']

    w.setColumnCount(len(headerLabels))
    w.setHorizontalHeaderLabels(headerLabels, 25)        
    w.setRowCount(3)
    w.setAlternatingRowColors(True)

    k = 1
    for j in range(3):
        for i in range(3):
            w.setItem(i, j, QTableWidgetItem('Value %i' % (k)))
            k += 1

    w.show() 
    w.resize(700, 200)

    sys.exit(app.exec_())