FROM python:3.7-slim

LABEL maintainer="thomastangweixin@163.com"

ADD app.py C.py dao.py poster.py R.py start.sh key.py requirements.txt /app/
COPY static/ /app/static/
COPY fonts/ /app/fonts/

EXPOSE 9001

VOLUME /app/static

WORKDIR /app
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

ENV ACCESS_KEY=""
ENV SECRET_KEY=""
ENV POSTER_URI_PREFIX=""

ENTRYPOINT ["/bin/bash", "start.sh"]