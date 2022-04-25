import os
import cv2
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

osr2mp4 = Osr2mp4(filedata='data.json', filesettings='settings.json', filepp='ppsettings.json', filestrain='strainsettings.json')

osr2mp4.startaudio()
osr2mp4.startvideo()

fps = 50
sr = 1/fps * 1000

alpha = cv2.imread('cursor.png', cv2.IMREAD_UNCHANGED)[:,:,3] / 255.0
alpha = alpha.reshape((alpha.shape[0], alpha.shape[1], 1))
alpha = (alpha, 1-alpha)
cursor = cv2.imread('cursor.png')

cmd = ['ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-r', str(fps), '-s', '{}x{}'.format(op.w, op.h), 
  '-i', '-', '-y', '-c:v', 'libx264', '-crf', '18', 'video.mp4']
proc = sp.Popen(cmd, stdin=sp.PIPE)

vid = FileVideoStream('vid.mp4').start()
frame = vid.read()
time = 0.0
i = 0
offset = osr2mp4.replay_info.play_data[0][Replays.TIMES]
while True:
	e = osr2mp4.replay_info.play_data[i]
	delta = abs(e[Replays.TIMES] - time - offset)
	if delta <= sr:
		frame = addPoint(e[Replays.CURSOR_X], e[Replays.CURSOR_Y], cursor, alpha, frame)
		i += 1
		continue

	proc.stdin.write(frame.tobytes())

	time += sr
	frame = vid.read()

vid.stop()
proc.stdin.close()
proc.wait()
osr2mp4.cleanup()
