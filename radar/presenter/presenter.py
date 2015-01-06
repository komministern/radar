#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from PyQt4 import QtCore
from pyqtgraph.Qt import QtCore

#import pyqtgraph as pg
#import numpy as np
import scipy.constants as const

class Presenter(QtCore.QObject):        # Must inherit QObject for beeing able to connect to signals from view.

    def __init__(self, amodel, aview, **kwds):

	self.model = amodel
	self.view = aview

        self.listofnoeditwhiletransmit = []

        # Initialize the view

        self.connect_signals()
        self.update_view_values()
        self.setup_plotwidget()

	super(Presenter, self).__init__(**kwds)


    # *** PROPERTIES ***


    @property
    def model(self):
	return self._model

    @model.setter
    def model(self, amodel):
	self._model = amodel

    @property
    def view(self):
	return self._view

    @view.setter
    def view(self, aview):
	self._view = aview

    @property
    def listofnoeditwhiletransmit(self):
        return self._listofnoeditwhiletransmit

    @listofnoeditwhiletransmit.setter
    def listofnoeditwhiletransmit(self, pointer):
        self._listofnoeditwhiletransmit = pointer


    # *** ACTIONS -> Model ***


    # Control Actions

    def start(self):
        for each in self.listofnoeditwhiletransmit:
            each.setReadOnly(True)
            #each.setPalette( Qt.QPalette( Qt.red ) )
        self.view.ui.pushButton_reinitialize.setEnabled(False)
        self.model.toggle_radar_state('ON')



    def stop(self):
        for each in self.listofnoeditwhiletransmit:
            each.setReadOnly(False)
        self.view.ui.pushButton_reinitialize.setEnabled(True)
        self.model.toggle_radar_state('OFF')



    def reinitialize(self):
        self.model.transceiver.set_rectangular_waveform()



    def noise(self):
        if self.view.ui.checkBox_noise.isChecked():
            self.model.transceiver.toggle_noise('ON')
        else:
            self.model.transceiver.toggle_noise('OFF')



    def stc(self):
        if self.view.ui.checkBox_stc.isChecked():
            self.model.transceiver.toggle_stc('ON')
        else:
            self.model.transceiver.toggle_stc('OFF')



    # Radar Actions

    def prf(self, adouble):
	self.model.prf = adouble

    def samplefrequency(self, adouble):
        self.model.sample_frequency = adouble * 1.0e6

    def listeningtime(self, adouble):
        self.model.transceiver.listeningtime = adouble * 1.0e-6

    # Transmitter Actions

    def power(self, adouble):
	self.model.transceiver.power = adouble * 1.0e3

    def pulsewidth(self, adouble):
	self.model.transceiver.pulsewidth = adouble * 1.0e-6

    def transmitfrequency(self, adouble):
        self.model.transceiver.transmit_frequency = adouble * 1.0e6

    def finaliffrequency(self, adouble):
        self.model.transceiver.final_if = adouble * 1.0e6

    def impedance(self, adouble):
        self.model.transceiver.impedance = adouble

    # Receiver Actions

    def bandwidth(self, adouble):
        self.model.transceiver.bandwidth = adouble * 1.0e6

    def temperature(self, adouble):
        self.model.transceiver.temperature = adouble

    def noisefigure(self, adouble):
        self.model.transceiver.noise_figure = adouble

    # Antenna

    def gain(self, adouble):
        self.model.antenna.main_lobe_gain = adouble

    def beamwidth(self, adouble):
        self.model.antenna.main_lobe_beamwidth = adouble


    # Environment Actions

    def targetone_distance(self, adouble):
        self.model.environment.target_1.r = adouble

    def targetone_velocity(self, adouble):
        self.model.environment.target_1.v = adouble

    def targetone_rcs(self, adouble):
        self.model.environment.target_1.rcs = adouble

    def targettwo_distance(self, adouble):
        self.model.environment.target_2.r = adouble

    def targettwo_velocity(self, adouble):
        self.model.environment.target_2.v = adouble

    def targettwo_rcs(self, adouble):
        self.model.environment.target_2.rcs = adouble





    # *** ACTIONS -> View ***


    def radarevent(self, *args):
