import os
from flask import Flask
from routes.expend import expend
from routes.admin import admin


def register_blueprint(app):
    """
    注册蓝图
    """
    app.register_blueprint(expend, url_prefix='/expend')
    app.register_blueprint(admin, url_prefix='/admin')


def create_essential_folder(app):
    """创建必要的文件夹"""
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])


def create_app():
    """
    工厂函数
    """
    app = Flask(__name__)
    app.config.from_object('settings.setting')
    register_blueprint(app)
    create_essential_folder(app)
    return app
