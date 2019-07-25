from datetime import (
    datetime,
    timedelta,
    date,
)
import pandas as pd

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


expend = Blueprint('expend', __name__)


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
    query = """
            SELECT *
            FROM bills
            WHERE pay_date >= ?
            ORDER BY pay_date
        """

    pay_date = date.today() - timedelta(days=160)
    data = query_db(query, (pay_date,))
    # print(data)
    df = pd.DataFrame(data)
    df = df.groupby('pay_date')['amount'].sum().reset_index()
    # df = df.groupby('pay_date', ).sum()
    print(df)
    data = df.to_dict(orient="records")
    print(data)
    return template_or_json(request, 'test_vue.html', data)
