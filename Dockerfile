FROM python:3.6-slim

WORKDIR /app
COPY . /app

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list \
    && tools='curl iputils-ping net-tools vim' \
    && apt-get update \
    && apt-get install -y $tools \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    # 换时区
    && ln -fs /usr/share/zoneinfo/US/Asia/Shanghai /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    # python 依赖
    && pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
    && cp deploy/settings_secure.py settings/secure.py

CMD gunicorn -c deploy/gconfig.py app:app
EXPOSE 5354
