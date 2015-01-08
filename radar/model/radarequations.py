#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scipy.constants as const
import numpy as np

# Simple form of the radar equation. Input is transmitted power, antenna gain, frequency, distance and 
# rcs, output is the power at the receiver input (that is, just after the antenna).

def p_rec(p_tr, gain, sigma, freq, r):	
	return p_tr * from_dB(gain)**2 * const.c**2 * sigma / (freq**2 * (4*np.pi)**3 * r**4)


# dBm, mW, etc för sinusvågor. Standardimpedansen är alltid 50 Ohm, om inget annat anges.
def dbm_voltage_ref(R):
	return np.sqrt(0.001 * R)


# The following true for sines only

def dbm_from_vrms(vrms, R=50.0):
	return 20.0 * np.log10( vrms / dbm_voltage_ref(R) ) 

def dbm_from_vpeak(vpeak, R=50.0):
	return dbm_from_vrms(vpeak / 2**0.5, R=50.0)

def vrms_from_dbm(dbm, R=50.0):
	return dbm_voltage_ref(R) * 10**(dbm / 20.0)

def vpeak_from_dbm(dbm, R=50.0):
	return 2**0.5 * vrms_from_dbm(dbm, R)

def vrms_from_mw(mw, R=50.0):
	return vrms_from_dbm( dbm_from_mw(mw), R)

def vpeak_from_mw(mw, R=50.0):
	return 2**0.5 * vrms_from_mw(mw, R)



# Power conversions

def mw_from_dbm(dbm):
	return 10 ** (dbm / 10.0)

def dbm_from_mw(mw):
	return 10 * np.log10(mw)


# Ratio conversions

def to_dB(ggr):
	return 10 * np.log(ggr)

def from_dB(db):
	return 10**(db/10.0)


# Noise

# This is from the radartutorial.eu:  (Is this the correct way of using the noise figure?)
# For all these reasons, the quantity kT0B is regarded as a minimum input noise power, only attainable in an "ideal" 
# receiver. Noise in a practical receiver is invariably greater by some factor Fn, expressed in Decibels and known as 
# the noise figure.

def noise_vrms(T, B, Fn, Gr, R=50.0):
	p_noise = const.k * T * B * from_dB(Fn) * from_dB(Gr)	# mW
	v_rms = np.sqrt(4 * R * p_noise)	# V
	return v_rms
	


