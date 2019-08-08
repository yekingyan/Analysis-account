import pandas as pd
import numpy as np
from flask import (
    Blueprint,
    request,
    abort,
)
from libs.response import template_or_json
from models.bill import BILL
from forms.expend import DaysForm, MonthsForm

expend = Blueprint('expend', __name__)
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', 4000)  # 页面宽度


@expend.route('/journal/')
def journal():
    form = DaysForm(request.args)
    start_date = form.data['start_date']
    end_date = form.data['end_date']

    bill = BILL(start_date, end_date, '-id')
    data = bill.data
    return template_or_json(request, 'journal.html', data={
        'rows': data,
        'columns': bill.columns,
        'count': len(data),
    })


@expend.route('/days/')
def days():
    form = DaysForm(request.args)
    start_date = form.data['start_date']
    end_date = form.data['end_date']

    bill = BILL(start_date, end_date)
    if not bill:
        abort(404, '该周期内无相应数据 \n like /expend/days/?start_date=2019/7/10&end_date=2019/7/20')

    df_data = bill.daily_amount_by_types()
    # 时间只保留日期。去nan
    df_data['pay_date'] = df_data['pay_date'].str.slice(0, -9)
    df_data = df_data.replace({np.nan: None})
    # 折线图与table数据
    data = df_data.to_dict(orient="records")

    # 各类型合计数
    df_types_amount = bill.total_amount_by_types()
    # 饼图
    pie_list = df_types_amount.to_dict('records')
    # 大类型(选择性合并几个小类型)合计数， 详情
    type_of_data = bill.total_amount_by_types_merge_eat(df_types_amount)
    type_of_data = {k: v for k, v in type_of_data.items() if k in ['amount', 'total_eat']}

    # 同比 环比
    ratio = bill.time_of_ratio()

    return template_or_json(request, 'days.html', data={
        'rows': data,
        'columns': bill.day_columns,
        'count': len(df_data),
        'pie': pie_list,
        'type_of_data': type_of_data,
        'ratio': ratio,
    })


@expend.route('/months/')
def months():
    form = MonthsForm(request.args)
    start_date = form.data['start_month']
    end_date = form.data['end_month']

    bill = BILL(start_date, end_date)
    if not bill:
        abort(404, '该周期内无相应数据 \n like /expend/months/?start_month=2019/6&end_month=2019/7')

    # 时间粒度合计数
    df_data = bill.monthly_amount_by_types()
    # 去nan
    df_data = df_data.replace({np.nan: None})
    # 折线图与table
    data = df_data.to_dict(orient="records")

    # 各类型合计数
    df_types_amount = bill.total_amount_by_types()
    # 饼图
    pie_list = df_types_amount.to_dict('records')

    # 大类型(选择性合并几个小类型)合计数， 详情
    type_of_data = bill.total_amount_by_types_merge_eat(df_types_amount)
    type_of_data = {k: v for k, v in type_of_data.items() if k in ['amount', 'total_eat']}

    # 同比 环比
    ratio = bill.time_of_ratio()

    return template_or_json(request, 'days.html', data={
        'rows': data,
        'columns': bill.month_columns,
        'count': len(df_data),
        'pie': pie_list,
        'type_of_data': type_of_data,
        'ratio': ratio,
    })
