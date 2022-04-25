import re
import numpy as np
import scipy.io.wavfile as wav

with open('list') as f:
	ns = sum(1 for _ in f)

f = open('list')

rate, a = wav.read('segments/segment000000.wav')
sl = np.shape(a)[0]

c = np.empty((ns * sl, 2), dtype=a.dtype)
print(sl, ns, rate, a.dtype, c.dtype)

i = 0
for x in f:
	m = re.search(r'seg.*\.wav', x).group()
	rate, data = wav.read(m)
	c[sl*i : sl*(i+1)] = data
	i = i + 1

wav.write('concat.wav', rate, c)
