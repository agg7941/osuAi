import numpy as np

def replaceClicks(play_data, pred, sample_rate, thresh):
	p = 1/sample_rate * 1000
	for i in range(len(play_data)):
		play_data[i][2] = 0

	for i in range(1, len(pred)-1):
		if pred[i] > pred[i-1] and pred[i] > pred[i+1] and pred[i] >= thresh:
			t = i*p
			j = 0
			k = 0
			while j < len(play_data)-1 and play_data[j][3] < t:
				k = j
				j += 1
			a = None
			b = None
			if play_data[k][3] + p >= pred[i]:
				a = abs(play_data[k][3] - pred[i])
			elif play_data[j][3] - p <= pred[i]:
				b = abs(play_data[j][3] - pred[i])
			if a is not None and (b is None or a < b):
				#x = play_data[k][0]
				#y = play_data[k][1]
				play_data[k][2] = 10
			elif b is not None and (a is None or b < a):
				#x = play_data[j][0]
				#y = play_data[j][1]
				play_data[j][2] = 10
			else:
				x = (play_data[k][0] + play_data[j][0])/2
				y = (play_data[k][1] + play_data[j][1])/2
				play_data.insert(j, [x, y, 10, t])

	return play_data

def replaceCursor(play_data, pred, sample_rate):
	p = 1 / sample_rate * 1000

	n = [None] * (len(pred) + 1) 
	for i in range(len(pred)):
		n[i] = [0.0, 0.0, 0, 0.0]
		n[i][0] = pred[i][1] * 512
		n[i][1] = pred[i][0] * 384
		n[i][3] = i*p + play_data[0][3]

	for i in range(len(play_data)):
		t = float(play_data[i][3] - 0.0)
		j = 0
		k = 1
		while k < len(n):
			if n[k] is None:
				break
			if n[j][3] <= t and t <= n[k][3]:
				a = abs(n[j][3] - t)
				b = abs(n[k][3] - t)
				if a < b:
					n[j][2] = 10 #play_data[i][2]
				else:
					n[k][2] = 10 #play_data[i][2]
				break
			else:
				j += 1
				k += 1

	n[-1] = [0.0, 0.0, 0, play_data[-1][3]]
	return n
