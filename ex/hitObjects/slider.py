import re
import numpy as np
import cv2
from imutils.video import FileVideoStream
import subprocess as sp

from libcurves.ccurves import create_curve, get_pos_at
import op

fps = 50.0
sr = 1/50 * 1000
ap = 100
start = 0
o = []
t = []

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

def sliderPoints(h, t):
	bl = float(t[0][1])
	sm = 100
	for i in range(len(t)-1, -1, -1):
		if float(h[2]) < int(t[i][0]):
			continue
		if float(t[i][1]) < 0.0:
			sm = float(t[i][1]) * -1
			continue
		if float(t[i][1]) > 0.0:
			bl = float(t[i][1])
			break

	ln = float(h[7])
	st = h[5].split('|')[0]
	cp = h[5].split('|')[1:]
	
	cps = cp.split('|')
	pos, cum_length = create_curve(st, cps, ln)

	print("new slider:")
	print(pos)
	print(cum_length)

	x = [0] 
	y = [0]

	return x, y

"""
with open('beatmap.osu') as f:
	for l in f:
		if re.match(r'\[TimingPoints\]', l):
			break
	l = f.readline()
	start = float(l.split(',')[0])
"""
"""
AR_TBL = {
	0: 1800,
	1: 1680,
	2: 1560,
	3; 1440,
	4: 1320,
	5: 1200,
	6: 1050,
	7:  900,
	8:  750,
	9:  600,
	10: 450,
}
with open('beatmap.osu') as f:
	for l in f:
		if re.match(r'ApproachRate.*', l):
			AR = AR_TBL[int(l.split(':')[1])]
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
	10: 99.5,
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

vid = FileVideoStream('vid.avi').start()
cmd = ['ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-r', str(fps), '-s', '{}x{}'.format(op.w, op.h), 
  '-i', '-', '-y', '-c:v', 'libx264', '-crf', '18', 'video.avi']
proc = sp.Popen(cmd, stdin=sp.PIPE)

with open('beatmap.osu') as f:
	for l in f:
		if re.match(r'\[TimingPoints\]', l):
			break
	for l in f:
		if x == "\n":
			break
		a = x.split(',')
		m.append([float(a[0]), float(a[1])])
		if float(a[1]) < 0:
			continue
		t.append(a)

with open('beatmap.osu') as f:
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
	if float(o[i][2]) - ap < time:
		if int(o[i][3]) & 2 == 2:
			if float(o[i][2]) < time + sr:
				frame = addPoint(int(o[i][0]), int(o[i][1]), cursor, alpha, frame)
				p = sliderPoints(o[i], t)
				for x, y in p:
					time += sr
					frame = vid.read()
					frame = addPoint(x, y, cursor, alpha, frame)
					proc.stdin.write(frame.tobytes())
			else:
				frame = addPoint(int(o[i][0]), int(o[i][1]), cursor, alpha, frame)
		else:
			frame = addPoint(int(o[i][0]), int(o[i][1]), cursor, alpha, frame)
		
	proc.stdin.write(frame.tobytes())

	time += sr
	if time < float(o[0][2]) - 5000:
		continue
	frame = vid.read()
vid.stop()
proc.stdin.close()
proc.wait()
