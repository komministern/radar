# simple code by Krystian Samp - krychu (samp[dot]krystian[monkey]gmail.com), November 2006

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import numpy as np
import scipy.constants as const

import struct

class MyPPI(QLabel): 
 
    def __init__(self, parent=None, **kwds):
        super(MyPPI, self).__init__(parent, **kwds)
        
        self._size = QSize(1000,1000)

        self._origo = QPointF(1.0 * self._size.width() / 2, 1.0 * self._size.height() / 2)
        self._ppiradius = self._size.width() / 2
        self._minsize = QSize(100,100)
#        self._mypixmap = QPixmap(self._size)
        self._myimage = QImage(self._size, QImage.Format_RGB32)      # NEW

        self.maxrange = 3.0e4       # m

#        painter = QPainter(self._mypixmap)
        painter = QPainter(self._myimage)


#        self._mypixmap.fill(QColor(0,0,0))

        pen = QPen(Qt.green)        
        painter.setPen(pen)

        painter.drawEllipse(self._origo, self._ppiradius-1.0, self._ppiradius-1.0)     # A nicer solution is wanted.
        painter.drawEllipse(self._origo, self._ppiradius*3/4, self._ppiradius*3/4)
        painter.drawEllipse(self._origo, self._ppiradius/2, self._ppiradius/2)
        painter.drawEllipse(self._origo, self._ppiradius/4, self._ppiradius/4)
    
#        self._mypixmap = QPixmap.fromImage(self._myimage)

#        self.setPixmap(self._mypixmap)
        self.setPixmap(QPixmap.fromImage(self._myimage))

        self.setMinimumSize(self._minsize)    # Seems resonable
        del painter

        self.ptr = self._myimage.bits()
        self.ptr.setsize(self._myimage.byteCount())
        print self._myimage.byteCount()
        self.arr = np.asarray(self.ptr).reshape(self._myimage.height(), self._myimage.width(), 4)

        print type(self.arr[0,0,0])
        print self.arr[0,0,:]

#        for i in range(100):

            #print qGreen()
#            self.arr[i,i,1] = 255   # Green
#            self.arr[i,i,2] = 255  # Red
            #self.arr[i,i,0] = 255   # Blue



    @property
    def maxrange(self):
        return self._maxrange

    @maxrange.setter
    def maxrange(self, arange):
        self._maxrange = arange






    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

#        newpixmap = self._mypixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        newpixmap = QPixmap.fromImage(self._myimage).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

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

#    def getPoint(self, r, angle):
#        x = np.fix(1.0 * r / self.maxrange * self._size.width() / 2 * np.cos(angle)).astype(int)
#        y = np.fix(1.0 * r / self.maxrange * self._size.height() / 2 * np.sin(angle)).astype(int)
#        return QPoint(x,y) + self._origo



    def drawVector(self, vector, angle):
        if len(vector) < self._ppiradius:
            return
        else:
#            print 'do stuff to image'
#            self._mypixmap = QPixmap.fromImage(self._myimage)

#            painter = QPainter(self._mypixmap)
            painter = QPainter(self._myimage)

            
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

            del painter
            #print len(vector)

#            img = self._myimage

#            ptr = img.bits()
#            ptr.setsize(img.byteCount())

            ## copy the data out as a string
#            strData = ptr.asstring()

            ## get a read-only buffer to access the data
#            buf = buffer(ptr, 0, img.byteCount())

            ## view the data as a read-only numpy array
#            import numpy as np

#            arr = np.frombuffer(buf, dtype=np.ubyte).reshape(img.height(), img.width(), 4)

#            print arr[0:10]

            ## view the data as a writable numpy array
#            arr = np.asarray(ptr).reshape(img.height(), img.width(), 4)




            # 

#            linebytes = self._myimage.bytesPerLine()
#            pixels = self._myimage.scanLine(0).asstring(linebytes)
            
#            x = 0
#            print pixels[x*4:x*4+4]
#            color = struct.unpack('I', pixels[x*4:x*4+4])[0]


#            r = qRed(color);
#            g = qGreen(color);
#            b = qBlue(color);

#            print color[0:10]

#            print r,g,b

#            print struct.pack('I',qRed(color),qGreen(color),qBlue(color))

#            print pixels[0:10]

            print len(vector)

            
            for i in range(500):





            for i in np.arange(len(vector)):
                if vector[i] > 0.0 and i % 20 == 0: # and i % (len(vector) / 1000) == 0:
                    r = const.c * vector.timevector[i] / 2
                    

                    self._myimage.setPoint()
                    x = np.fix( 1.0 * r / self.maxrange * self._size.width() / 2 * np.cos(angle) + self._origo.x()).astype(int)
                    y = np.fix( 1.0 * r / self.maxrange * self._size.height() / 2 * np.sin(angle) + self._origo.y()).astype(int)
                    self.arr[y,x,1] = 255   # Green
                    self.arr[y,x,2] = 255   # Red

                    
                    #(self.getPoint(r,angle))
                    
#            del painter

#            self._mypixmap = QPixmap.fromImage(self._myimage)

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
