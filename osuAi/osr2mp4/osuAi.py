import numpy as np

def replaceClicks(play_data, pred, sample_rate, thresh):
	i = 0

	for i in range(len(play_data)):
		play_data[i][2] = 0

	for i in range(1, len(pred)-1):
		if pred[i] > pred[i-1] and pred[i] > pred[i+1] and pred[i] >= thresh:
			t = i * (1/sample_rate) * 1000
			j = 0
			k = 0
			while j < len(play_data)-1 and play_data[j][3] < t:
				k = j
				j += 1
			a = None
			b = None
			if play_data[k][3] + (1/sample_rate) * 1000 >= pred[i]:
				a = abs(play_data[k][3] - pred[i])
			elif play_data[j][3] - (1/sample_rate) * 1000 <= pred[i]:
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
    j = 0
    p = 1 / sample_rate * 1000
    
    n = np.zeros((len(pred), 4))
    for i in range(len(pred)):
        n[i][0] = pred[i][1]
        n[i][1] = pred[i][0]
        n[i][3] = i*p
        
        while play_data[j][3] + p < i*p:
            j += 1
            
        if play_data[j][3] < i*p and play_data[j][3] + p > i*p:
            n[i][2] = play_data[j][2]
    
    return n
