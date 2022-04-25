import os
import sys
import numpy as np
from osr2mp4.osr2mp4 import Osr2mp4
import osuAi

def replaceClicks(play_data):
	global pred, sample_rate, thresh
	return osuAi.replaceClicks(play_data, pred, sample_rate, thresh)

def create_replay(f, s, t):
	global pred, sample_rate, thresh
	sample_rate = s
	thresh = t
	pred = np.load(f)

	osr2mp4 = Osr2mp4(
		filedata='data.json', filesettings='settingsP.json', filepp='ppsettings.json', filestrain='strainsettings.json',
		logtofile=False, pred=replaceClicks)

	osr2mp4.startaudio()
	osr2mp4.startvideo()
	osr2mp4.cleanup()

if __name__ == "__main__":
	create_replay(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
