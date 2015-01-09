#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PointTarget(object):

    def __init__(self, r, v, rcs, **kwds):

        super(PointTarget, self).__init__(**kwds)

        self.v = v
        self.r = r
        self.rcs = rcs
        


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

    # info

    @property
    def info(self):
        return (self.r, self.v, self.rcs)


