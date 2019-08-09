from flask import (
    request,
    session,
    g,
    Blueprint,
)

middleware = Blueprint('middleware', __name__)


@middleware.before_app_request
def session_auth():
    """用户标识"""
    username = session.get('username')
    if username is not None:
        g.user = username
        g.user_authenticated = True
    else:
        g.user = None
        g.user_authenticated = False


@middleware.before_app_request
def construct_request():
    """同时获取form 与json 数据"""
    json_data = request.get_json() or {}
    form_data = request.form.copy()
    form_data.update(json_data)
    request.form_with_json = form_data


@middleware.before_app_request
def request_log():
    ...


@middleware.after_request
def response_log(res):
    return res
