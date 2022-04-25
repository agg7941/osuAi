import Resolution

h = 600
w = 1024

H = 480
W = 640

s = 1.0

playfield_scale = 0.
move_right = 0.
move_down = 0.

def calratio():
	global playfield_scale, move_right, move_down
	playfield_scale, playfield_width, playfield_height, scale, move_right, move_down = Resolution.get_screensize(w, h)

def cor(x, y):
	j = int(x * playfield_scale) + move_right
	k = int(y * playfield_scale) + move_down
	return j, k
