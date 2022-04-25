import os
import numpy as np
from osr2mp4.osr2mp4 import Osr2mp4

pred = np.load('pred.npy')

osr2mp4 = Osr2mp4(
	filedata='data.json', filesettings='settings.json', filepp='ppsettings.json', filestrain='strainsettings.json',
	logtofile=False, 
	pred=pred, sample_rate=44100/441/2)

osr2mp4.startaudio()
osr2mp4.startvideo()
osr2mp4.cleanup()
