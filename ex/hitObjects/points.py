import re
import numpy as np
from PIL import Image
import cv2

import op

fps = 50.0
sr = 1/50 * 1000
op.h = 600
op.w = 1024
op.calratio()

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
l = f.readline()
h = l.split(',')
time = 0.0
frame = bg.copy()
while True:
	if float(h[2]) < time:
		x, y = op.cor(int(h[0]), int(h[1]))
		
		w, h = cursor.size
		frame.paste(cursor, (int(x - w/2), int(y - h/2)), cursor)

		l = f.readline()
		if l == "\n" or l == "":
			break
		h = l.split(',')
		continue

	opencvFrame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGBA2BGR)
	out.write(opencvFrame)

	frame = bg.copy()
	time += sr
out.release()
