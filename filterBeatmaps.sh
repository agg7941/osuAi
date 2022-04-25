#!/bin/sh

SONG_DIR=songs2
BEATMAP_DIR=beatmaps
WD=`pwd`

while read lst
do
	cd "$WD/$SONG_DIR/$lst"
	osuf=`ls -1 | grep osu | grep -i insane | tail -1`
	if [ -z "$osuf" ]; then
		osuf=`ls -1 | grep osu | tail -1`
	fi
	if [ ! -z "$osuf" ]; then
		if [[ `cat "$osuf" | grep Mode | awk '{print $2}' | tr -d '\r'` -eq 0 ]]; then
			if [ -z "$(ls -1 | grep mp3)" ]; then
				continue
			fi
			audio=`cat "$osuf" | grep -Po '(?<=AudioFilename: ).*' | tr -d '\r'`
			mkdir -p "$WD/$BEATMAP_DIR/$lst"
			cp "$osuf" "$WD/$BEATMAP_DIR/$lst/"
			cp "$audio" "$WD/$BEATMAP_DIR/$lst/"
			if [ $? -ne 0 ]; then
				echo "from: $lst"
				cp -v *.mp3 "$WD/$BEATMAP_DIR/$lst/"
			fi
		fi
	else
		echo "skipping $lst"
	fi
done <<< "$(cd $SONG_DIR; ls -d1 */)"
