#!/bin/sh

ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 $1
