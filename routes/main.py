from flask import (
    Blueprint,
    redirect,
    url_for,
)

main = Blueprint('main', __name__)


@main.route('/ping/')
def ping():
    return '200 ok'


@main.route('/')
def index():
    return redirect(url_for('expend.days'))


@main.route('/home/')
def home():
    from flask import render_template
    return render_template('home.html')
