import sys
from osr2mp4.osr2mp4 import Osr2mp4

def create_vid(data_json):
	osr2mp4 = Osr2mp4(filedata=data_json, filesettings='settings.json', filepp='ppsettings.json', filestrain='strainsettings.json', logtofile=True)
	osr2mp4.startaudio()
	osr2mp4.startvideo()
	osr2mp4.cleanup()

if __name__ == '__main__':
	create_vid(sys.argv[1])
