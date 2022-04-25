import re
import numpy as np
import cv2
from imutils.video import FileVideoStream
import subprocess as sp

import op

fps = 50.0
sr = 1/50 * 1000
ap = 100
start = 0
o = []

op.h = 600
op.w = 1024
op.calratio()

def addPoint(x, y, cursor, alpha, frame):
	x, y = op.cor(x, y)
	w, h, = cursor.shape[0:2]
	a, b, c, d = (0, w, 0, h)
	xo = int(x - w/2)
	yo = int(y - h/2)
	if yo < 0:
		c = -yo
		yo = 0
	if xo < 0:
		a = -xo
		xo = 0
	if yo+h > op.h:
		d = yo+h - op.h
	if xo+w > op.w:
		b = xo+w - op.w

	frame[yo:yo+(d-c), xo:xo+(b-a),:] = frame[yo:yo+(d-c), xo:xo+(b-a),:]*alpha[1][c:d, a:b,:] + cursor[c:d, a:b,:]*alpha[0][c:d, a:b,:]
	
	return frame

"""
with open('beatmap.osu') as f:
	for l in f:
		if re.match(r'\[TimingPoints\]', l):
			break
	l = f.readline()
	start = float(l.split(',')[0])
"""
"""
with open('beatmap.osu') as f:
	for l in f:
		if re.match(r'ApproachRate.*', l):
			AR = int(l.split(':')[1])
			if AR < 5:
				AR = 1800 - 120*(AR)
			else:
				AR = 1200 - 150*(AR-5)
			AR /= 4
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

alpha = cv2.imread('cursor.png', cv2.IMREAD_UNCHANGED)[:,:,3] / 255.0
alpha = alpha.reshape((alpha.shape[0], alpha.shape[1], 1))
alpha = (alpha, 1-alpha)
cursor = cv2.imread('cursor.png')

f = open('beatmap.osu')

vid = FileVideoStream('vid.avi').start()
#out = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps,
#  (op.w, op.h))
cmd = ['ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-r', str(fps), '-s', '{}x{}'.format(op.w, op.h), 
  '-i', '-', '-y', '-c:v', 'libx264', '-crf', '18', 'video.avi']
proc = sp.Popen(cmd, stdin=sp.PIPE)

for l in f:
	if re.match(r'\[HitObjects\]', l):
		break
for l in f:
	o.append(l.split(','))

frame = vid.read()
time = 0.0
i = 0
while True:
	if i == len(o):
		break
	if float(o[i][2]) < time:
		i += 1
		continue

	"""
	j = i - 1
	while j >= 0:
		if float(o[j][2]) < time - ap or float(o[j][2]) > time:
			break
		frame = addPoint(int(o[j][0]), int(o[j][1]), cursor, alpah, frame)
		j -= 1
	"""
	"""
	j = i
	while j < len(o):
		if float(o[j][2]) > time + AR or float(o[j][2]) < time:
			break
		frame = addPoint(int(o[j][0]), int(o[j][1]), cursor, alpha, frame)
		j += 1
	"""
	if float(o[i][2]) < time + ap:
		frame = addPoint(int(o[i][0]), int(o[i][1]), cursor, alpha, frame)
		
	#out.write(frame)
	proc.stdin.write(frame.tobytes())

	time += sr
	if time < float(o[0][2]) - 5000:
		continue
	frame = vid.read()
vid.stop()
proc.stdin.close()
proc.wait()
