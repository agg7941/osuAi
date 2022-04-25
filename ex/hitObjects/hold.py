import re
import numpy as np
from PIL import Image
import cv2

import op

fps = 50.0
sr = 1/50 * 1000
ap = 100
op.h = 600
op.w = 1024
op.calratio()

o = []

def addPoint(x, y, frame):
	x, y = op.cor(x, y)
	w, h = cursor.size
	frame.paste(cursor, (int(x - w/2), int(y - h/2)), cursor)
	return frame

bg = Image.open('img.png')
cursor = Image.open('cursor.png')
f = open('beatmap.osu')

w, h = bg.size
print(w, h)
if h/w < op.h/op.w:
	bg = bg.resize((int(w * op.h/h), op.h))
	w, h = bg.size
	bg = bg.crop((int(w/2 - op.w/2), 0, int(w/2 + op.w/2), op.h))
else:
	bg = bg.resize(w, int(h * op.w/w))
	w, h = bg.size
	bg = bg.crop((0, int(h/2 - op.h/2), op.w, int(h/2 + op.h/2)))

out = cv2.VideoWriter('noVideo.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps,
  (op.w, op.h))

for l in f:
	if re.match(r'\[HitObjects\]', l):
		break
for l in f:
	o.append(l.split(','))
time = 0.0
frame = bg.copy()
i = 0
while True:
	if i == len(o):
		break
	j = i - 1
	while j >= 0:
		if float(o[j][2]) < time - ap or float(o[j][2]) > time:
			break
		frame = addPoint(int(o[j][0]), int(o[j][1]), frame)
		j -= 1
	j = i
	while j < len(o):
		if float(o[j][2]) > time + ap or float(o[j][2]) < time:
			break
		frame = addPoint(int(o[j][0]), int(o[j][1]), frame)
		j += 1

	if float(o[i][2]) < time:
		i += 1
		
	opencvFrame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGBA2BGR)
	out.write(opencvFrame)

	frame = bg.copy()
	time += sr
out.release()

