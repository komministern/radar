#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from pylab import plot, show, title, xlabel, ylabel, subplot, ylim
from scipy.signal import lfilter, butter, bessel

#import numpy as np
#import scipy as sc
import scipy.constants as const
from functools import partial

#import time

# *** class Analogue_Waveform ***


class Analogue_Waveform(object):
	
    def __init__(self, **kwds):
        
        super(Analogue_Waveform, self).__init__(**kwds)
    	
        self.freq_func = None	# The center frequency of the waveform.
    	self.timelength = None	# Timelength at zero doppler.
    	self.phase_func = None	# A biphase code.
	


    # *** PROPERTIES, GETTERS AND SETTERS ***


    # freq_func

    @property
    def freq_func(self):
    	return self._freq_func

    @freq_func.setter
    def freq_func(self, afunc):
    	self._freq_func = np.vectorize(afunc)	# Vectorize to enable afunc to be fed numpy arrays.
	
    # phase_func

    @property
    def phase_func(self):
    	return self._phase_func

    @phase_func.setter
    def phase_func(self, afunc):
    	self._phase_func = np.vectorize(afunc)	# See comment above.

    # timelength

    @property
    def timelength(self):
    	return self._timelength

    @timelength.setter
    def timelength(self, value):
    	self._timelength = value


    # *** METHODS ***


    def nbrofsamples(self,fs):			# Gives the nbr of samples for a hypothetical fs
    	return nsamples(fs, self.timelength)

    def constant(self, value, t):
    	return value

    def chirp(self, timespan, lowfreq, highfreq, t):
	return lowfreq + (highfreq - lowfreq)*t/timespan

    def phase(self, timespan, aphasecode, t):
		
    	# This is really really slow!!! It probably should be rewritten in some smart way.
    	# But it seems to produce correct results. I'm leaving it for later.

    	#t0 = time.time()
    	bitlength = 1.0 * timespan / len(aphasecode)
    	q = t / bitlength
    	r = np.fix(q)
    	s = r.astype(int)
    	#t1 = time.time()		
    	#numpycode = np.array(aphasecode)		
    	aphasecode = np.append(aphasecode, aphasecode[-1])	# This saves the day if q - np.fix(q) > 0.
		
    	#t2 = time.time()
    	#print t1-t0, t2-t1
    	#print aphasecode[s], type(aphasecode[s])
    	return aphasecode[s]
		
    def set_chirp(self, lowfreq, highfreq):
    	self.freq_func = partial(self.chirp, self.timelength, lowfreq, highfreq)
    	self.phase_func = partial(self.constant, 1.0)

    def set_rect(self, freq):
    	self.freq_func = partial(self.chirp, self.timelength, freq, freq)
    	self.phase_func = partial(self.constant, 1.0)

    #def set_nlfm(self, .....) # Implementation of non linear frequency coding is left to do.

    def set_biphasecode(self, freq, phasecode):
    	self.freq_func = partial(self.constant, freq)
    	self.phase_func = partial(self.phase, self.timelength, phasecode) 

    def digitize(self, fs, velocity, transmit_freq, time_delay):

    	#print time_delay	# Hmmm... time_delay ger lustiga värden. Har jag tänkt helt fel någonstans?????

    	#t0 = time.time()		

    	nbrofsamples = self.nbrofsamples(fs)
    	t = np.linspace(0.0, self.timelength, nbrofsamples, endpoint=False)

    	doppler_freq = np.ones(nbrofsamples) * (2.0 * velocity * transmit_freq / const.c)
			
    	digitized_waveform = np.sin(2*np.pi * (self.freq_func(t - time_delay) + doppler_freq) * (t - time_delay))	# Stiligt med np.vectorize()

		
    	digitized_waveform *= self.phase_func(t - time_delay)	# Slow, slow, slow, slow!!!!!!!!!!!


    	# Då 0 <= time_delay < 1/fs så kommer automatiskt det första samplet i digitized_waveform att vara noll, om time_delay > 0.

    	if time_delay > 0.0:
    	    digitized_waveform[0] = 0.0 

		#print "    ", time.time() - t0

	return Sampled_Waveform(digitized_waveform, fs)


# *** Functions ***


def nsamples(fs, timelength):
    return np.fix(1.0 * timelength * fs).astype(int) + 1







# *** class Sampled_Waveform ***


class Sampled_Waveform(np.ndarray):     # This taken from numpy docs (__new__, __array_finalize__)
	
    def __new__(cls, input_array, _fs=None):
    	obj = np.asarray(input_array).view(cls)
    	obj._fs = _fs
    	return obj

    def __array_finalize__(self, obj):
    	if obj is None: return
    	self._fs = getattr(obj, '_fs', None)

    @property
    def timelength(self):
    	return 1.0 * (len(self) - 1) / self.fs
	
    @property
    def timevector(self):
    	return np.linspace(0.0, self.timelength, len(self)) #(), len(self))

    @property
    def fs(self):
    	return self._fs

    def show(self):

    	print self.timevector #()

    	subplot(3,1,1)
    	plot(self.timevector, self) #(), self)
    	xlabel('Time')
    	ylabel('Amplitude (V)')
		
    	subplot(3,1,2)

    	n = len(self)
    	p = np.fft.fft(self)
    	#print 'n=', n

    	nUniquePts = np.ceil((n+1)/2.0)
    	#print 'nUniquePts=', nUniquePts

    	p = p[0:nUniquePts]
    	p = np.abs(p)

    	p = p / float(n) # scale by the number of points so that
       		         # the magnitude does not depend on the length 
               		 # of the signal or on its sampling frequency  
    	p = p**2 	 # square it to get the power 

    	p = p / 50.0	 # 50 Ohm. Hmmm.... ????
        
        if n % 2 > 0: # we've got odd number of points fft
            p[1:len(p)] = p[1:len(p)] * 2
        else:
    	    p[1:len(p) - 1] = p[1:len(p) - 1] * 2 # we've got even number of points fft
            
        #domf = np.argmax(p)
        
        freqArray = np.arange(0, nUniquePts, 1.0) * (self.fs / n) # Hmmm. Att dela med (n-1) i stället för n gjorde susen(?).
    	plot(freqArray, 30 + 10*np.log10(p), color='r')
	
    	#print 'Max freq: ', freqArray[np.argmax(p)]

    	#ylim((-60,10))	
        
        xlabel('Frequency')
        ylabel('Power (dBm)')
        
        subplot(3,1,3)
        
        plt.psd(self, Fs=self.fs)
        
        show()

    	# Hmmm... Blir nog ganska så stiligt detta!!!?!!

















