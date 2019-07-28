import pandas as pd
from flask import (
    Blueprint,
    request,
    abort,
    render_template
)
from libs.response import template_or_json
from models.bill import BILL
from libs.db_tools import get_db_latest_create_time, get_db_latest_auto_add_time

admin = Blueprint('admin', __name__)


@admin.route('/settings/')
def settings():
    last_create_time = get_db_latest_create_time().strftime('%Y-%m-%d %H:%M:%S')
    last_auto_add_time = get_db_latest_auto_add_time().strftime('%Y-%m-%d %H:%M:%S')
    print(last_auto_add_time)
    return render_template('settings.html', data={
        'last_create_time': last_create_time,
        'last_auto_add_time': last_auto_add_time,
    })


@admin.route('/upload/')
def upload():
    return 'upp'
