import os

import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError
from osr2mp4 import logger
from osr2mp4.EEnum.EImageFrom import ImageFrom
from osr2mp4.ImageProcess import imageproc


oldimg = Image.open
def newimg(fp, mode: str = "r"):
	try:
		return oldimg(fp, mode)
	except UnidentifiedImageError:
		a = cv2.imread(fp, -1)
		# cv2.imwrite("temp.png", a)
		# r = oldimg("temp.png", mode)
		# os.remove("temp.png")
		a = cv2.cvtColor(a, cv2.COLOR_RGBA2BGRA)
		r = Image.fromarray(a)
		return r
Image.open = newimg


class YImage:
	def __init__(self, filename, settings, scale=1, rotate=0, defaultpath=False, prefix="", fallback=None, scaley=None, defaultfallback=True):
		self.filename = filename
		self.origfile = filename
		self.x2 = False
		self.imgfrom = None

		self.settings = settings
		self.defaultfallback = defaultfallback

		self.loadimg(defaultpath, prefix, fallback)

		if rotate:
			self.tosquare()

		if scaley is None:
			scaley = scale

		if self.x2:
			# logger.debug(self.filename)
			scale /= 2
			scaley /= 2

		self.orig_img = self.img.copy()
		self.orig_rows = self.img.size[1]
		self.orig_cols = self.img.size[0]
		if scale != 1:
			self.change_size(scale, scaley)
			self.orig_img = self.img.copy()
			self.orig_rows = self.img.size[1]
			self.orig_cols = self.img.size[0]

		# logger.debug(filename)

	def loadx2(self, path, pre, filename=None):
		if filename is None:
			filename = self.filename
		try:
			p = os.path.join(path, pre + filename + self.settings.x2 + self.settings.format)
			self.img = Image.open(p).convert("RGBA")
			self.filename = p
			self.x2 = True
			return True
		except FileNotFoundError as er:
			try:
				p = os.path.join(path, pre + filename + self.settings.format)
				self.img = Image.open(p).convert("RGBA")
				self.filename = p
				return True
			except FileNotFoundError as e:
				return False

	def loadimg(self, defaultpath, prefix, fallback):
		pre = self.settings.skin_ini.fonts.get(prefix, "")
		default_pre = self.settings.default_skin_ini.fonts.get(prefix, "")

		if defaultpath:
			path = self.settings.default_path
		else:
			path = self.settings.skin_path

		if self.loadx2(path, pre):
			if defaultpath:
				self.imgfrom = ImageFrom.DEFAULT_X2 if self.x2 else ImageFrom.DEFAULT_X
			else:
				self.imgfrom = ImageFrom.SKIN_X2 if self.x2 else ImageFrom.SKIN_X
			return

		if fallback is not None:
			if self.loadx2(path, pre, fallback):
				self.imgfrom = ImageFrom.FALLBACK_X2 if self.x2 else ImageFrom.FALLBACK_X
				return
			self.filename = fallback

		if self.defaultfallback:
			if self.loadx2(self.settings.default_path, default_pre):
				self.imgfrom = ImageFrom.DEFAULT_X2 if self.x2 else ImageFrom.DEFAULT_X
				return

		self.filename = "None"
		self.img = Image.new("RGBA", (1, 1))
		self.imgfrom = ImageFrom.BLANK

	def tosquare(self):
		"""
		When the image needs rotation, it will be cropped. So we make the image box bigger.
		"""
		dim = int(np.sqrt(self.img.size[0]**2 + self.img.size[1]**2))
		square = Image.new("RGBA", (dim, dim))
		square.paste(self.img, ((dim - self.img.size[0])//2, (dim - self.img.size[1])//2))
		self.img = square

	def changealpha(self, alpha):
		imageproc.changealpha(self.img, alpha)

	def change_size(self, scale_row, scale_col):
		"""
		When using this method, the original image size will be used
		:param scale_row: float
		:param scale_col: float
		:return:
		"""
		self.img = imageproc.change_size(self.img, scale_row, scale_col, rows=self.orig_rows, cols=self.orig_cols)


class YImages:
	def __init__(self, filename, settings, scale=1, delimiter="", rotate=0):
		self.settings = settings
		self.filename = filename
		self.scale = scale
		self.delimiter = delimiter
		self.frames = []
		self.rotate = rotate
		self.n_frame = 0
		self.unanimate = False
		self.imgfrom = None

		self.load(defaultpath=False)
		if self.unanimate and self.imgfrom == ImageFrom.BLANK:
			logger.debug("Loading default path YImagesss: %s", filename)
			self.frames = []
			self.load(defaultpath=True)

	def load(self, defaultpath=False):
		counter = 0

		while True:
			img = YImage(self.filename + self.delimiter + str(counter), self.settings, scale=self.scale, rotate=self.rotate, defaultpath=defaultpath, defaultfallback=defaultpath)
			if img.imgfrom == ImageFrom.BLANK:
				break
			self.imgfrom = img.imgfrom
			self.frames.append(img.img)

			counter += 1

		if not self.frames:
			self.unanimate = True

			a = YImage(self.filename, self.settings, scale=self.scale, rotate=self.rotate, defaultpath=defaultpath, defaultfallback=defaultpath)
			self.imgfrom = a.imgfrom
			self.frames.append(a.img)

		self.n_frame = len(self.frames)