#	print 'Presenter notified by model with argument', args[0]

        wf = args[1]

        self.curve.setData(wf.timevector, wf) 

#        self.app.processEvents()            # This is used in a pyqtgraph example. Will need a
                                            # reference to the app though. (Doesn't exist at the moment.)

        self.model.environment.update_targets(1.0 / self.model.prf)
        self.update_view_values()       # Onödigt brutalt. Endast target-relaterade värden behöver uppdateras.


    # Update (parts of) the view.

    def update_view_values(self):
        
        # Radar view

        self.view.ui.doubleSpinBox_samplefrequency.setValue(self.model.transceiver.sample_frequency / 1.0e6)
        self.listofnoeditwhiletransmit.append(self.view.ui.doubleSpinBox_samplefrequency)
        self.view.ui.doubleSpinBox_prf.setValue(self.model.prf)
        self.listofnoeditwhiletransmit.append(self.view.ui.doubleSpinBox_prf)

        # Transmitter view

        self.view.ui.doubleSpinBox_power.setValue(self.model.transceiver.power / 1.0e3)
        self.view.ui.doubleSpinBox_pulsewidth.setValue(self.model.transceiver.pulsewidth * 1.0e6)
        self.listofnoeditwhiletransmit.append(self.view.ui.doubleSpinBox_pulsewidth)
        self.view.ui.doubleSpinBox_transmitfrequency.setValue(self.model.transceiver.transmit_frequency / 1.0e6)
        self.view.ui.doubleSpinBox_finaliffrequency.setValue(self.model.transceiver.final_if / 1.0e6)
        self.listofnoeditwhiletransmit.append(self.view.ui.doubleSpinBox_finaliffrequency)
        self.view.ui.doubleSpinBox_impedance.setValue(self.model.transceiver.impedance)
        self.view.ui.doubleSpinBox_listeningtime.setValue(self.model.transceiver.listeningtime * 1.0e6)

        # Receiver view

        self.view.ui.doubleSpinBox_bandwidth.setValue(self.model.transceiver.bandwidth / 1.0e6)
        self.view.ui.doubleSpinBox_noisefigure.setValue(self.model.transceiver.noise_figure)
        self.view.ui.doubleSpinBox_temperature.setValue(self.model.transceiver.temperature)

        # Antenna view

        self.view.ui.doubleSpinBox_gain.setValue(self.model.antenna.main_lobe_gain)
        self.view.ui.doubleSpinBox_beamwidth.setValue(self.model.antenna.main_lobe_beamwidth)

        # Environment

        self.view.ui.doubleSpinBox_targetonedistance.setValue(self.model.environment.target_1.r)
        self.view.ui.doubleSpinBox_targetonevelocity.setValue(self.model.environment.target_1.v)
        self.view.ui.doubleSpinBox_targetonercs.setValue(self.model.environment.target_1.rcs)
        self.view.ui.doubleSpinBox_targettwodistance.setValue(self.model.environment.target_2.r)
        self.view.ui.doubleSpinBox_targettwovelocity.setValue(self.model.environment.target_2.v)
        self.view.ui.doubleSpinBox_targettworcs.setValue(self.model.environment.target_2.rcs)



    # Do some init stuff to the plotwidget(s).

    def setup_plotwidget(self):
        self.pw = self.view.ui.plotWidget_finalif
        self.view.ui.plotWidget_finalif.setTitle('Final IF')
        self.view.ui.plotWidget_finalif.setLabel('left', 'Value', units='V')
        self.view.ui.plotWidget_finalif.setLabel('bottom', 'Time', units='s')
        self.view.ui.plotWidget_finalif.setYRange(-10.0e-5, 10.0e-5)
        # self.curve är en tillfällig nödlösning. Hur lösa snyggt?
        self.curve = self.pw.plot(pen='y')
