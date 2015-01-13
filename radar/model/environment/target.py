#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np

class Target(object):

    def __init__(self, r, v, mean_rcs, sw_type, rtime, **kwds):

        super(Target, self).__init__(**kwds)

        self.v = v
        self.r = r
        self.mean_rcs = mean_rcs
        
        self.target_type = sw_type

        self.radartime = rtime

        self.last_reflected_time = None

    # PROPERTIES

    
    # v 

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, avalue):
        self._v = avalue

    # r

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, avalue):
        if avalue > 0.0:
            self._r = avalue
        else:
            self._r = 0.0

    # rcs

    @property
    def mean_rcs(self):
        return self._mean_rcs

    @mean_rcs.setter
    def mean_rcs(self, avalue):
        self._mean_rcs = avalue

    # target_type

    @property
    def target_type(self):
        return self._target_type

    @target_type.setter
    def target_type(self, atype):
        self._target_type = atype

    # info
    # info is effectively called when the target reflects some waveform. That is, when the info method
    # is called from the environment object (which happens before each pulse). The radartime.time will be
    # saved. In this way, we can get the Swerling 1 and 3 cases working. 
    
    @property
    def info(self):
        
        cases = {'SW1' : self.swerling_one,
                'SW2' : self.swerling_two,
                'SW3' : self.swerling_three,
                'SW4' : self.swerling_four,
                'SW5' : self.swerling_five}

        target_info = (self.r, self.v, cases[self.target_type]() )
        self.last_reflected_time = self.radartime.time
        return target_info

    # The Swerling 2 and 4 cases are not implemented so far. Need to get radartime working
    # before this is relevant.

    def swerling_one(self):
        #if self.radartime.time - self.last_reflected_time > SOME TIME LARGER THAN 1/PRF:
        self.last_rcs = self.exp_distr()
        return self.last_rcs
        #else:
            #return self.last_rcs

    def swerling_two(self):
        return self.exp_distr()

    def swerling_three(self):
        #if self.radartime.time - self.last_reflected_time > SOME TIME LARGER THAN 1/PRF:
        self.last_rcs = self.chi_squared_m2_distr()
        return self.last_rcs
        #else:
            #return self.last_rcs

    def swerling_four(self):
        return self.chi_squared_m2_distr()

    def swerling_five(self):
        return self.mean_rcs


    # *** STATISTICS ***

    def exp_distr(self):
        return - self.mean_rcs * np.log( random.random() )

    def chi_squared_m2_distr(self):
        return - self.mean_rcs / 2 * np.log( random.random() * random.random() )

