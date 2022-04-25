from osr2mp4.Utils.Auto import get_auto
from osr2mp4.Parser.osuparser import read_file
from osr2mp4.Utils.getmods import mod_string_to_enums
from osr2mp4.Parser.jsonparser import read
from osr2mp4.Utils.Setup import setupglobals
from osr2mp4.global_var import Settings, defaultsettings, defaultppconfig, defaultstrainconfig
import pickle

data = read('data.json')

gameplaysettings = defaultsettings
ppsettings = defaultppconfig
strainsettings = defaultstrainconfig

gameplaysettings["Custom mods"] = gameplaysettings.get("Custom mods", "")
mod_combination = mod_string_to_enums(gameplaysettings["Custom mods"])
settings = Settings()
settings.path = './'
setupglobals(data, gameplaysettings, mod_combination, settings, ppsettings=ppsettings, strainsettings=strainsettings)

beatmap = read_file(settings.beatmap, settings.playfieldscale, settings.skin_ini.colours, mods=mod_combination, lazy=False)
replay_info = get_auto(beatmap)

with open('orig.rp', 'wb') as f:
	pickle.dump(replay_info.play_data, f)
