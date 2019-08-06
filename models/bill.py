from datetime import date
from copy import copy
from dateutil.relativedelta import relativedelta

import pandas as pd

from data.connet_db import get_db, query_db
from libs.db_tools import validate_ordering

__migrate = """
表迁移

INSERT INTO bills(
create_time, pay_date, transaction_type, transaction_item, 
amount, payment, pay_type, need) 
SELECT create_time, pay_date,transaction_type, 
transaction_item, amount, payment, pay_type, need 
FROM bills_without_autoat;
"""


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
            `need` INTEGER NOT NULL, -- 需要程度
            `auto_add_time` DATETIME DEFAULT (datetime('now','localtime'))  -- 数据导入时间
)"""
    columns = ['id', 'create_time', 'pay_date', 'transaction_type', 'transaction_item', 'amount', 'payment', 'pay_type',
               'need', 'auto_add_time']
    accuracy = 3  # 计算精度

    start_pay_date = None  # 开始支付日期
    end_pay_date = None  # 结束支付日期
    chain_start_date = None  # 环比开始日期
    chain_end_date = None  # 环比结束日期
    last_year_start_date = None  # 同比开始日期
    last_year_end_date = None  # 同比结束日期

    data = None  # 当前时间段内的dict数据
    df_data = None  # 当前时间段内的df数据
    total_data = None  # 当前+同环比dict数据
    df_total_data = None  # 当前+同环比df数据
    types_columns = None  # 当前时间段内各消费类型
    month_field = 'pay_month'  # 指代月份的列名

    def __init__(self, start_pay_date: date, end_pay_date: date, ordering='id'):
        self.start_pay_date = start_pay_date
        self.end_pay_date = end_pay_date
        # 同比时间段
        self.chain_start_date = start_pay_date - (end_pay_date - start_pay_date)
        self.chain_end_date = start_pay_date
        # 环比时间段
        self.last_year_start_date = start_pay_date - relativedelta(years=1)
        self.last_year_end_date = end_pay_date - relativedelta(years=1)

        print(start_pay_date, end_pay_date)
        print(self.chain_start_date, self.chain_end_date)
        print(self.last_year_start_date, self.last_year_end_date)

        # 所有数据
        self.total_data = self.get_range_day_data(
            self.last_year_start_date, self.last_year_end_date, self.chain_start_date, end_pay_date, ordering)
        self.df_total_data = pd.DataFrame(self.total_data)
        self.df_total_data['pay_date_datetime'] = pd.to_datetime(self.df_total_data['pay_date'])
        # 当前数据
        self.df_data = self.df_total_data[(start_pay_date < self.df_total_data['pay_date_datetime'])
                                          & (self.df_total_data['pay_date_datetime'] < end_pay_date)]
        del self.df_data['pay_date_datetime']
        self.data = self.df_data.to_dict(orient='records')

        # columns
        self.types_columns = self._get_types_columns()
        self.day_columns = ['pay_date', 'amount', *self.types_columns]
        self.month_columns = [self.month_field, 'amount', *self.types_columns]

    def __bool__(self):
        if self.df_data.empty:
            return False
        else:
            return True

    @staticmethod
    def create_bill():
        """创建表"""
        get_db().execute(BILL.create_bill_text)

    def _get_types_columns(self) -> list:
        """各消费类型"""
        if not self:
            return []
        return self.df_data['transaction_type'].drop_duplicates().tolist()

    @classmethod
    def get_range_day_data(cls, last_year_start_date: date, last_year_end_date: date,
                           chain_start_date: date, end_pay_date: date, ordering='-id') -> (dict, None):
        """
        取两段时间(pay_date)的数据
        环比 一段， 同比+当前 一段
        """
        if not validate_ordering(ordering, cls.columns):
            raise Exception('排序字段不在表列名中')
        query = f"""
            SELECT *
            FROM bills
            WHERE pay_date BETWEEN ? AND ? OR pay_date BETWEEN ? AND ?
            ORDER BY {ordering};
        """
        data = query_db(query, (last_year_start_date, last_year_end_date, chain_start_date, end_pay_date))
        return data

    def get_amount_of_granularity(self, granularity: str, need_columns: list) -> pd.DataFrame:
        """
        根据不同的颗粒度，返回相应的类型（col）所对应的amount(row)
        :param granularity: 数据分组的颗粒度，需在self.df_data的列名中
        :param need_columns: 需要保留的列

        pay_month   amount     交通     ...
        4           6527.14    734.3    ...
        5           7021.42    630.0    ...
        """
        df = self.df_data
        if df.empty or granularity not in self.df_data:
            raise Exception('无效的granularity 或 时间区间内数据为空')

        # granularity时间内  各个类型 对应的 amount
        df_transaction_type = df.groupby([granularity, 'transaction_type'])['amount'].sum().reset_index()
        df_transaction_type = df_transaction_type.pivot(index=granularity, columns='transaction_type',
                                                        values='amount').reset_index().round(self.accuracy)
        # granularity时间内 总amount
        df_amount_of_granularity = df.groupby(granularity)['amount'].sum().reset_index().round(self.accuracy)

        # 合并总计与类型分类
        df_amount_and_types = pd.merge(df_amount_of_granularity, df_transaction_type,
                                       how='left',
                                       left_on=df_amount_of_granularity[granularity],
                                       right_on=df_transaction_type[granularity],
                                       suffixes=('', '_y')
                                       )
        # 保留列
        [df_amount_and_types.drop(col, axis=1, inplace=True) for col in list(df_amount_and_types) if col not in need_columns]
        return df_amount_and_types

    def daily_amount_by_types(self) -> pd.DataFrame:
        """
        以天为颗粒度
        总数，各类型数
        """
        granularity = 'pay_date'
        need_columns = self.day_columns
        df_data = self.get_amount_of_granularity(granularity, need_columns)
        return df_data

    def monthly_amount_by_types(self) -> pd.DataFrame:
        """
        以月为颗粒度
        总数，各类型数
        """
        granularity = self.month_field
        need_columns = self.month_columns
        self.df_data[self.month_field] = pd.to_datetime(self.df_data['pay_date']).dt.month.astype(str)
        df_data = self.get_amount_of_granularity(granularity, need_columns)
        return df_data

    def total_amount_by_types(self) -> pd.DataFrame:
        """类型合计金额"""
        df = self.df_data
        df_transaction_type = df.groupby(['transaction_type'])['amount'].sum().reset_index().round(self.accuracy)
        df_transaction_type = df_transaction_type.rename(columns={'transaction_type': '类型'})
        return df_transaction_type

    def total_amount_by_types_merge_eat(self, total_amount_by_types: pd.DataFrame) -> dict:
        """
        合并多个餐饮数据
        :param total_amount_by_types:  self.total_amount_by_types的结果
        :return:
        """
        type_of_data = {k: v for k, v in total_amount_by_types.values}
        type_of_data['amount'] = float(total_amount_by_types['amount'].sum().round(self.accuracy))
        type_of_data['total_eat'] = 0
        for k, v in copy(type_of_data).items():
            if '餐饮' in k:
                type_of_data['total_eat'] += v
                type_of_data.pop(k)
        type_of_data['total_eat'] = round(type_of_data['total_eat'], self.accuracy)
        return type_of_data

    def time_of_ratio(self):
        """同比、环比"""
        ...


if __name__ == '__main__':
    import os
    from app import app
    with app.app_context():
        # 运行时路径与app.py保持一致
        os.chdir('..')
        BILL.create_bill()
