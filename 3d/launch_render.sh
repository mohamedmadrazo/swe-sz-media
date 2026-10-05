#!/bin/bash
# usage: bash launch_render.sh "<frames>" <samples>   (kills a previous render of the same script, then runs in background)
cd "$(dirname "$0")"
for p in $(pgrep -f "^python3 build_v1_scene.py"); do kill "$p" 2>/dev/null; done
sleep 1
nohup bash -c "timeout 3000 python3 build_v1_scene.py --frames $1 --samples $2 > renders/render.log 2>&1; echo \"[EXIT \$?]\" >> renders/render.log" >/dev/null 2>&1 &
echo "render launched (frames $1, samples $2)"
