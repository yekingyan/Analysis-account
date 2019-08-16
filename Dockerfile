# Defining environment
ARG PIP_ENV=old


FROM scratch AS ac-code-only
COPY . /code


FROM python:3.6-slim AS new-env
COPY requirements.txt requirements.txt
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list \
    && tools='curl iputils-ping net-tools vim' \
    && apt-get update \
    && apt-get install -y $tools \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    # 换时区
    && ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    # python 依赖
    && pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple


FROM yekingyan/analysisaccount:env AS old-env
RUN echo "import old env"


FROM ${PIP_ENV}-env as final
WORKDIR /app
COPY . /app
COPY --from=ac-code-only /code /app
RUN cp deploy/settings_secure.py settings/secure.py \
    && mkdir -p logs

CMD gunicorn -c deploy/gconfig.py app:app
EXPOSE 5354


# use new env:
#    方法一：一次性build完
#    DOCKER_BUILDKIT=1 docker build -t yekingyan/analysisaccount --build-arg PIP_ENV=new .
#    方法二：留下中间层方便下次使用
#    docker build --target new-env -t yekingyan/analysisaccount:env .
#    docker push yekingyan/analysisaccount:env
#    DOCKER_BUILDKIT=1 docker build -t yekingyan/analysisaccount .

# user old env:
#    DOCKER_BUILDKIT=1 docker build -t yekingyan/analysisaccount .
