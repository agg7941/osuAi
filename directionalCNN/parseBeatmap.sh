#!/bin/bash

osud="$1"
osuf="$2"
dataset="$3"
anno="$4"

b=0
e=0
s=a
while read ln; do
	if [ $s == 'a' ]; then
		if [[ -z `echo $ln | grep AudioFilename` ]]; then
			continue
		fi
		auf=`echo $ln | grep -Po '(?<=AudioFilename: ).*' | tr -d '\r'`
		s=i
		continue
	elif [ $s == 'i' ]; then
		if [[ -z `echo $ln | grep BeatmapSetID` ]]; then
			continue
		fi
		id=`echo $ln | grep -Po '(?<=BeatmapSetID:).*' | tr -d '\r'`
		s=t
		continue
	elif [ $s == 't' ]; then
		if [[ -z `echo $ln | grep TimingPoints` ]]; then
			continue
		fi
		s=f
		t=0
		continue
	fi

	if [[ -z `echo $ln | tr -d '\r'` ]]; then
		break
	fi

	echo $ln
	if [ $s == 'f' ]; then
		t=`echo $ln | awk -F ',' '{print $2}'`
		s=s
		continue
	elif [ $s == 's' ]; then
		n=`echo $ln | awk -F ',' '{print $2}'`
		if [[ 1 -eq `echo "$n > 0" | bc` ]]; then
			echo "$t > $anno/$id-$b.bpm"
			echo $t > "$anno/$id-$b.bpm"
			t=$n
		else
			continue
		fi
		e=`echo $ln | awk -F ',' '{print $1}'`
		echo "ffmpeg -i $osud/$auf -ss ${b}ms -to ${e}ms -c:a copy $dataset/$id-$b.mp3"
		$(ffmpeg -y -i "$osud/$auf" -ss "${b}ms" -to "${e}ms" -c:a copy "$dataset/$id-$b.mp3")
		b=$e
	fi
done <<< "$(cat "$osuf")"

echo "$t > $anno/$id-$b.bpm"
echo $t > "$anno/$id-$b.bpm"
echo "ffmpeg -i $osud/$auf -ss ${b}ms -c:a copy $dataset/$id-$b.mp3"
$(ffmpeg -y -i "$osud/$auf" -ss "${b}ms" -c:a copy "$dataset/$id-$b.mp3")
