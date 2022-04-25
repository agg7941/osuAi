from recordclass import recordclass

from osr2mp4.ImageProcess import imageproc
from osr2mp4.ImageProcess.Objects.FrameObject import FrameObject

spinnercircle = "spinner-circle"
spinnerbackground = "spinner-background"
spinnerbottom = "spinner-bottom"
spinnerspin = "spinner-spin"
spinnermetre = "spinner-metre"
spinnerapproachcircle = "spinner-approachcircle"
spinnertop = "spinner-top"
spinnerrpm = "spinner-rpm"


Spinner = recordclass("Spinner", "angle duration starttime_left alpha index rpm")


class SpinnerManager(FrameObject):
	def __init__(self, frames, settings, check):
		super().__init__(frames[0], settings=settings)

		self.moveright = self.settings.moveright
		self.movedown = self.settings.movedown
		self.scale = self.settings.playfieldscale
		self.width = self.settings.playfieldwidth
		self.height = self.settings.playfieldheight
		self.spinners = {}

		self.interval = self.settings.timeframe / self.settings.fps
		self.timer = 0

		self.scoreframes = frames[1]
		self.check = check

	def add_spinner(self, osu_d, curtime):
		starttime = osu_d["time"]
		endtime = osu_d["end time"]
		idd = str(osu_d["id"]) + "o"
		duration = endtime - starttime
		# img, duration, startime left, alpha, index, progress
		self.spinners[idd] = Spinner(0, duration, starttime - curtime, 0, 0, 0)

	def update_spinner(self, idd, angle, progress, rpm):
		self.spinners[idd].angle = angle

		progress = progress * 10
		if 0.3 < progress - int(progress) < 0.35 or 0.6 < progress - int(progress) < 0.65:
			progress -= 1

		self.spinners[idd].index = min(10, int(progress))
		self.spinners[idd].rpm = rpm

	def drawrpm(self, background, x_offset, y_offset, number, alpha):
		number = str(number)[::-1]
		x_start = x_offset
		for digit in number:
			digit = int(digit)
			imageproc.add(self.scoreframes[digit], background, x_start, y_offset, alpha=alpha)
			x_start -= self.scoreframes[digit].size[0]

	def add_to_frame(self, background, i, _):
		if self.spinners[i].starttime_left > 0:
			self.spinners[i].starttime_left -= self.interval
			self.spinners[i].alpha = min(1, self.spinners[i].alpha + self.interval / 400)
		else:
			self.spinners[i].duration -= self.interval
			if 0 > self.spinners[i].duration > -200:
				self.spinners[i].alpha = max(0, self.spinners[i].alpha - self.interval / 200)
			else:
				self.spinners[i].alpha = 1
		img = self.frames[spinnerbackground]
		imageproc.add(img, background, self.width/2 + self.moveright, self.height/2 + self.movedown, alpha=self.spinners[i].alpha)

		img = self.frames[spinnercircle].rotate(self.spinners[i].angle)
		imageproc.add(img, background, self.width/2 + self.moveright, self.height/2 + self.movedown, alpha=self.spinners[i].alpha)

		height = self.frames[spinnermetre].size[1]
		y_start = height - self.spinners[i].index * height // 10
		width = self.frames[spinnermetre].size[0]
		img = self.frames[spinnermetre].crop((0, y_start, width, height))

		x = self.width/2 + self.moveright - width/2
		y = 46/768 * self.height + y_start
		imageproc.add(img, background, x, y, alpha=self.spinners[i].alpha, topleft=True)

		img = self.frames[spinnerrpm]
		x = self.settings.width/2 - 139 * self.settings.scale
		y = 712/768 * self.settings.height
		imageproc.add(img, background, x, y, alpha=self.spinners[i].alpha, topleft=True)

		rpm = int(self.spinners[i].rpm)
		self.drawrpm(background, x + 250 * self.settings.scale, y + 25 * self.settings.scale, rpm, self.spinners[i].alpha)

