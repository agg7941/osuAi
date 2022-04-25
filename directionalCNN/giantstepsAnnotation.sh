#!/bin/sh

BPM=giantsteps-tempo-dataset/annotations_v2/tempo

flst=`ls -1 $BPM`

:> "$BPM/tempo.tsv"
while read lst; do
	name=`echo $lst | grep -Po '.*(?=.LOFI.bpm)'`
	bpm=`cat "$BPM/$lst"`
	echo -e "$name\t$bpm\tX\tX" >> "$BPM/tempo.tsv"
done <<< "$flst"
