#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
#import scipy as sc
import scipy.constants as const
import model.radarequations as radarequations
import model.waveforms as wfs

class Antenna(object):

    def __init__(self, pointer, **kwds):

        super(Antenna, self).__init__(**kwds)

    	self.simulation_globals = pointer

    	self.main_lobe_gain = None          # dB (!)
    	self.main_lobe_beamwidth = None

    	self.environment = None
    	self.position = None
    	self.angle = None



    # *** PROPERTIES, GETTERS AND SETTERS ***

	
    # environment

    @property
    def environment(self):
    	return self._environment

    @environment.setter
    def environment(self, value):
    	self._environment = value

    # position
	
    @property
    def position(self):
    	return self._position

    @position.setter
    def position(self, value):
    	self._position = value

    # angle

    @property
    def angle(self):
    	return self._angle

    @angle.setter
    def angle(self, value):
    	self._angle = value

    # main_lobe_gain

    @property
    def main_lobe_gain(self):
    	return self._main_lobe_gain

    @main_lobe_gain.setter
    def main_lobe_gain(self, value):
    	self._main_lobe_gain = value

    # main_lobe_beamwidth

    @property
    def main_lobe_beamwidth(self):
    	return self._main_lobe_beamwidth

    @main_lobe_beamwidth.setter
    def main_lobe_beamwidth(self, value):
    	self._main_lobe_beamwidth = value

    # simulation_globals

    @property
    def simulation_globals(self):
    	return self._simulation_globals

    @simulation_globals.setter
    def simulation_globals(self, pointer):
    	self._simulation_globals = pointer





    # This method determines which of the pre-calculated waveforms that the reflection (due to velocity and distance)
    # has produced.

    def get_received_waveform_from_point_target(self, waveforms, r, velocity, fs):

	if velocity < -1.0 * self.simulation_globals.max_abs_velocity:
            velocity = -1.0 * self.simulation_globals.max_abs_velocity
        elif velocity > self.simulation_globals.max_abs_velocity:
            velocity = self.simulation_globals.max_abs_velocity
        
        dopplerbin = np.around(velocity / self.simulation_globals.doppler_resolution).astype(int)		
        
        lengthbetweensamples = 1.0 / fs * const.c
        
        nbrofdelays = waveforms.shape[0]
        
        q = 2.0 * r / lengthbetweensamples
        
        delaybin = np.fix( (q - np.fix(q)) * nbrofdelays ).astype(int)
        
        return waveforms[delaybin, dopplerbin, :]





    # The listen method is the method called from the transceiver object (or whoever the user is). At the moment only the main beam will be considered, but multiple calls to
    # the calculate_received_beam_waveform can be made.

    def listen(self, power, transmitted_freq, waveforms, listening_time, pulsewidth, fs, impedance, receiver_gain):
        return self.calculate_received_beam_waveform(self.position, self.angle, power, transmitted_freq, self.main_lobe_gain, self.main_lobe_beamwidth, waveforms, listening_time, pulsewidth, fs, impedance, receiver_gain)
		




    # Calculate_received_beam_waveform returns a vector with all the reflections produced by reflectors in the beam. This method will be called multiple times if
    # secondary beams are present in the simulation.

    def calculate_received_beam_waveform(self, position, angle, power, transmitted_freq, gain, beamwidth, waveforms, listening_time, pulsewidth, fs, impedance, receiver_gain):
        
        listen_wf = wfs.Sampled_Waveform(np.zeros(wfs.nsamples(fs, listening_time)), fs)

        # max_range is the longest distance a target can have whilst having part of the reflection
        # occur in our listen_wf
        
        max_range = listening_time * const.c / 2
        env_array = self.environment.get_reflection_vector(position, angle, max_range)
        
        for (r,v,rcs) in env_array:
            
            if r > pulsewidth * const.c / 8 and r < max_range + pulsewidth * const.c:	# Distances shorter than pw*c/8 is not considered. (To avoid division by zero)
                
                i = np.fix( (2.0*r / const.c - pulsewidth) * fs ).astype(int)
                # i is the samplebin which corresponds to the targets distance. i=0 should correspond to
                # a target at r=c*pulsewidth/2

                p_received = radarequations.p_rec(power, gain, rcs, transmitted_freq, r) * radarequations.from_dB(receiver_gain)
                vect_received = self.get_received_waveform_from_point_target(waveforms, r, v, fs)
 

                # If r < pulsewidth*c/2 (but greater than the condition in the if condition above)
    	        # only part of the reflection (the tail) will appear in the listen-vector.                
                if r < pulsewidth * const.c / 2:
                    # Condition implies i < 0
        
                    listen_wf[0:len(vect_received)+i] += vect_received[-i:] * radarequations.vpeak_from_mw(p_received * 1000.0, impedance)
				
    		# If r > Rmax and r < Rmax + pulsewidth*c/2, then only the head of the transmitted
		# waveform will appear in the listening vector.
		elif r > max_range:

                    if i <= len(listen_wf):
                        listen_wf[i:] += vect_received[0:(len(listen_wf)-i)] * radarequations.vpeak_from_mw(p_received * 1000.0, impedance)
                
                # If target in between, just add.
                else:
                    
                    listen_wf[i:i+len(vect_received)] += vect_received * radarequations.vpeak_from_mw(p_received * 1000.0, impedance)
                    
        return listen_wf
