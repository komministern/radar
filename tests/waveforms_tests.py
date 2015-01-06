#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import *
from radar.model.waveforms import Analogue_Waveform, Sampled_Waveform

def test_Analogue_Waveform():
	
	wf = Analogue_Waveform()

	wf.timelength = 1.0

	assert_equal(wf.nbrofsamples(1000.0), 1001)
	
