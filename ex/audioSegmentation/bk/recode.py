import wavio
import numpy as np

a = wavio.read('audio.wav')

sl = int(a.rate * 0.02)
ns = np.shape(a.data)[0] / sl

c = np.empty((int(ns * sl), 2))

for i in range(0, int(ns)):
	c[sl*i : sl*(i+1)] = a.data[sl*i : sl*(i+1)]

wavio.write('recode.wav', c, a.rate, sampwidth=a.sampwidth)

