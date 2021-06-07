#! /bin/bash

# desc: 构建镜像
POSTER_VERSION=1.3.0

cd `dirname $0`

function build() {
  echo 构建镜像 tangweixin/poster:$POSTER_VERSION
  docker build -t tangweixin/poster:$POSTER_VERSION -f Dockerfile .
  docker push tangweixin/poster:$POSTER_VERSION
}

build