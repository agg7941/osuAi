import re
import numpy as np
from PIL import Image
import cv2

import op

fps = 50.0
sr = 1/50 * 1000
ap = 100
start = 0
o = []

op.h = 600
op.w = 1024
op.calratio()

def addPoint(x, y, frame):
	x, y = op.cor(x, y)
	w, h = cursor.size
	frame.paste(cursor, (int(x - w/2), int(y - h/2)), cursor)
	return frame

"""
with open('beatmap.osu') as f:
	for l in f:
		if re.match(r'\[TimingPoints\]', l):
			break
	l = f.readline()
	start = float(l.split(',')[0])
"""
with open('beatmap.osu') as f:
	for l in f:
		if re.match(r'ApproachRate.*', l):
			AR = int(l.split(':')[1])
			if AR < 5:
				preempt = 1200 + 600 * (5 - AR) / 5
				fadein = 800 + 400 * (5 - AR) / 5
				#AR = 1800 - 120*(AR)
			else:
				preempt = 1200 - 750 * (AR - 5) / 5
				fadein = 800 - 500 * (AR - 5) / 5
				#AR = 1200 - 150*(AR-5)
			#AR /= 4
			preempt -= fadein*0.1
			break
"""
AP_TBL = {
	0: 199.5,
	1: 189.5,
	2: 179.5,
	3: 169.5,
	4: 159.5,
	5: 149.5,
	6: 139.5,
	7: 129.5,
	8: 119.5,
	9: 109.5,
	10: 99.5
}
with open('beatmap.osu') as f:
	for l in f:
		if re.match(r'OverallDifficulty.*', l):
			ap = AP_TBL[int(l.split(':')[1])]
			break
"""

cursor = Image.open('cursor.png')
f = open('beatmap.osu')

vid = cv2.VideoCapture('vid.avi')
out = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps,
  (op.w, op.h))

for l in f:
	if re.match(r'\[HitObjects\]', l):
		break
for l in f:
	o.append(l.split(','))

ret, img = vid.read()
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
frame = Image.fromarray(img)
time = 0.0
i = 0
while True:
	if i == len(o):
		break
	if float(o[i][2]) < time:
		i += 1
		continue

	j = i - 1
	"""
	while j >= 0:
		if float(o[j][2]) < time - ap or float(o[j][2]) > time:
			break
		frame = addPoint(int(o[j][0]), int(o[j][1]), frame)
		j -= 1
	"""
	j = i
	while j < len(o):
		if float(o[j][2]) > time + preempt or float(o[j][2]) < time:
			break
		frame = addPoint(int(o[j][0]), int(o[j][1]), frame)
		j += 1
	"""
	if float(o[i][2]) < time + ap:
		frame = addPoint(int(o[i][0]), int(o[i][1]), frame)
	"""
		
	opencvFrame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGBA2BGR)
	out.write(opencvFrame)

	time += sr
	if time < float(o[0][2]) - 5000:
		continue
	ret, img = vid.read()
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	frame = Image.fromarray(img)
out.release()

