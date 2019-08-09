from flask import (
    Blueprint,
)

main = Blueprint('main', __name__)


@main.route('/ping/')
def ping():
    return '200 ok'


@main.route('/')
def index():
    from flask import render_template
    return render_template('index__test.html')
