from osr2mp4.ImageProcess.Animation.easing import easingout
from osr2mp4.ImageProcess.Objects.FrameObject import FrameObject


class ScoreCounter(FrameObject):
	def __init__(self, frames, diff, gap, settings):
		super().__init__(frames, settings=settings)
		self.freeze = 0
		self.showscore = 0
		self.score = 0
		self.diff = diff
		self.width = self.settings.width
		self.height = self.settings.height
		self.gap = int(gap * self.settings.scale * 0.75)

	def set_score(self, freeze, score, showscore):
		"""
		:param freeze:
		:param score:
		:param showscore:
		:return:
		"""
		self.freeze = freeze
		self.score = score
		self.showscore = showscore

	def update_score(self, score):
		self.score = score

	def bonus_score(self, score):
		self.score += score
		self.showscore += score

	def draw_score(self, score_string, background):
		x = self.width - (-self.gap + self.frames[0].size[0]) * len(score_string)
		y = self.frames[0].size[1] // 2
		for digit in score_string:
			self.frame_index = int(digit)
			super().add_to_frame(background, x, y)
			x += -self.gap + self.frames[0].size[0]

	def add_to_frame(self, background, cur_time, inbreak):
		if not self.settings.settings["In-game interface"]:
			return

		score_string = str(int(self.showscore))
		score_string = "0" * (8 - len(score_string)) + score_string
		if self.settings.settings["In-game interface"] or inbreak:
			self.draw_score(score_string, background)

		current = self.settings.timeframe/self.settings.fps
		change = self.score - self.showscore
		duration = 500
		self.showscore = easingout(current, self.showscore, change, duration)
