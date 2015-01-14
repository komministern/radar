#!/usr/bin/env python
# -*- coding: utf-8 -*-



class RadarTime(object):

    def __init__(self, inittime, **kwds):
        super(RadarTime, self).__init__(**kwds)

        self.time = inittime



    # *** PROPERTIES ***

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, newtime):
        self._time = newtime


