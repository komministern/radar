#!/usr/bin/env python
# -*- coding: utf-8 -*-

from transceiver.transceiver import Transceiver
from antenna.antenna import Antenna
from environment.environment import Environment
from simulation_constants import Simulation_Constants
import scipy.constants as const
#import radarequations

#import threading
from pyqtgraph.Qt import QtCore     # This is unfortunate. But I will use this package for
                                    # the QTimer, as I got a lot of problems using the 
                                    # threadinf.Timer class. So, until I (need to) get a better
                                    # understanding of periodical timers, here we are.

from observable.observable import Observable


class Radar(Observable):
	
    def __init__(self, **kwds):

        super(Observable, self).__init__(**kwds)
	self.simulation_globals = None 
	self.transceiver = None 
	self.environment = None
	self.antenna = None
		
	self.prf = None					
	self.radar_state = None

#	self._time = None

        self.radar_setup()
	


    # *** PROPERTIES ***

	
    # transceiver
	
    @property
    def transceiver(self):
    	return self._transceiver

    @transceiver.setter
    def transceiver(self, pointer):
    	self._transceiver = pointer

    # environment

    @property
    def environment(self):
    	return self._environment

    @environment.setter
    def environment(self, pointer):
    	self._environment = pointer

    # antenna

    @property
    def antenna(self):
    	return self._antenna

    @antenna.setter
    def antenna(self, pointer):
    	self._antenna = pointer

    # prf
	
    @property
    def prf(self):
    	return self._prf

    @prf.setter
    def prf(self, value):
    	self._prf = value

    # state
		
    @property
    def radar_state(self):
    	return self._radar_state

    @radar_state.setter
    def radar_state(self, newstate):
    	self._radar_state = newstate
	
    # simulation_globals

    @property
    def simulation_globals(self):
    	return self._simulation_globals

    @simulation_globals.setter
    def simulation_globals(self, pointer):
    	self._simulation_globals = pointer



    # *** METHODS ***


    def toggle_radar_state(self, newstate):
	if self.state == 'OFF' and newstate == 'ON':
	    self.state = newstate
            self.timer.start(1000.0 / self.prf)

            # Make certain chsckBoxes etc unCheckable.

	elif self.state == 'ON' and newstate == 'OFF':
	    self.state = newstate

            # Make them checkable again.



    def execute(self):
    	if self.state == 'ON':			
            wf = self.transceiver.transmit_and_listen()
            self.emit('Jesus Lever!', wf)               # Working. But is this the way forward?
    	else:
            pass



    def radar_setup(self):
		
    	self.simulation_globals = Simulation_Constants()

    	self.environment = Environment()
    	self.antenna = Antenna(self.simulation_globals)
    	self.transceiver = Transceiver(self.simulation_globals)

    	self.transceiver.antenna = self.antenna

    	self.antenna.environment = self.environment

    	# radar
	
    	self.prf = 25.0
    	self.state = 'OFF'

    	# transceiver

    	self.transceiver.power = 20.0e3
    	self.transceiver.pulsewidth = 5.0e-6
    	Rmax = 100.0e3
    	self.transceiver.listeningtime = 2.0 * Rmax / const.c
    	self.transceiver.transmit_frequency = 5.0e9
    	self.transceiver.temperature = 290.0
    	self.transceiver.bandwidth = 50.0e6
    	self.transceiver.noise_figure = 4.0
        self.transceiver.receiver_gain = 0.0
    	self.transceiver.resistance = 50.0
    	self.transceiver.final_if = 5.0e6
    	self.transceiver.sample_frequency = 63.0e6
        self.transceiver.impedance = 50.0

        self.transceiver.noise_state = 'OFF'
        self.transceiver.stc_state = 'OFF'
        self.transceiver.stc_choice = 2     # That is, 30km.

    	self.transceiver.set_rectangular_waveform()

#   	self.transceiver.set_biphase_waveform(np.array([1, -1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]))	
        
        # Genereringen av biphase_waveform är antagligen buggad.
	# Otroligt långsam är den i alla fall.
   	
        
#        self.transceiver.set_chirp_waveform(0.0, self.transceiver.final_if)

    	# antenna

    	self.antenna.main_lobe_gain = 36.0	
    	self.antenna.main_lobe_beamwidth = 0.4

        # timer - Observe that new period of the timer is set the next time
        # the radar starts.
		
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.execute)
        self.timer.start(1000.0 / self.prf)
