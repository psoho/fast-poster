#!/bin/bash

cd $(dirname $0)
pwd

#(./design/build.sh)

server=sh1
rsync -avz --exclude="__pycache__" --exclude="venv" --exclude="data" server/ root@${server}:/opt/docker/fastposter-python/app/ \
&& ssh root@${server} 'cd /opt/docker/fastposter-python/; docker-compose restart fastposter-python' \
&& ssh root@${server} 'docker logs -f --tail=10 fastposter-python'


#server=sh1
#rsync -avz .docker/ root@${server}:/opt/docker/fastposter-pro-python/