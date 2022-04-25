#!/bin/sh

ls -1 segments | awk '{print "file " "\047" "segments/" $0 "\047"}' > list
