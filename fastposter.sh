#! /bin/bash
cd `dirname $0`
python -u app.py -k "${ACCESS_KEY}" -s "${SECRET_KEY}"

