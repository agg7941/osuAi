#!/bin/sh

DS="$1"
BPM="$2"
TSV="$3"

rm "$3"
flst=`ls -1 $BPM`

echo "$flst" | while read lst; do
	echo $lst

	bpm=`cat "$BPM/$lst"`

	name=`echo $lst | grep -Po '.*(?=.bpm)'`
	duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$DS/$name.mp3")

	if [ -z $duration ] || [ `echo "$duration < 10" | bc` -eq 1 ]; then
		continue
	fi
	echo "$name\t$bpm\tX\tX" >> "$TSV"
done
