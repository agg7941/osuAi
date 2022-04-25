import os
import sys
import copy
import numpy as np
from osr2mp4.osr2mp4 import Osr2mp4
import osuAi

def replaceBoth(play_data):
	global hpred, vpred, sample_rate, thresh
	play_data = osuAi.replaceCursor(play_data, vpred, sample_rate)
	play_data = osuAi.replaceClicks(play_data, hpred, sample_rate, thresh)
	return play_data

def create_replay(hf, vf, s, t):
	global hpred, vpred, sample_rate, thresh
	sample_rate = s
	hpred = np.load(hf)
	vpred = np.load(vf)
	thresh = t

	osr2mp4 = Osr2mp4(
		filedata='data.json', filesettings='settingsP.json', filepp='ppsettings.json', filestrain='strainsettings.json',
		logtofile=False, pred=replaceBoth)

	osr2mp4.startaudio()
	osr2mp4.startvideo()
	osr2mp4.cleanup()

if __name__ == "__main__":
	create_replay(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
