FROM alpine:3.5

RUN apk update --no-cache && apk upgrade
RUN apk add python3
RUN pip3 install awscli pymysql

WORKDIR /app

ADD py/ /app/