from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from flask import (
    Blueprint,
    request,
    session,
    g,
    current_app,
    jsonify,
)
from forms.auth import LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/register/', methods=['POST'])
def register():
    form = LoginForm(request.form_with_json)
    if not form.validate():
        return jsonify(form.errors), 400
    username = form.data['username']
    password = form.data['password']
    pw_hash = generate_password_hash(password)
    print(username, pw_hash)
    return jsonify({'msg': '这个接口是用来搞笑的'})


@auth.route('/login/', methods=['POST'])
def login():
    form = LoginForm(request.form_with_json)
    if not form.validate():
        return jsonify(form.errors), 400
    username = form.data['username']
    password = form.data['password']
    the_only_user = current_app.config['USERNAME']
    pw_hash = current_app.config['PASSWORD']
    if username == the_only_user and check_password_hash(pw_hash, password):
        session['username'] = username
        return jsonify({'username': username})
    else:
        return jsonify({'msg': '登陆失败'}), 401


@auth.route('/logout/', methods=['GET'])
def logout():
    session.pop('username', None)
    return '11'


@auth.route('/state/', methods=['GET'])
def state():
    return jsonify({
        'username': g.user,
        'has_login': g.user_authenticated,
    })
