from datetime import (
    datetime,
    date,
)

import pandas as pd
import numpy as np
from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
)
from data.connet_db import (
    query_db,
)

from libs.response import template_or_json
from models.bill import BILL

expend = Blueprint('expend', __name__)
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', 4000)  # 页面宽度


@expend.route('/')
def hello_world():
    print(1212)
    return render_template('test.html')


@expend.route('/a/')
def hello_world1():
    query = """
        SELECT *
        FROM bills
        WHERE create_time >= ?
    """
    create_time = datetime(year=2019, month=6, day=1)
    data = query_db(query, (create_time,))
    for row in data:
        print(row['create_time'], row['amount'])
        print(type(row['create_time']), type(row['amount']))
    return jsonify(data)


@expend.route('/days/')
def days():
    bill = BILL()
    start = date(year=2019, month=4, day=1)
    end = date(year=2019, month=8, day=1)
    data = bill.get_range_day_data(start, end)
    df = pd.DataFrame(data)

    # 各个类型 amount list
    transaction_types = df['transaction_type'].drop_duplicates().tolist()
    df_transaction_type = df.groupby(['pay_date', 'transaction_type'])['amount'].sum().reset_index()
    df_transaction_type = df_transaction_type.pivot(index='pay_date', columns='transaction_type',
                                                    values='amount').reset_index()
    # 总amount
    df_pay_date = df.groupby('pay_date')['amount'].sum().reset_index()

    # 合并总计与类型分类
    df_data = pd.merge(df_pay_date, df_transaction_type,
                       how='left',
                       left_on=df_pay_date['pay_date'],
                       right_on=df_transaction_type['pay_date'],
                       suffixes=('', '_y')
                       )
    # 去nan
    df_data = df_data.replace({np.nan: None})
    # 保留列
    need_columns = ['pay_date', 'amount', *transaction_types]
    [df_data.drop(col, axis=1, inplace=True) for col in list(df_data) if col not in need_columns]
    # 转dict
    data = df_data.to_dict(orient="records")

    return template_or_json(request, 'days.html', data={
        'rows': data,
        'columns': need_columns,
        'count': len(df_data)
    })
