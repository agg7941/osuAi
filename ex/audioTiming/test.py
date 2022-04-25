import numpy as np
import scipy.io.wavfile as wav

rate, data = wav.read('audio.wav')
alen = np.shape(data)[0]
hrate, hitsound = wav.read('beat.wav')
hlen = np.shape(hitsound)[0]
print(alen, hlen, rate, hrate)

i = 13934.548884 * 0.001 * rate
while i+hlen < alen:
	x = round(i)
	data[x: x+hlen] = 0.7 * data[x: x+hlen] + 0.7 * hitsound
	i = i + 363.636363 * 0.001 * rate

wav.write('timed.wav', rate, data)