#        pg.setConfigOptions(antialias=True)




    # Subscribe to events from both model and view.

    def connect_signals(self):

        # Subscribe to notifications from the model.

        self.model.subscribe(self.radarevent)

	# Connect all actions from view to methods in the presenter.

	# Controls

	self.view.connect(self.view.ui.pushButton_transmit, QtCore.SIGNAL("clicked()"), self.start)
	self.view.connect(self.view.ui.pushButton_stop, QtCore.SIGNAL("clicked()"), self.stop)
        self.view.connect(self.view.ui.checkBox_noise, QtCore.SIGNAL("stateChanged(int)"), self.noise)
        self.view.connect(self.view.ui.checkBox_stc, QtCore.SIGNAL("stateChanged(int)"), self.stc)
        self.view.connect(self.view.ui.pushButton_reinitialize, QtCore.SIGNAL("clicked()"), self.reinitialize)

	# Radar

	self.connect(self.view.ui.doubleSpinBox_prf, QtCore.SIGNAL("valueChanged(double)"), self.prf)
        self.connect(self.view.ui.doubleSpinBox_listeningtime, QtCore.SIGNAL("valueChanged(double)"), self.listeningtime)
        self.connect(self.view.ui.doubleSpinBox_samplefrequency, QtCore.SIGNAL("valueChanged(double)"), self.samplefrequency)

	# Transmitter

	self.connect(self.view.ui.doubleSpinBox_power, QtCore.SIGNAL("valueChanged(double)"), self.power)
	self.connect(self.view.ui.doubleSpinBox_pulsewidth, QtCore.SIGNAL("valueChanged(double)"), self.pulsewidth)
        self.connect(self.view.ui.doubleSpinBox_transmitfrequency, QtCore.SIGNAL("valueChanged(double)"), self.transmitfrequency)
	self.connect(self.view.ui.doubleSpinBox_finaliffrequency, QtCore.SIGNAL("valueChanged(double)"), self.finaliffrequency)
	self.connect(self.view.ui.doubleSpinBox_impedance, QtCore.SIGNAL("valueChanged(double)"), self.impedance)
       
        # Receiver

        self.connect(self.view.ui.doubleSpinBox_bandwidth, QtCore.SIGNAL("valueChanged(double)"), self.bandwidth)
        self.connect(self.view.ui.doubleSpinBox_temperature, QtCore.SIGNAL("valueChanged(double)"), self.temperature)
        self.connect(self.view.ui.doubleSpinBox_noisefigure, QtCore.SIGNAL("valueChanged(double)"), self.noisefigure)

	# Environment

        self.connect(self.view.ui.doubleSpinBox_targetonedistance, QtCore.SIGNAL("valueChanged(double)"), self.targetone_distance)
        self.connect(self.view.ui.doubleSpinBox_targetonevelocity, QtCore.SIGNAL("valueChanged(double)"), self.targetone_velocity)
        self.connect(self.view.ui.doubleSpinBox_targetonercs, QtCore.SIGNAL("valueChanged(double)"), self.targetone_rcs)
        self.connect(self.view.ui.doubleSpinBox_targettwodistance, QtCore.SIGNAL("valueChanged(double)"), self.targettwo_distance)
        self.connect(self.view.ui.doubleSpinBox_targettwovelocity, QtCore.SIGNAL("valueChanged(double)"), self.targettwo_velocity)
        self.connect(self.view.ui.doubleSpinBox_targettworcs, QtCore.SIGNAL("valueChanged(double)"), self.targettwo_rcs)

        # Antenna

        self.connect(self.view.ui.doubleSpinBox_gain, QtCore.SIGNAL("valueChanged(double)"), self.gain)
        self.connect(self.view.ui.doubleSpinBox_beamwidth, QtCore.SIGNAL("valueChanged(double)"), self.beamwidth)



