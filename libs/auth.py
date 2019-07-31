from functools import wraps

from flask import g, jsonify


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        print(g.user_authenticated)
        if g.user_authenticated:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': '无权访问'}), 401
    return decorated_view
