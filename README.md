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

### 启动项目
```
$ python app.py
```

