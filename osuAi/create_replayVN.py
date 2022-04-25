import os
import sys
import copy
import numpy as np
from osr2mp4.osr2mp4 import Osr2mp4
import osuAi

def replaceCursor(play_data):
	global pred, sample_rate
	return osuAi.replaceCursor(play_data, pred, sample_rate)

def create_replay(f, s):
	global pred, sample_rate
	global n
	sample_rate = s
	pred = np.load(f)

	osr2mp4 = Osr2mp4(
		filedata='data.json', filesettings='settingsP.json', filepp='ppsettings.json', filestrain='strainsettings.json',
		logtofile=False, pred=replaceCursor)

	osr2mp4.startaudio()
	osr2mp4.startvideo()
	osr2mp4.cleanup()

if __name__ == "__main__":
	create_replay(sys.argv[1], float(sys.argv[2]))
