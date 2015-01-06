#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from collections import List

class Observable(list):

    def __init__(self, **kwds):
        super(list, self).__init__(**kwds)

    def emit(self, *args):
#        print 'emit sent to subscribers'
        for subscriber in self:
            subscriber(*args)           # Call subscribers with args.

    def subscribe(self, subscriber):    # Register new subscriber.
        self.append(subscriber)

