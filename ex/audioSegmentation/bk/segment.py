import wavio
import numpy as np

a = wavio.read('right.wav')

sl = int(a.rate * 0.02)
ns = np.shape(a.data)[0] / sl

for i in range(0, int(ns)):
	wavio.write('segments/segment' + f"{i:06}" + '.wav',
	  a.data[sl*i : sl*(i+1)], a.rate, sampwidth=a.sampwidth)
