def replace(play_data, pred, sample_rate):
	i = 0

	for i in range(len(play_data)):
		play_data[i][2] = 0

	for i in range(1, len(pred)-1):
		if pred[i] > pred[i-1] and pred[i] > pred[i+1]:
			t = i * (1/sample_rate) * 1000
			j = 0
			k = 0
			while j < len(play_data) and play_data[j][3] < t:
				k = j
				j += 1
			if play_data[k][3] + (1/sample_rate) * 1000 >= pred[i]:
				play_data[k][2] = 10
			elif play_data[j][3] - (1/sample_rate) * 1000 <= pred[i]:
				play_data[j][2] = 10
			else:
				x = (play_data[k][0] + play_data[j][0])/2
				y = (play_data[k][1] + play_data[j][1])/2
				arr.splice(j, 0, [x, y, 10, t])

	return play_data
