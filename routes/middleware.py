from flask import (
    request,
    session,
    g,
)
from app import app


@app.before_request
def session_auth():
    """用户标识"""
    username = session.get('username')
    if username is not None:
        g.user = username
        g.user_authenticated = True
    else:
        g.user = None
        g.user_authenticated = False


@app.before_request
def construct_request():
    """同时获取form 与json 数据"""
    json_data = request.get_json() or {}
    form_data = request.form.copy()
    form_data.update(json_data)
    request.form_with_json = form_data


@app.before_request
def request_log():
    ...


@app.after_request
def response_log(res):
    return res
