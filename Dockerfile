FROM python:3.7-slim

LABEL maintainer="thomastangweixin@163.com"
LABEL version="1.4.1"

ADD fastposter.sh key.py app.py C.py dao.py poster.py R.py store.py requirements.txt /app/
COPY static/ /app/static/
COPY fonts/ /app/fonts/

EXPOSE 9001

VOLUME /app/static

WORKDIR /app
#RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN pip install -r requirements.txt

ENV ACCESS_KEY="ApfrIzxCoK1DwNZO"
ENV SECRET_KEY="EJCwlrnv6QZ0PCdvrWGi"
ENV POSTER_URI_PREFIX="http://127.0.0.1:9001/"

#ENTRYPOINT ["/bin/bash", "fastposter.sh"]
CMD ["/bin/bash", "fastposter.sh"]
