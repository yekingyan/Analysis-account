from factory_app import create_app
app = create_app()
from data.connet_db import get_db, query_db


@app.route('/')
def hello_world():
    print(1212)
    return 'Hello World!111'


@app.route('/a/')
def hello_world1():
    query = """
        SELECT *
        FROM bills
        WHERE create_time >= ?
    """
    import datetime
    create_time = datetime.datetime(year=2019, month=6, day=1)
    data = query_db(query, (create_time,))
    for row in data:
        print(row['create_time'], row['amount'])
        print(type(row['create_time']), type(row['amount']))
    from flask import jsonify
    return jsonify(data)


if __name__ == '__main__':
    app.run()
