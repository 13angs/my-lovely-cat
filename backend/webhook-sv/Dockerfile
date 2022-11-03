# docker from docker refs: https://tomgregory.com/running-docker-in-docker-on-windows/
FROM python:3.9.13-alpine3.16

WORKDIR /usr/src/app

# install the required packages
COPY ./webhook-sv/requirements.txt ./

RUN apk update && \ 
    pip install --no-cache-dir -r requirements.txt

COPY ./webhook-sv/ ./
COPY ./common_lib ./common_lib

RUN mv ./.env.sample ./.env

# run docker as non-root user
# RUN adduser -D 13angs

# # run as 13angs
# USER 13angs
ENV TZ=Asia/Bangkok

EXPOSE 8000

CMD gunicorn -w 4 -b 0.0.0.0 'app:app'