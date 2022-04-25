import re
import numpy as np
import scipy.io.wavfile as wav

rate, data = wav.read('audio.wav')
alen = np.shape(data)[0]
hrate, hitsound = wav.read('gos.wav')
hlen = np.shape(hitsound)[0]
print(alen, hlen, rate, hrate)

t = []
m = []

with open('beatmap.osu') as f:
	for l in f:
		if re.match(r'BeatDivisor.*', l):
			BeatDivisor = re.search('BeatDivisor:\s*(\d+).*', l).group(1)
			BeatDivisor = int(BeatDivisor)
			break

f = open('beatmap.osu')
for x in f:
	if re.match(r'\[TimingPoints\]', x):
		break
for x in f:
	#print(":".join("{:02x}".format(ord(c)) for c in x))
	if x == "\n":
		break

	a = x.split(',')
	if float(a[1]) < 0:
		continue
	m.append(float(a[1]))
	t.append(float(a[0]))
	print(a[0], float(a[1]))
t.append(alen)

i = t[1] * 0.001 * rate
d = 0
while i > 0:
	x = round(i)
	if d % BeatDivisor == 0:
		data[x: x+hlen] = 0.7 * data[x: x+hlen] + 0.7 * hitsound
	i -= m[0] * 0.001 * rate
	d -= 1

for j in range(0, len(t) - 1):
	i = t[j] * 0.001 * rate
	d = 0
	while i < (t[j+1] * 0.001 * rate):
		x = round(i)
		if d % BeatDivisor == 0:
			data[x: x+hlen] = 0.7 * data[x: x+hlen] + 0.7 * hitsound
		i += m[j] * 0.001 * rate

		if i+hlen > alen:
			break
		d += 1

wav.write('down.wav', rate, data)
