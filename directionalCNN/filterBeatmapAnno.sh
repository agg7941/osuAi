#!/bin/sh

NUM=$1
OFFSET=$2
IN=`cat $3`
OUT="$4"

rm $OUT
echo "$IN" | while read ln; do
	bpm=`echo "$ln" | awk '{print $2}'`
	bpm=`echo "($bpm+0.5)/1" | bc`
	high=$((NUM+OFFSET))
	if [ `echo "$bpm < $high && $bpm > $OFFSET" | bc` -eq 1 ]; then
		echo "$(echo "$ln" | awk '{print $1}')\t$bpm\tX\tX"
		echo "$(echo "$ln" | awk '{print $1}')\t$bpm\tX\tX" >> "$OUT"
	fi
done
