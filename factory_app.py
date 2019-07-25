from flask import Flask
from routes.expend import expend


def register_blueprint(app):
    """
    注册蓝图
    """
    app.register_blueprint(expend, url_prefix='/expend')


def create_app():
    """
    工厂函数
    """
    app = Flask(__name__)
    app.config.from_object('settings.setting')
    register_blueprint(app)
    return app
