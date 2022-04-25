#!/bin/bash

BEATMAPS=../beatmaps
WD=`pwd`
DATASET=$WD/osuDS
ANNOTATIONS=$WD/osuAnno
cmd='sh /home/poi/proj/osuAi/directionalCNN/parseBeatmap.sh'

cd $BEATMAPS
ls -d1 */ | while read -r i; do
	echo "$i"
	cd "$WD/$BEATMAPS/$i"
	osuf=`ls -1 | grep osu`
	echo $osuf
	echo "sh parseBeatmap.sh . $osuf $DATASET $ANNOTATIONS"
	$cmd "./" "$osuf" "$DATASET" "$ANNOTATIONS"
done
