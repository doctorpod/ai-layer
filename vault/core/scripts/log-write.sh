#!/bin/bash

PATH="_AI/logs"
TODAYS_LOG="$PATH/log-$(/bin/date +%Y-%m-%d).md"
NOW=$(/bin/date +"%H:%M:%S")

/usr/bin/touch "$TODAYS_LOG"
echo "$NOW: $@" >> "$TODAYS_LOG"
