#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from model.radar import *
from model.transceiver import *
from model.environment import *
from model.antenna import *
from model.waveforms import Analogue_Waveform
from model.simulation_constants import Simulation_Constants

import time


if __name__ == "__main__":

	glob_const = Simulation_Constants()	# This should be sent as an argument to the objects concerned.

	t = Transceiver(glob_const)
	t.pulsewidth = 16.0e-6
	t.power = 10.0e3		# In Watts
	t.sample_frequency = int(140.0e6)
	t.final_if = int(7.0e6)
	t.transmit_frequency = int(9.0e9)
	t._listeningtime = 200.0e-6

	env = Environment()

	ant = Antenna(glob_const)
	ant.environment = env

	t.antenna = ant

#	t.set_rectangular_waveform()

	t.set_biphase_waveform(np.array([1, -1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]))	# Genereringen av biphase_waveform är antagligen buggad.
															# Otroligt långsam är den i alla fall.
#	t.set_chirp_waveform(0.0, t.final_if)

	t0 = time.time()

	mywf = t.transmit_and_listen()

	print time.time() - t0	

	mywf.show()




