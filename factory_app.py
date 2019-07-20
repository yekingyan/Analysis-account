from flask import Flask


def create_app():
    """
    工厂函数
    """
    app = Flask(__name__)
    app.config.from_object('settings.setting')
    return app
