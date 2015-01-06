#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import sys
from pyqtgraph.Qt import QtGui
import pyqtgraph as pg

from model.radar import Radar
from view.mymainwindow import MyMainWindow
from presenter.presenter import Presenter

if __name__ == "__main__":

#    app = QtGui.QApplication(sys.argv)
    app = pg.mkQApp()

    view = MyMainWindow()
    model = Radar()
    presenter = Presenter(model, view)

    view.show()

#    sys.exit(app.exec_())
    QtGui.QApplication.instance().exec_()


