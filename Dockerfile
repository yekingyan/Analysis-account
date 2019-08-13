FROM python:3.6-alpine

WORKDIR /app
COPY . /app

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk update \
    && apk add --no-cache make automake gcc g++ subversion python3-dev curl tzdata \
    # 换时区
    && ln -sf /user/share/zoneinfo/Asia/ShangHai /etc/localtime \
    && echo 'Asia/Shanghai' > /etc/timezone \
    && apk del tzdata \
    # python 依赖
    && pip install -r requirements.txt -i https://pypi.douban.com/simple/ \
    && cp deploy/settings_secure.py settings/secure.py

CMD gunicorn -c deploy/gconfig.py app:app
EXPOSE 5354
