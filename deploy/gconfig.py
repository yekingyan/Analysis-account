from gevent import monkey

monkey.patch_all()

import multiprocessing

debug = 'true'
bind = '127.0.0.1:5354'
# logs
loglevel = 'debug'
pidfile = 'logs/gunicorn.pid'
logfile = 'logs/debug.log'
errorlog = "logs/error.log"

# 默认为阻塞模式，选择gevent模式
worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1

# gunicorn -c deploy/gconfig.py app:app
