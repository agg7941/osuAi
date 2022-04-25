from osr2mp4 import logger
from osr2mp4.EEnum.EReplay import Replays


def nearer(cur_time, replay_info, index):
	replay = replay_info.play_data
	x = index
	keys = []
	while x < len(replay) and replay[x][Replays.TIMES] <= cur_time:
		x += 1
		if replay[x-1][Replays.KEYS_PRESSED] != replay[x][Replays.KEYS_PRESSED]:
			keys.append(replay[x][Replays.KEYS_PRESSED])

	if not keys and replay[max(0, x-1)][Replays.KEYS_PRESSED] != 0:
		keys.append(replay[max(0, x-1)][Replays.KEYS_PRESSED])

	return x - index, keys


def find_followp_target(beatmap, frame_info):
	# reminder: index means the previous circle. the followpoints will point to the circle of index+1

	index = frame_info.index_fp

	while "spinner" in beatmap.hitobjects[index + 1]["type"] or "new combo" in beatmap.hitobjects[index + 1]["type"]:
		index += 1

	if "end" in beatmap.hitobjects[index + 1]["type"]:
		frame_info.x_end = 0
		frame_info.y_end = 0

		frame_info.obj_endtime = beatmap.hitobjects[index]["end time"] * 10
		frame_info.index_fp = index * 10
		return index * 10, beatmap.hitobjects[index]["end time"] * 10, 0, 0

	osu_d = beatmap.hitobjects[index]
	frame_info.x_end = osu_d["end x"]
	frame_info.y_end = osu_d["end y"]

	frame_info.obj_endtime = osu_d["end time"]
	frame_info.index_fp = index


def new_keys(n):
	k1 = n & 5 == 5
	k2 = n & 10 == 10
	m1 = not k1 and n & 1 == 1
	m2 = not k2 and n & 2 == 2
	smoke = n & 16 == 16
	return k1, k2, m1, m2  # fuck smoke


def check_key(component, cur_key, curtime, in_break):
	if in_break:
		return

	k1, k2, m1, m2 = new_keys(cur_key)
	if k1:
		component.key1.clicked(curtime)
	if k2:
		component.key2.clicked(curtime)
	if m1:
		component.mouse1.clicked(curtime)
	if m2:
		component.mouse2.clicked(curtime)


def add_hitobjects(beatmap, component, frame_info, time_preempt, settings):
	osu_d = beatmap.hitobjects[frame_info.index_hitobj]
	x_circle = int(osu_d["x"] * settings.playfieldscale) + settings.moveright
	y_circle = int(osu_d["y"] * settings.playfieldscale) + settings.movedown
	# check if it's time to draw circles
	if frame_info.cur_time + time_preempt >= osu_d["time"] and frame_info.index_hitobj + 1 < len(beatmap.hitobjects):

		# logger.log(1, "Adding osu object {}\n{}".format(osu_d, frame_info))

		if "spinner" in osu_d["type"]:

			if frame_info.cur_time + 400 > osu_d["time"]:
				component.hitobjmanager.add_spinner(osu_d, frame_info.cur_time)
				frame_info.index_hitobj += 1

		else:

			component.hitobjmanager.add_circle(osu_d, x_circle, y_circle, frame_info.cur_time)

			if "slider" in osu_d["type"]:
				component.hitobjmanager.add_slider(osu_d, x_circle, y_circle, frame_info.cur_time)

			frame_info.index_hitobj += 1


def add_followpoints(beatmap, component, frame_info, preempt_followpoint):
	# check if it's time to draw followpoints
	if frame_info.cur_time + preempt_followpoint >= frame_info.obj_endtime and frame_info.index_fp + 2 < len(
			beatmap.hitobjects):
		frame_info.index_fp += 1
		if "new combo" not in beatmap.hitobjects[frame_info.index_fp]["type"]:
			component.followpoints.add_fp(frame_info.x_end, frame_info.y_end, frame_info.obj_endtime,
			                              beatmap.hitobjects[frame_info.index_fp])

		find_followp_target(beatmap, frame_info)


def check_break(beatmap, component, frame_info, updater, settings):
	breakperiod = beatmap.breakperiods[frame_info.break_index]
	next_break = frame_info.cur_time > breakperiod["End"]
	if next_break:
		frame_info.break_index = min(frame_info.break_index + 1, len(beatmap.breakperiods) - 1)
		# component.background.startbreak(beatmap.breakperiods[frame_info.break_index], frame_info.cur_time)
		breakperiod = beatmap.breakperiods[frame_info.break_index]

	in_break = int(frame_info.cur_time) in range(breakperiod["Start"], breakperiod["End"])

	half = breakperiod["Start"] + (breakperiod["End"] - breakperiod["Start"]) / 2

	if in_break:
		duration = (breakperiod["End"] - frame_info.cur_time) / settings.timeframe * 1000
		component.scorebarbg.startbreak(breakperiod, duration)
		component.background.startbreak(breakperiod, duration)
		component.combocounter.startbreak(breakperiod, duration)
		component.urbar.startbreak(breakperiod, duration)
		component.flashlight.startbreak(breakperiod, duration)

		endgamebreak = frame_info.break_index == len(beatmap.breakperiods) - 1
		if not endgamebreak:
			component.playinggrade.startbreak(breakperiod)

	if frame_info.cur_time > breakperiod["End"] - 700 and in_break and breakperiod["Arrow"]:
		component.arrowwarning.startbreak(breakperiod["Start"])

	return in_break
