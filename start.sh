#! /bin/bash
# desc: 入口程序

cd `dirname $0`

echo "run fastposter on 9001"

python app.py -k "${ACCESS_KEY}" -s "${SECRET_KEY}"

