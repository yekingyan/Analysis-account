from flask import Flask
from routes.expend import expend
from routes.admin import admin


def register_blueprint(app):
    """
    注册蓝图
    """
    app.register_blueprint(expend, url_prefix='/expend')
    app.register_blueprint(admin, url_prefix='/admin')


def create_app():
    """
    工厂函数
    """
    app = Flask(__name__)
    app.config.from_object('settings.setting')
    register_blueprint(app)
    return app
