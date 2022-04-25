import os

from osr2mp4 import logger
from osr2mp4.ImageProcess.PrepareFrames.Scores.URArrow import prepare_urarrow
from osr2mp4.ImageProcess.Objects.Components.Flashlight import Flashlight
from osr2mp4.ImageProcess.PrepareFrames.Components.Flashlight import prepare_flashlight
from osr2mp4.ImageProcess.Objects.Components.PlayingModIcons import PlayingModIcons
from osr2mp4.osrparse.enums import Mod

from osr2mp4.ImageProcess.Objects.Scores.PPCounter import PPCounter
from osr2mp4.ImageProcess.Objects.Scores.StrainGraph import StrainGraph
from osr2mp4.ImageProcess.PrepareFrames.Components.PlayingGrade import prepare_playinggrade
from osr2mp4.ImageProcess.Objects.Components.PlayingGrade import PlayingGrade
from osr2mp4.CheckSystem.Judgement import DiffCalculator
from osr2mp4.ImageProcess.Objects.Components.ArrowWarning import ArrowWarning
from osr2mp4.ImageProcess.Objects.Components.Background import Background
from osr2mp4.ImageProcess.Objects.Components.ScorebarBG import ScorebarBG
from osr2mp4.ImageProcess.Objects.Scores.ScoreNumbers import ScoreNumbers
from osr2mp4.ImageProcess.Objects.Components.Followpoints import FollowPointsManager
from osr2mp4.ImageProcess.Objects.Components.TimePie import TimePie
from osr2mp4.ImageProcess.Objects.HitObjects.CircleNumber import Number
from osr2mp4.ImageProcess.Objects.HitObjects.Slider import SliderManager
from osr2mp4.ImageProcess.Objects.HitObjects.Spinner import SpinnerManager
from osr2mp4.ImageProcess.Objects.Scores.Accuracy import Accuracy
from osr2mp4.ImageProcess.Objects.Scores.ComboCounter import ComboCounter
from osr2mp4.ImageProcess.Objects.Scores.Hitresult import HitResult
from osr2mp4.ImageProcess.Objects.Scores.ScoreCounter import ScoreCounter
from osr2mp4.ImageProcess.Objects.HitObjects.Circles import CircleManager
from osr2mp4.ImageProcess.Objects.HitObjects.Manager import HitObjectManager
from osr2mp4.ImageProcess.Objects.Components.Button import InputOverlay, InputOverlayBG, ScoreEntry
from osr2mp4.ImageProcess.Objects.Components.Cursor import Cursor, Cursortrail
from osr2mp4.ImageProcess.Objects.Scores.SpinBonusScore import SpinBonusScore
from osr2mp4.ImageProcess.Objects.Scores.URBar import URBar
from osr2mp4.ImageProcess.PrepareFrames.Components.ArrowWarning import prepare_arrowwarning
from osr2mp4.ImageProcess.PrepareFrames.Components.Button import prepare_scoreentry, prepare_inputoverlaybg, \
	prepare_inputoverlay
from osr2mp4.ImageProcess.PrepareFrames.Components.Cursor import prepare_cursor, prepare_cursortrail, prepare_cursormiddle
from osr2mp4.ImageProcess.PrepareFrames.Components.Followpoints import prepare_fpmanager
from osr2mp4.ImageProcess.PrepareFrames.Components.Background import prepare_background
from osr2mp4.ImageProcess.PrepareFrames.RankingScreens.ModIcons import prepare_modicons
from osr2mp4.ImageProcess.PrepareFrames.Components.ScorebarBG import prepare_scorebarbg
from osr2mp4.ImageProcess.PrepareFrames.HitObjects.CircleNumber import prepare_hitcirclenumber
from osr2mp4.ImageProcess.PrepareFrames.HitObjects.Circles import prepare_circle, calculate_ar
from osr2mp4.ImageProcess.PrepareFrames.HitObjects.Slider import prepare_slider
from osr2mp4.ImageProcess.PrepareFrames.HitObjects.Spinner import prepare_spinner
from osr2mp4.ImageProcess.PrepareFrames.Scores.Accuracy import prepare_accuracy
from osr2mp4.ImageProcess.PrepareFrames.Scores.ComboCounter import prepare_combo
from osr2mp4.ImageProcess.PrepareFrames.Scores.Hitresult import prepare_hitresults
from osr2mp4.ImageProcess.PrepareFrames.Scores.ScoreCounter import prepare_scorecounter
from osr2mp4.ImageProcess.PrepareFrames.Scores.SpinBonusScore import prepare_spinbonus
from osr2mp4.ImageProcess.PrepareFrames.Scores.URBar import prepare_bar
from osr2mp4.ImageProcess.PrepareFrames.Scores.PPCounter import prepare_pp_counter
from osr2mp4.ImageProcess.Objects.Scores.HitresultCounter import HitresultCounter

