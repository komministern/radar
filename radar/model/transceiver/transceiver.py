#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from Waveforms import Sampled_Waveform, Analogue_Waveform
import model.waveforms as wfs

import numpy as np
#import scipy as sc
import scipy.constants as const
import model.radarequations as radarequations
import time


class Transceiver(object):

    def __init__(self, pointer, **kwds):

    	self.simulation_globals = pointer

    	self.antenna = None

    	self.power = None		# kW

    	self.pulsewidth = None
        self.listeningtime = None

	self.final_if_transmit_waveform = None
    	self.final_if_receive_waveforms = None

    	self.transmit_frequency = None
		
    	self.temperature = None		# K
    	self.bandwidth = None		# Hz

    	# The best available receiver technology currently limits the receiver’s noise figure to
    	# around 3dB (less is better). -From www.radar-sales.com.

    	self.noise_figure = None	# dB

    	self.impedance = None		# Ohm

    	self.final_if = None
    	self.sample_frequency = None

        self.noise_state = None
        self.stc_state = None

        super(Transceiver, self).__init__(**kwds)


    # GETTERS AND SETTERS

	
    # simulation_globals

    @property
    def simulation_globals(self):
    	return self._simulation_globals

    @simulation_globals.setter
    def simulation_globals(self, pointer):
    	self._simulation_globals = pointer

    # power

    @property
    def power(self):
		return self._power

    @power.setter
    def power(self, value):
		self._power = value

    # pulsewidth

    @property
    def pulsewidth(self):
    	return self._pulsewidth

    @pulsewidth.setter	
    def pulsewidth(self, value):
    	self._pulsewidth = value

    # antenna

    @property
    def antenna(self):
    	return self._antenna

    @antenna.setter
    def antenna(self, pointer):
    	self._antenna = pointer


    # transmit_frequency

    @property
    def transmit_frequency(self):
    	return self._transmit_frequency

    @transmit_frequency.setter
    def transmit_frequency(self, value):
    	self._transmit_frequency = value

    # final_if

    @property
    def final_if(self):
    	return self._final_if

    @final_if.setter
    def final_if(self, value):
    	self._final_if = value

    # sample_frequency 

    @property
    def sample_frequency(self):
    	return self._sample_frequency

    @sample_frequency.setter
    def sample_frequency(self, value):
    	self._sample_frequency = value


    # final_if_transmit_waveform 

    @property
    def final_if_transmit_waveform(self):
    	return self._final_if_transmit_waveform 

    @final_if_transmit_waveform.setter
    def final_if_transmit_waveform(self, value):
    	self._final_if_transmit_waveform = value

    # final_if_receive_waveforms 

    @property
    def final_if_receive_waveforms(self):
    	return self._final_if_receive_waveforms 

    @final_if_receive_waveforms.setter
    def final_if_receive_waveforms(self, value):
    	self._final_if_receive_waveforms = value

    # listeningtime

    @property
    def listeningtime(self):
    	return self._listeningtime

    @listeningtime.setter
    def listeningtime(self, value):
    	self._listeningtime =  value

    # temperature

    @property
    def temperature(self):
    	return self._temperature

    @temperature.setter
    def temperature(self, value):
    	self._temperature = value

    # bandwidth

    @property
    def bandwidth(self):
    	return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, value):
    	self._bandwidth = value	

    # noise_figure

    @property
    def noise_figure(self):
    	return self._noise_figure

    @noise_figure.setter
    def noise_figure(self, value):
    	self._noise_figure = value

    # impedance

    @property
    def impedance(self):
    	return self._impedance

    @impedance.setter
    def impedance(self, value):
    	self._impedance = value



    # *** METHODS ***


    def toggle_noise(self, newstate):
        if newstate != self.noise_state:
            self.noise_state = newstate


    def toggle_stc(self, newstate):
        if newstate != self.stc_state:
            self.stc_state = newstate






    def generate_final_if_receive_waveforms(self, awf, fs, transmit_freq):
	
