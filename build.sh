#! /bin/bash

# desc: 构建镜像
POSTER_VERSION=1.3.2

cd `dirname $0`

function build() {
  echo 构建镜像 tangweixin/fast-poster:$POSTER_VERSION
  docker build -t tangweixin/fast-poster:$POSTER_VERSION -f Dockerfile .
  docker tag tangweixin/fast-poster:$POSTER_VERSION tangweixin/fast-poster:latest
  docker push tangweixin/fast-poster:$POSTER_VERSION
  docker push tangweixin/fast-poster:latest
}

build