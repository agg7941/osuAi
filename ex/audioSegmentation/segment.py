import scipy.io.wavfile as wav
import numpy as np

rate, data = wav.read('audio.wav')

sl = int(rate * 0.02)
ns = np.shape(data)[0] / sl

for i in range(0, int(ns)):
	wav.write('segments/segment' + f"{i:06}" + '.wav', rate,
	  data[sl*i : sl*(i+1)])
