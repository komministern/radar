#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Target(object):

    def __init__(self, r, v, rcs, sw_type, **kwds):

        super(Target, self).__init__(**kwds)

        self.v = v
        self.r = r
        self.rcs = rcs
        
        self.target_type = sw_type

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
    def rcs(self):
        return self._rcs

    @rcs.setter
    def rcs(self, avalue):
        self._rcs = avalue

    # target_type

    @property
    def target_type(self):
        return self._target_type

    @target_type.setter
    def target_type(self, atype):
        self._target_type = atype

    # info

    @property
    def info(self):
        return (self.r, self.v, self.rcs)


