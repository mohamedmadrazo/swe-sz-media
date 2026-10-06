#!/bin/bash
# Lanza en segundo plano el rodaje de la version 30 s (v1_tokyo_30s.blend -> renders_shoot30/, 540x960, 12 samples).
# Log: renders_shoot30.log ([START]/[FRAME]/[DONE]/[EXIT]). Por defecto frames 0-720; los args extra se pasan a render_shoot.py
# y pisan los valores por defecto (el ultimo --start/--end gana).
# usage: bash launch_shoot30.sh [--start 264 --end 640] [--skip-existing] [--samples N]
cd "$(dirname "$0")"
for p in $(pgrep -f "^python3 render_shoot.py"); do kill "$p" 2>/dev/null; done
sleep 1
nohup bash -c "timeout 7200 python3 render_shoot.py --blend v1_tokyo_30s.blend --out renders_shoot30 --start 0 --end 720 $* > renders_shoot30.log 2>&1; echo \"[EXIT \$?]\" >> renders_shoot30.log" >/dev/null 2>&1 &
echo "shoot30 launched (args: --start 0 --end 720 $*) -> renders_shoot30/, log renders_shoot30.log"
