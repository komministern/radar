# simple code by Krystian Samp - krychu (samp[dot]krystian[monkey]gmail.com), November 2006

import sys
#from PyQt4 import Qt, QtGui, QtCore

from PyQt4.QtGui import *
from PyQt4.QtCore import *
#from PyQt4.Qt import bitBlt
#from PyQt4.QtCore import bitBlt
#import Qt

class MyPPI(QLabel): 
 
    def __init__(self, parent=None, **kwds):
        super(MyPPI, self).__init__(parent, **kwds)
        
        self.mypixmap = QPixmap(QSize(1000,1000))
        painter = QPainter(self.mypixmap)

        self.mypixmap.fill(QColor(0,0,0))
        pen = QPen(Qt.green)        
        painter.setPen(pen)

        painter.drawEllipse(QPointF(500.0,500.0), 499.0, 499.0)
        painter.drawEllipse(QPointF(500.0,500.0), 375.0, 375.0)
        painter.drawEllipse(QPointF(500.0,500.0), 250.0, 250.0)
        painter.drawEllipse(QPointF(500.0,500.0), 125.0, 125.0)
         
        del painter

        self.setPixmap(self.mypixmap)
        self.setMinimumSize(100,100)

        

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        newpixmap = self.mypixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        ax, ay, aw, ah = self.frameRect().getRect()

        x,y = 0,0
        if aw > ah:
            x = (aw-ah) / 2
        else:
            y = (ah-aw) / 2

        painter.drawPixmap(x, y, newpixmap)
        
        del painter








class MainWindow(QMainWindow):
    def __init__(self, **kwds):
        super(MainWindow, self).__init__(**kwds)
        self.ppi = MyPPI(self)
        self.setCentralWidget(self.ppi)





if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
   
#    view = QWidget()

#    pm = MyPixMap(QSize(1000,1000))

#    view.show()
    sys.exit(app.exec_())
