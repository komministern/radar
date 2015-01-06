#!/usr/bin/env python
# -*- coding: utf-8 -*-

###from PyQt4 import QtGui, uic
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

from pyqtgraph.Qt import loadUiType

WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType('./resources/radarmainwindow.ui')
#WindowTemplate, TemplateBaseClass = loadUiType('./resources/radarmainwindow.ui')

###class MyMainWindow(QtGui.QMainWindow):
    
###    def __init__(self, **kwds):
###        super(MyMainWindow, self).__init__(**kwds)      # THIS MUST BE EXECUTED BEFORE loadUI!
###	self.ui = uic.loadUi('./resources/radarmainwindow.ui', self)


class MyMainWindow(TemplateBaseClass):
    def __init__(self, **kwds):

        super(TemplateBaseClass, self).__init__(**kwds)
#        TemplateBaseClass.__init__(self)
#        self.setWindowTitle('Jesus Lever!')

        # Create main window

        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        

    # *** PROPERTIES ***


    @property
    def ui(self):
	return self._ui

    @ui.setter
    def ui(self, pointer):
	self._ui = pointer