class PreparedFrames:
	def __init__(self, settings, diff, mod_combination, ur=None, bg=None, beatmap=None):
		skin = settings.skin_ini
		check = DiffCalculator(diff)
		hd = Mod.Hidden in mod_combination
		fl = Mod.Flashlight in mod_combination
		if settings.settings["Automatic cursor size"]:
			circlescale = 4/diff["CircleSize"]
			settings.settings["Cursor size"] *= circlescale
		if ur is None:
			ur = [0, 0, 0]
		if bg is None:
			bg = [0, 0, ""]

		logger.debug('start preparing cursor')
		self.cursor, default = prepare_cursor(settings.scale * settings.settings["Cursor size"], settings)
		logger.debug('start preparing cursormiddle')
		self.cursormiddle, self.continuous = prepare_cursormiddle(settings.scale * settings.settings["Cursor size"], settings, default)
		logger.debug('start preparing cursortrail')
		self.cursor_trail = prepare_cursortrail(settings.scale * settings.settings["Cursor size"], self.continuous, settings)

		logger.debug('start preparing scoreentry')
		self.scoreentry = prepare_scoreentry(settings.scale, skin.colours["InputOverlayText"], settings)
		self.inputoverlayBG = prepare_inputoverlaybg(settings.scale, settings)
		self.key = prepare_inputoverlay(settings.scale, [255, 220, 20], 2, settings)
		self.mouse = prepare_inputoverlay(settings.scale, [220, 0, 220], 1, settings)

		logger.debug('start preparing scorenumber')
		self.scorenumbers = ScoreNumbers(settings.scale, settings)
		self.hitcirclenumber = prepare_hitcirclenumber(diff, settings.playfieldscale, settings)

		logger.debug('start preparing accuracy')
		self.accuracy = prepare_accuracy(self.scorenumbers)
		self.combocounter = prepare_combo(self.scorenumbers, settings)
		self.hitresult = prepare_hitresults(settings.scale, diff, settings)
		self.spinbonus = prepare_spinbonus(self.scorenumbers)
		self.scorecounter = prepare_scorecounter(self.scorenumbers)

		self.playinggrade = prepare_playinggrade(settings.scale * 0.75, settings)

		self.urbar = prepare_bar(settings.scale * settings.settings["Score meter size"], check.scorewindow)

		self.fpmanager = prepare_fpmanager(settings.playfieldscale, settings)

		logger.debug('start preparing circle')
		self.circle = prepare_circle(diff, settings.playfieldscale, settings, hd)
		self.slider = prepare_slider(diff, settings.playfieldscale, settings)
		self.spinner = prepare_spinner(settings.playfieldscale, settings)

		logger.debug('start preparing background')
		self.bg = prepare_background(os.path.join(settings.beatmap, bg[2]), settings)

		logger.debug('start preparing sections')
		self.scorebarbg = prepare_scorebarbg(settings.scale, self.bg, settings)
		self.arrowwarning = prepare_arrowwarning(settings.scale, settings)

		self.modicons = prepare_modicons(settings.scale, settings)

		self.flashlight = prepare_flashlight(settings, fl)
		self.urarrow = prepare_urarrow(settings)

		self.pp_counter_custom = prepare_pp_counter(settings, os.path.join(settings.beatmap, bg[2]), beatmap)
		logger.debug('start preparing done')


class FrameObjects:
	def __init__(self, frames, settings, diff, replay_info, meta, maphash, map_time):
		opacity_interval, timepreempt, _ = calculate_ar(diff["ApproachRate"], settings)
		check = DiffCalculator(diff)
		rankinggap = 0
		skin = settings.skin_ini
		hd = Mod.Hidden in replay_info.mod_combination
		hasfl = Mod.Flashlight in replay_info.mod_combination

		self.cursormiddle = Cursor(frames.cursormiddle)
		self.cursor = Cursor(frames.cursor)
		self.cursor_trail = Cursortrail(frames.cursor_trail, frames.continuous, settings)

		self.scoreentry = ScoreEntry(frames.scoreentry, settings)

		self.inputoverlayBG = InputOverlayBG(frames.inputoverlayBG, settings=settings)
		self.key1 = InputOverlay(frames.key, self.scoreentry, settings)
		self.key2 = InputOverlay(frames.key, self.scoreentry, settings)
		self.mouse1 = InputOverlay(frames.mouse, self.scoreentry, settings)
		self.mouse2 = InputOverlay(frames.mouse, self.scoreentry, settings)
		self.playingmodicons = PlayingModIcons(frames.modicons, replay_info, settings)

		self.accuracy = Accuracy(frames.accuracy, skin.fonts["ScoreOverlap"], settings)
		self.timepie = TimePie(self.accuracy, map_time[0], map_time[1], frames.scorebarbg, settings)
		self.playinggrade = PlayingGrade(frames.playinggrade, self.timepie, replay_info, settings)
		self.hitresult = HitResult(frames.hitresult, settings, replay_info.mod_combination)
		self.spinbonus = SpinBonusScore(frames.spinbonus, skin.fonts["ScoreOverlap"], settings)
		self.combocounter = ComboCounter(frames.combocounter, skin.fonts["ScoreOverlap"], settings)
		self.scorecounter = ScoreCounter(frames.scorecounter, diff, skin.fonts["ScoreOverlap"], settings)

		self.urbar = URBar(frames.urbar, frames.urarrow, settings)

		self.followpoints = FollowPointsManager(frames.fpmanager, settings)

		self.hitcirclenumber = Number(frames.hitcirclenumber, skin.fonts)
		self.circle = CircleManager(frames.circle, timepreempt, self.hitcirclenumber, settings)
		self.slider = SliderManager(frames.slider, diff, settings, hd)
		self.spinner = SpinnerManager((frames.spinner, frames.scorecounter), settings, check)
		self.hitobjmanager = HitObjectManager(self.circle, self.slider, self.spinner, check.scorewindow[2], settings)

		self.background = Background(frames.bg, map_time[0] - timepreempt, settings, hasfl)
		self.scorebarbg = ScorebarBG(frames.scorebarbg, map_time[0] - timepreempt, settings, hasfl)
		self.arrowwarning = ArrowWarning(frames.arrowwarning, settings)

		self.ppcounter = PPCounter(settings, custom_counter = frames.pp_counter_custom)
		self.hitresultcounter = HitresultCounter(settings)
		self.flashlight = Flashlight(frames.flashlight, settings, hasfl)
		self.strain_graph = StrainGraph(settings, map_time[0], map_time[1])