#    	t0 = time.time()
	
    	wavelength_fs = const.c / fs							# In meters
    	nbrofdelays = np.fix(wavelength_fs / self.simulation_globals.spatial_resolution) + 1	# The +1 guarantees the spatial resolution to be better than spatial_res.
    	nbrofdelays = nbrofdelays.astype(int)						# Should the actual resolution be accesible somehow? Should it be stored
    	actual_spatial_res = wavelength_fs / nbrofdelays				# in the _globals object perhaps?
    	actual_time_delay_res = 1.0 / fs / nbrofdelays
                
        print "Actual spatial res:", actual_spatial_res
        print "Actual time res:", actual_time_delay_res

    	nbrofdopplers = np.fix(self.simulation_globals.max_abs_velocity / self.simulation_globals.doppler_resolution)	# The resolution is always doppler_res
	nbrofdopplers = nbrofdopplers.astype(int)

    	nbrofsamples = awf.nbrofsamples(fs)

    	waveforms = np.zeros((nbrofdelays, 2*nbrofdopplers + 1, nbrofsamples))


    	delay_vector = np.linspace(0.0, 1.0 / fs, num=nbrofdelays, endpoint=False)  
        doppler_velocity_vector = np.linspace(-nbrofdopplers*self.simulation_globals.doppler_resolution, nbrofdopplers*self.simulation_globals.doppler_resolution, num=2*nbrofdopplers + 1, endpoint=True)

    	for delaybin in range(nbrofdelays):
            for dopplerbin in range(2*nbrofdopplers + 1):

	    	waveforms[delaybin, dopplerbin, :] += awf.digitize(fs, doppler_velocity_vector[dopplerbin], transmit_freq, delay_vector[delaybin]) 

#	print time.time() - t0

        return wfs.Sampled_Waveform(waveforms, fs)
		

    # Set transmitter waveforms.

    def set_rectangular_waveform(self):
	
    	awf = wfs.Analogue_Waveform()
    	awf.timelength = self.pulsewidth
    	awf.set_rect(self.final_if)
		
    	self.final_if_transmit_waveform = awf.digitize(self.sample_frequency, 0.0, self.transmit_frequency, 0.0)
#        self.final_if_transmit_waveform.show()

    	self.final_if_receive_waveforms = self.generate_final_if_receive_waveforms(awf, self.sample_frequency, self.transmit_frequency)
		
    	# The final_if_receive_waveform will for now be the ideal form, with some added
    	# noise in the receiver stage.


    def set_biphase_waveform(self, aphasecode):

    	awf = wfs.Analogue_Waveform()
    	awf.timelength = self.pulsewidth
    	awf.set_biphasecode(self.final_if, aphasecode)

    	self.final_if_transmit_waveform = awf.digitize(self.sample_frequency, 0.0, self.transmit_frequency, 0.0)

    	self.final_if_receive_waveforms = self.generate_final_if_receive_waveforms(awf, self.sample_frequency, self.transmit_frequency)


    def set_chirp_waveform(self, freq_low, freq_high):

    	awf = wfs.Analogue_Waveform()
    	awf.timelength = self.pulsewidth
    	awf.set_chirp(freq_low, freq_high)

    	self.final_if_transmit_waveform = awf.digitize(self.sample_frequency, 0.0, self.transmit_frequency, 0.0)

#        self.final_if_transmit_waveform.show()

    	self.final_if_receive_waveforms = self.generate_final_if_receive_waveforms(awf, self.sample_frequency, self.transmit_frequency)



    # Send pulse and listen. 
	

    def transmit_and_listen(self):
    	listen_wf = self.antenna.listen(self.power, self.transmit_frequency, self.final_if_receive_waveforms, self.listeningtime, self.pulsewidth, self.sample_frequency, self.impedance)

#        listen_wf.show()

        if self.noise_state == 'ON':
    	    listen_wf += radarequations.noise_vrms(self.temperature, self.bandwidth, self.noise_figure, self.impedance) * np.random.randn( len(listen_wf) )

        return listen_wf


	
	# Let's have a STC-function as well! (Seems easy enough.) Should the STC perhaps be implemeted in the Antenna class? For reasons of speed (scipy.weave.blitz) if no other.

	# What is the general form of the STC curve? (k * 1 / r4 obviously, but is this all?)
