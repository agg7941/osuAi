import re
import numpy as np
import scipy.io.wavfile as wav

rate, data = wav.read('audio.wav')
alen = np.shape(data)[0]
grate, gos = wav.read('gos.wav')
glen = np.shape(gos)[0]
hrate, hit = wav.read('hitsound.wav')
hlen = np.shape(hit)[0]
print(alen, glen, hlen, rate, grate, hrate)

f = open('beatmap.osu')
b = []
t = []
m = []

# reduce for clipping
#data = 0.7 * data

sliderMultiplyer = 1.0
with open('beatmap.osu') as f:
	for l in f:
		if re.match(r'SliderMultiplyer.*', l):
			sliderMultiplier = float(l.split(':')[1])

f = open('beatmap.osu')
for x in f:
	if re.match(r'\[TimingPoints\]', x):
		break
for x in f:
	#print(":".join("{:02x}".format(ord(c)) for c in x))
	if x == "\n":
		break
	a = x.split(',')
	m.append([float(a[0]), float(a[1])])
	if float(a[1]) < 0:
		continue
	b.append(float(a[1]))
	t.append(float(a[0]))
	print(a[0], float(a[1]))
t.append(alen)

for j in range(0, len(t) - 1):
	i = t[j] * 0.001 * rate
	while i < (t[j+1] * 0.001 * rate):
		x = round(i)
		#data[x: x+glen] = data[x: x+glen] + 0.2 * gos
		data[x: x+glen] += (0.2 * gos).astype(data.dtype)
		i = i + b[j] * 0.001 * rate
		if i+glen > alen:
			break
for x in f:
	if re.match(r'\[HitObjects\]', x):
		break
for x in f:
	if x == "\n":
		break
	h = x.split(',')
	x = round(float(h[2]) * 0.001 * rate)
	#data[x : x+hlen] = data[x : x+hlen] + 0.2 * hit
	data[x : x+hlen] += (0.2 * hit).astype(data.dtype)

	if int(h[3]) & 2 == 2:
		sm = None
		l = None
		for i in range(len(m)-1, 0-1, -1):
			if sm != None:
				if m[i][1] < 0.0:
					continue
				l = m[i][1]
				break
			if m[i][0] < float(h[2]):
				if m[i][1] > 0.0:
					sm = 100
					l = m[i][1]
					break
				else:
					sm = m[i][1] * -1
		if l == None:
			l = m[0][1]
			sm = 100

		y = round(float(h[7]) * l / (100/sm * sliderMultiplyer * 100.0) * 0.001 * rate)
		for i in range(1, int(h[6]) + 1):
			if x+(y*i)+hlen > alen:
				break
			#data[x+(y*i) : x+(y*i)+hlen] = data[x+(y*i) : x+(y*i)+hlen] + 0.2 * hit
			data[x+(y*i) : x+(y*i)+hlen] += (0.2 * hit).astype(data.dtype)

wav.write('hits.wav', rate, data)
