#!/bin/sh

ffmpeg -f concat -i list -c copy concat.wav
