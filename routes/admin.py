import os
from datetime import datetime

import pandas as pd
from flask import (
    Blueprint,
    request,
    render_template,
    current_app,
    jsonify,
)
from libs.db_tools import (
    get_db_latest_create_time,
    get_db_latest_auto_add_time,
)
from libs.auth import login_required
from libs.upload import secure_filename_utf8
from data.import_data import create_or_append_df_to_sql

admin = Blueprint('admin', __name__)


@admin.route('/settings/')
def settings():
    last_create_time = get_db_latest_create_time().strftime('%Y-%m-%d %H:%M:%S')
    last_auto_add_time = get_db_latest_auto_add_time().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('settings.html', data={
        'last_create_time': last_create_time,
        'last_auto_add_time': last_auto_add_time,
    })


@admin.route('/upload/', methods=['POST'])
@login_required
def upload():
    try:
        file = request.files['file']
        df = pd.read_csv(file)
        # 增量写入sql
        df_patch = create_or_append_df_to_sql(df)
    except KeyError:
        return jsonify({'error': '无效的文件，或错误的列名'}), 422

    # 保存文件
    str_time = str(datetime.now().strftime('%Y%m%d%H%M%S'))
    filename = f"{str_time}_{secure_filename_utf8(file.filename)}"
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    df.to_csv(path, index=False, encoding='utf_8_sig')

    return jsonify({'patch_len': len(df_patch)}), 201
