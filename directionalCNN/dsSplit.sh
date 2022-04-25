#!/bin/sh

tsv=$1
train=0.6
val=0.2
test=0.2

c=`wc -l $tsv | awk '{print $1}'`
echo $c
head -`echo "$c*$train/1" | bc` $tsv > train.tsv
head -`echo "($c*$train + $c*$val)/1" | bc` $tsv | tail -`echo "$c*$val/1" | bc` > val.tsv
tail -`echo "$c*$val/1" | bc` $tsv > test.tsv
