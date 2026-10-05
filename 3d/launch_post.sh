#!/bin/bash
# Lanza en segundo plano turntable + previz animada (secuencial). Logs: renders_turntable.log / renders_anim.log
cd "$(dirname "$0")"
nohup bash -c "timeout 3000 python3 render_turntable.py > renders_turntable.log 2>&1; echo \"[EXIT \$?]\" >> renders_turntable.log; timeout 3000 python3 render_previz_anim.py > renders_anim.log 2>&1; echo \"[EXIT \$?]\" >> renders_anim.log" >/dev/null 2>&1 &
echo "post renders launched"
