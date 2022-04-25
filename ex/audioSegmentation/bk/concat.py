import re
import wavio
import numpy as np

with open('list') as f:
	ns = sum(1 for _ in f)

f = open('list')

a = wavio.read('segments/segment000000.wav')
sl = np.shape(a.data)[0]
rate = a.rate
sw = a.sampwidth

c = np.empty((ns * sl, 1), dtype=a.data.dtype)
print(sl, ns, rate, sw, a.data.dtype, c.dtype)

i = 0
for x in f:
	m = re.search(r'seg.*\.wav', x).group()
	a = wavio.read(m)
	c[sl*i : sl*(i+1)] = a.data

wavio.write('concat.wav', c, rate, sampwidth=sw)
