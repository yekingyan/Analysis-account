##

### Requirements
- Flask
- pandas
- WTForms

### 安装项目依赖
```
$ virtualenv --no-site-packages .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### 修改配置文件
```
$ cp deploy/settings_secure.py settings/secure.py
```

### 开发启动项目
```
$ python app.py
```

### Docker

#### 构建方式
采用 BuildKit 多阶段构建方式， Docker 版本需大于 18.06。

修改/etc/docker/daemon.json， 加入{"experimental":true}

检查是否修改成功 
```$ docker version -f '{{.Server.Experimental}}'```

启用多层构建方式，设置环境变量（可全局） DOCKER_BUILDKIT=1


#### 正常打包
```
$ DOCKER_BUILDKIT=1 docker build -t yekingyan/analysisaccount .
```

#### pip环境有变的打包
```
#方法一：一次性build完
$ DOCKER_BUILDKIT=1 docker build -t new --build-arg PIP_ENV=new .

#方法二：留下中间层方便下次使用
$ docker build --target new-env -t yekingyan/analysisaccount:env .
$ docker push yekingyan/analysisaccount:env
$ DOCKER_BUILDKIT=1 docker build -t old .
```


#### 启动容器
```
$ docker run -d -p 5354 yekingyan/analysisaccount .

ps: support docker-compose
```

