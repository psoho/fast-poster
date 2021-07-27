#! /bin/bash
# desc: 入口程序

cd `dirname $0`

# 使用无缓冲输出 `python -u`，否则会导致docker容器长时间没有响应. 即无法通过`ctrl + c`中断容器
#
python -u app.py -k "${ACCESS_KEY}" -s "${SECRET_KEY}"

