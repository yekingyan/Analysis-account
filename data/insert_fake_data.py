from datetime import datetime, timedelta
from numpy.random import randint, choice


from app import app
from models.bill import BILL
from data.connet_db import _get_db

# """
# UPDATE bills
# SET amount = amount + ABS(RANDOM()) % (100 - 10) + 10
# """


query = """
INSERT INTO bills(create_time, pay_date, transaction_type, transaction_item,
amount, payment, pay_type, need) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

payments = ['信用卡', '支付宝', '微信', '现金', '银行卡']
pay_types = ['现金', '信贷']
needs = range(1, 6)


def template(_datetime, transaction_type, amount):
    return (_datetime, _datetime, transaction_type, None, amount,
            choice(payments, 1)[0], choice(pay_types, 1)[0], int(choice(needs, 1, p=[0.4, 0.2, 0.2, 0.1, 0.1])[0]))


def create_data():
    values_to_insert = []
    _datetime = datetime(year=2019, month=1, day=1)
    while _datetime.year <= 2019:
        cloth = template(_datetime, '衣服', randint(30, 150))
        food = template(_datetime, '餐饮', randint(70, 200))
        live = template(_datetime, '房租', randint(150, 200))
        line = template(_datetime, '交通', randint(10, 20))
        fruits = template(_datetime, '水果', randint(5, 20))

        values_to_insert.extend([cloth, food, live, line, fruits])
        _datetime = _datetime + timedelta(days=1)
    return values_to_insert


if __name__ == '__main__':
    with app.app_context():
        db = _get_db('fake_database.db')
        db.execute(BILL.create_bill_text)
        values = create_data()
        print(values)
        db.executemany(query, values)
        db.commit()
        # db.execute(query, values[0])
