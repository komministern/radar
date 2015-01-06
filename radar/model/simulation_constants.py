#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Perhaps this should be realized through a non-instantialized class pattern
# instead of this. But this is nicer, isn't it?

class Simulation_Constants(object):

	def __init__(self):

		self._spatial_resolution = 0.3		# m
		self._doppler_resolution = 5.0		# m/s
		self._max_abs_velocity = 200.0		# m/s

		self._real_spatial_resolution = None	# Hmmmm.....
		self._real_doppler_resolution = None	# Is this a good idea?



	@property
	def spatial_resolution(self):
		return self._spatial_resolution

	@spatial_resolution.setter
	def spatial_resolution(self, value):
		self._spatial_resolution = value

	@property
	def doppler_resolution(self):
		return self._doppler_resolution

	@doppler_resolution.setter
	def doppler_resolution(self, value):
		self._doppler_resolution = value

	@property
	def max_abs_velocity(self):
		return self._max_abs_velocity

	@max_abs_velocity.setter
	def max_abs_velocity(self, value):
		self._max_abs_velocity = value



