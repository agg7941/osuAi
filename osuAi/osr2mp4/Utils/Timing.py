from osr2mp4 import logger
from osr2mp4.VideoProcess.calc import nearer
from osr2mp4.CheckSystem.Judgement import DiffCalculator
from osr2mp4.EEnum.EReplay import Replays
from osr2mp4.Utils.skip import search_time, search_osrindex


def get_offset(beatmap, start_index, end_index, replay_info, endtime, fps=60):
	replay_event = replay_info.play_data
	if endtime == -1:
		endtime = 5000
	else:
		endtime = 0
	start_time = replay_event[start_index][3]
	diffcalculator = DiffCalculator(beatmap.diff)
	timepreempt = diffcalculator.ar()

	# same as skip() code
	hitobjectindex = search_time(start_time, beatmap.hitobjects)
	to_time = min(beatmap.hitobjects[hitobjectindex]["time"] - timepreempt, start_time)
	osr_index = search_osrindex(to_time, replay_event)
	old = osr_index
	# simulate video draw code
	curtime = replay_event[osr_index][Replays.TIMES]
	interval = 1000/fps
	while osr_index < start_index:
		curtime += interval
		tt, _ = nearer(curtime, replay_info, osr_index)
		osr_index += tt
	osr_index = max(0, osr_index-1)

	offset = replay_event[osr_index][Replays.TIMES]
	endtime += replay_event[end_index][Replays.TIMES] + 100
	logger.debug("\n\nOFFSET: %s", offset)
	return offset, endtime


def find_time(starttime, endtime, replay, settings):

	starttime *= settings.timeframe
	starttime += replay[0][Replays.TIMES]
	starttime = min(starttime, replay[-15][Replays.TIMES])

	if endtime != -1:
		endtime *= settings.timeframe
		# endtime += replay_start
		endtime += replay[0][Replays.TIMES]

		endtime = max(endtime, starttime - 900)

	startindex = None

	if starttime == 0:
		startindex = 0

	endindex = len(replay) - 3
	if endtime == -1:
		endindex = len(replay) - 3

	for index, x in enumerate(replay[:-3]):
		if x[3] >= starttime and startindex is None:
			startindex = index
		if x[3] >= endtime + 1000 and endtime != -1:
			endindex = index
			break
	return startindex, endindex
