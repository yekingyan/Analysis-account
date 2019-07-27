from datetime import date
from data.connet_db import get_db, query_db


class BILL:
    create_bill_text = """
        CREATE TABLE IF NOT EXISTS `bills`(
            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `create_time` DATETIME NOT NULL, -- 添加时间
            `pay_date` DATE NOT NULL, -- 付款时间
            `transaction_type` TEXT NOT NULL, -- 交易类型
            `transaction_item` TEXT, -- 交易项目
            `amount` DECIMAL(7, 3) NOT NULL, -- 金额
            `payment` TEXT NOT NULL, -- 支付方式
            `pay_type` TEXT NOT NULL, -- 支付类型
            `need` INTEGER NOT NULL -- 需要程度
)"""
    columns = ['id', 'create_time', 'pay_date', 'transaction_type', 'transaction_item', 'amount', 'payment', 'pay_type',
               'need']

    def __init__(self, start_pay_date: date, end_pay_date: date):
        self.start_pay_date = start_pay_date
        self.end_pay_date = end_pay_date
        self.data = self.get_range_day_data(start_pay_date, end_pay_date)

    @staticmethod
    def create_bill():
        """创建表"""
        get_db().execute(BILL.create_bill_text)

    @staticmethod
    def get_range_day_data(start_pay_date: date, end_pay_date: date) -> (dict, None):
        """
        取一段时间(pay_date)的数据
        """
        query = """
            SELECT *
            FROM bills
            WHERE pay_date BETWEEN ? AND ?;
        """
        return query_db(query, (start_pay_date, end_pay_date))

    @classmethod
    def day_interval(cls, start: date, end: date) -> (dict, None):
        """
        以天为颗粒度
        总数，各类型数
        """
        data = cls.get_range_day_data(start, end)

    def month_interval(self, start: date, end: date) -> (dict, None):
        """
        以月为颗粒度
        总数，各类型数
        """
        ...

