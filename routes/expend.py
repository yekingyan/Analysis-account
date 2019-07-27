import copy
from datetime import (
    datetime,
    date,
    timedelta,
)

import pandas as pd
import numpy as np
from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    abort,
)
from data.connet_db import (
    query_db,
)

from libs.response import template_or_json
from models.bill import BILL
from forms.expend import DaysForm, MonthsForm

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
    form = DaysForm(request.args)
    start_date = form.data['start_date']
    end_date = form.data['end_date']

    data = BILL.get_range_day_data(start_date, end_date)
    df = pd.DataFrame(data)
    if df.empty:
        abort(404, '该周期内无相应数据 \n like /expend/days/?start_date=2019/7/10&end_date=2019/7/20')

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
    df_data['pay_date'] = df_data['pay_date'].str.slice(0, -9)
    # df_data['amount'] = np.around(df_data['amount'].astype(np.double), 3)
    # 保留列
    need_columns = ['pay_date', 'amount', *transaction_types]
    [df_data.drop(col, axis=1, inplace=True) for col in list(df_data) if col not in need_columns]
    # 转dict
    data = df_data.to_dict(orient="records")

    # 各类型金额合计
    type_of_data = df_data.sum().to_dict()
    type_of_data.pop('pay_date')

    # 饼图
    pie_list = [{'类型': k, 'amount': v} for k, v in type_of_data.items() if k != 'amount']

    # 大类型合计
    type_of_data['total_eat'] = 0
    for k, v in copy.copy(type_of_data).items():
        if '餐饮' in k:
            type_of_data['total_eat'] += v
            type_of_data.pop(k)

    return template_or_json(request, 'days.html', data={
        'rows': data,
        'columns': need_columns,
        'count': len(df_data),
        'pie': pie_list,
        'type_of_data': type_of_data,
    })


@expend.route('/months/')
def months():
    form = MonthsForm(request.args)
    start_date = form.data['start_month']
    end_date = form.data['end_month']

    data = BILL.get_range_day_data(start_date, end_date)
    df = pd.DataFrame(data)
    if df.empty:
        abort(404, '该周期内无相应数据 \n like /expend/months/?start_month=2019/6&end_month=2019/7')

    df['pay_month'] = pd.to_datetime(df['pay_date']).dt.month.astype(str)
    # 各个类型 amount list
    transaction_types = df['transaction_type'].drop_duplicates().tolist()
    df_transaction_type = df.groupby(['pay_month', 'transaction_type'])['amount'].sum().reset_index()

    df_transaction_type = df_transaction_type.pivot(index='pay_month', columns='transaction_type',
                                                    values='amount').reset_index()
    # 总amount
    df_pay_month = df.groupby('pay_month')['amount'].sum().reset_index()

    # 合并总计与类型分类
    df_data = pd.merge(df_pay_month, df_transaction_type,
                       how='left',
                       left_on=df_pay_month['pay_month'],
                       right_on=df_transaction_type['pay_month'],
                       suffixes=('', '_y')
                       )
    # 去nan
    df_data = df_data.replace({np.nan: None})
    # df_data['pay_month'] = df_data['pay_month'].str.slice(0, -9)
    # df_data['amount'] = np.around(df_data['amount'].astype(np.double), 3)
    # 保留列
    need_columns = ['pay_month', 'amount', *transaction_types]
    [df_data.drop(col, axis=1, inplace=True) for col in list(df_data) if col not in need_columns]
    # 转dict
    data = df_data.to_dict(orient="records")

    # 各类型金额合计
    type_of_data = df_data.sum().to_dict()
    type_of_data.pop('pay_month')

    # 饼图
    pie_list = [{'类型': k, 'amount': v} for k, v in type_of_data.items() if k != 'amount']

    # 大类型合计
    type_of_data['total_eat'] = 0
    for k, v in copy.copy(type_of_data).items():
        if '餐饮' in k:
            type_of_data['total_eat'] += v
            type_of_data.pop(k)

    return template_or_json(request, 'days.html', data={
        'rows': data,
        'columns': need_columns,
        'count': len(df_data),
        'pie': pie_list,
        'type_of_data': type_of_data,
    })
