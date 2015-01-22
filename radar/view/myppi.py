# simple code by Krystian Samp - krychu (samp[dot]krystian[monkey]gmail.com), November 2006

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import numpy as np
import scipy.constants as const

class MyPPI(QLabel): 
 
    def __init__(self, parent=None, **kwds):
        super(MyPPI, self).__init__(parent, **kwds)
        
        self._size = QSize(1000,1000)
        self._origo = QPointF(1.0 * self._size.width() / 2, 1.0 * self._size.height() / 2)
        self._ppiradius = self._size.width() / 2
        self._minsize = QSize(100,100)
        self._mypixmap = QPixmap(self._size)

        self.maxrange = 3.0e4       # m

        painter = QPainter(self._mypixmap)

        self._mypixmap.fill(QColor(0,0,0))
        pen = QPen(Qt.green)        
        painter.setPen(pen)

        painter.drawEllipse(self._origo, self._ppiradius-1.0, self._ppiradius-1.0)     # A nicer solution is wanted.
        painter.drawEllipse(self._origo, self._ppiradius*3/4, self._ppiradius*3/4)
        painter.drawEllipse(self._origo, self._ppiradius/2, self._ppiradius/2)
        painter.drawEllipse(self._origo, self._ppiradius/4, self._ppiradius/4)
         
        self.setPixmap(self._mypixmap)
        self.setMinimumSize(self._minsize)    # Seems resonable
        del painter


    @property
    def maxrange(self):
        return self._maxrange

    @maxrange.setter
    def maxrange(self, arange):
        self._maxrange = arange






    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        newpixmap = self._mypixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        ax, ay, aw, ah = self.frameRect().getRect()
        x,y = 0,0
        if aw > ah:
            x = (aw-ah) / 2
        else:
            y = (ah-aw) / 2
        painter.drawPixmap(x, y, newpixmap)
        del painter



    def getPointF(self, r, angle):
        # 0 degrees is north.
        x = 1.0 * r / self.maxrange * self._size.width() / 2 * np.cos(angle)
        y = 1.0 * r / self.maxrange * self._size.height() / 2 * np.sin(angle)
        return QPointF(x,y) + self._origo


    def drawVector(self, vector, angle):
        if len(vector) < self._ppiradius:
            return
        else:

            painter = QPainter(self._mypixmap)
            
            brush = QBrush(Qt.black)
            painter.setBrush(brush) 
            painter.drawPolygon(self._origo, self.getPointF(self.maxrange,angle), self.getPointF(self.maxrange, angle+np.pi/90))

            pen = QPen(Qt.green)
            painter.setPen(pen)
            painter.drawLine(self.getPointF(self.maxrange-1.0, angle), self.getPointF(self.maxrange-1.0, angle+np.pi/90))
            painter.drawLine(self.getPointF(self.maxrange*3/4, angle), self.getPointF(self.maxrange*3/4, angle+np.pi/90))
            painter.drawLine(self.getPointF(self.maxrange/2, angle), self.getPointF(self.maxrange/2, angle+np.pi/90))
            painter.drawLine(self.getPointF(self.maxrange/4, angle), self.getPointF(self.maxrange/4, angle+np.pi/90))
             
            pen = QPen(Qt.yellow)
            painter.setPen(pen)
            painter.drawLine(self._origo, self.getPointF(self.maxrange, angle+np.pi/180))
            #print len(vector)

            

            for i in np.arange(len(vector)):
                if vector[i] > 0.0 and i % (len(vector) / 500):
                    r = const.c * vector.timevector[i] / 2
                    painter.drawPoint(self.getPointF(r,angle))
                    
            del painter
            self.update()


#    def getPointFFromPolar(self, r, angle):

#        pass
        #return PointF(x,y)



class MainWindow(QMainWindow):
    def __init__(self, **kwds):
        super(MainWindow, self).__init__(**kwds)
        self.ppi = MyPPI(self)
        self.setCentralWidget(self.ppi)





if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
   
    sys.exit(app.exec_())
