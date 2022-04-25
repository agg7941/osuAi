import os
import cv2
import math
import numpy as np
from imutils.video import FileVideoStream
import subprocess as sp

import op
from osr2mp4.EEnum.EReplay import Replays
from osr2mp4.osr2mp4 import Osr2mp4

op.h = 600
op.w = 1024
op.calratio()

def addPoint(x, y, cursor, alpha, frame):
	x, y = op.cor(x, y)
	w, h = cursor.shape[0:2]
	a, b, c, d = (0, w, 0, h)
	xo = int(x - w/2)
	yo = int(y - h/2)
	if xo >= op.w or yo >= op.h:
		#print(xo, yo, op.w, op.h)
		return frame
	if yo < 0:
		c = -yo
		yo = 0
	if xo < 0:
		a = -xo
		xo = 0
	if yo+h > op.h:
		d = op.h - yo
	if xo+w > op.w:
		b = op.w - xo

	frame[yo:yo+(d-c), xo:xo+(b-a),:] = frame[yo:yo+(d-c), xo:xo+(b-a),:]*alpha[1][c:d, a:b,:] + cursor[c:d, a:b,:]*alpha[0][c:d, a:b,:]

	return frame

osr2mp4 = Osr2mp4(filedata='data.json', filesettings='settings.json', filepp='ppsettings.json', filestrain='strainsettings.json')

#osr2mp4.startaudio()
#osr2mp4.startvideo()

fps = 50
sr = 1/fps * 1000

alpha = cv2.imread('cursor.png', cv2.IMREAD_UNCHANGED)[:,:,3] / 255.0
alpha = alpha.reshape((alpha.shape[0], alpha.shape[1], 1))
alpha = (alpha, 1-alpha)
cursor = cv2.imread('cursor.png')

cmd = ['ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-r', str(fps), '-s', '{}x{}'.format(op.w, op.h), 
  '-i', '-', '-y', '-c:v', 'libx264', '-crf', '18', 'video.mp4']
proc = sp.Popen(cmd, stdin=sp.PIPE)

offset = osr2mp4.replay_info.play_data[0][Replays.TIMES]
cursorstream = np.zeros((math.ceil((osr2mp4.replay_info.play_data[-1][Replays.TIMES] - offset) * 0.001 * fps), 2), dtype=np.float32)

for j in range(len(osr2mp4.replay_info.play_data) - 1):
	a = osr2mp4.replay_info.play_data[j]
	b = osr2mp4.replay_info.play_data[j+1]
	delta = (b[Replays.TIMES] - a[Replays.TIMES]) * 0.001 * fps
	xdist = b[Replays.CURSOR_X] - a[Replays.CURSOR_X]
	ydist = b[Replays.CURSOR_Y] - a[Replays.CURSOR_Y]
	stime = (a[Replays.TIMES] - offset) * 0.001 * fps
	x = a[Replays.CURSOR_X]
	y = a[Replays.CURSOR_Y]

	def f(x, o):
		c = 20 # curve
		o = o/2
		#print(x, o)
		if o == 0:
			return x
		return o*2 * 1 / (1 + math.exp(-1 * c * (x - o) / o))
	for t in range(math.ceil(delta)):
		#cursorstream[int(stime + t)] = (x + xdist/delta*t, y + ydist/delta*t)
		cursorstream[int(stime + t)] = (x + f((xdist/delta*t), xdist), y + f((ydist/delta*t), ydist))

	cursorstream[int((b[Replays.TIMES] - offset) * 0.001 * fps)] = (b[Replays.CURSOR_X], b[Replays.CURSOR_Y])
#cursorstream = cursorstream[int(osr2mp4.replay_info.play_data[0][Replays.TIMES] * 0.001 * fps):]

vid = FileVideoStream('vid.mp4').start()
frame = vid.read()
print(len(cursorstream))
for e in cursorstream:
	if e[0] != 0 and e[1] != 0:
		frame = addPoint(e[0], e[1], cursor, alpha, frame)

	proc.stdin.write(frame.tobytes())
	frame = vid.read()

vid.stop()
proc.stdin.close()
proc.wait()
osr2mp4.cleanup()
