#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
#import scipy as sc
#import scipy.constants as const

import random

from target import Target

class Environment(object):

    def __init__(self, **kwds):

        super(Environment, self).__init__(**kwds)
        
        self.target_1 = None
        self.target_2 = None
        self.targets = []

        self.setup_targets()


    # PROPERTIES

    @property
    def targets(self):
        return self._targets

    @targets.setter
    def targets(self, pointer):
        self._targets = pointer

    @property
    def target_1(self):
        return self._target_1

    @target_1.setter
    def target_1(self, pointer):
        self._target_1 = pointer

    @property
    def target_2(self):
        return self._target_2

    @target_2.setter
    def target_2(self, pointer):
        self._target_2 = pointer


    # METHODS

    def setup_targets(self):
        self.target_1 = Target(r=35000.0, v=50.0, rcs=100.0)
        self.target_2 = Target(r=50000.0, v=-35.0, rcs=100.0)
        self.targets.append(self.target_1)
        self.targets.append(self.target_2)


    def set_r_target_1(self, value):
        self.target_1.r = value

    def set_v_target_1(self, value):
        self.target_1.v = value

    def set_rcs_target_1(self, value):
        self.target_1.rcs = value

    def set_r_target_2(self, value):
        self.target_2.r = value

    def set_v_target_2(self, value):
        self.target_2.v = value

    def set_rcs_target_2(self, value):
        self.target_2.rcs = value



    def createtargets(self, n, Rmin, Rmax):

        self.targets = []

        for i in range(n):
            self.targets.append(Target(random.randint(Rmin,Rmax), 0.0, 100.0))


        





    def update_targets(self, delta_t):
        for element in self.targets:
            element.r += element.v * delta_t



    def get_reflection_vector(self, position, angle, max_distance):
        reflection_array = np.array([element.info for element in self.targets])	 	
	return reflection_array			




