#!/bin/bash
# Lanza en segundo plano el rodaje S5-S6 (frames 204-360, 540x960, 12 samples). Log: renders_shoot.log ([FRAME]/[DONE]/[EXIT])
# usage: bash launch_shoot.sh [extra args para render_shoot.py, p.ej. --skip-existing]
cd "$(dirname "$0")"
for p in $(pgrep -f "^python3 render_shoot.py"); do kill "$p" 2>/dev/null; done
sleep 1
nohup bash -c "timeout 7000 python3 render_shoot.py $* > renders_shoot.log 2>&1; echo \"[EXIT \$?]\" >> renders_shoot.log" >/dev/null 2>&1 &
echo "shoot launched (frames 204-360 -> renders_shoot/, log renders_shoot.log)"
