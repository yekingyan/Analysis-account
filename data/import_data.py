from datetime import timedelta, datetime
import pandas as pd

from app import app
from data.connet_db import get_db, query_db
from models.bill import BILL


pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', 4000)  # 页面宽度


def serializer_1718_data(df: pd.DataFrame) -> pd.DataFrame:
    # print(df['時間戳記'])
    df['am_add_time'] = pd.to_datetime(df['時間戳記'], format='%Y年%m月%d日 上午%H:%M:%S', errors='coerce')
    df['pm_add_time'] = pd.to_datetime(df['時間戳記'], format='%Y年%m月%d日 下午%H:%M:%S', errors='coerce')
    df['pm_add_time'] = pd.DatetimeIndex(df['pm_add_time']) + timedelta(hours=12)
    df['create_time'] = df.apply(lambda x: x.pm_add_time if isinstance(x.am_add_time, pd._libs.NaTType) else x.am_add_time, axis=1)
    # print(df['create_time'])

    # print(df['交易日期'])
    df['pay_date'] = pd.to_datetime(df['交易日期'], format='%Y年%m月%d日')
    # print(df['pay_date'])

    df['transaction_type'] = df['支出类型']
    df['transaction_item'] = df['支出项目']
    df['amount'] = df['金额']
    df['payment'] = df['支付方式']
    df['pay_type'] = df['支付类型']
    df['need'] = df['需要程度']
    return df


def serializer_data(df: pd.DataFrame) -> pd.DataFrame:
    # print(df['時間戳記'])
    df['create_time'] = pd.to_datetime(df['時間戳記'])
    # print(df['create_time'])

    # print(df['交易日期'])
    df['pay_date'] = pd.to_datetime(df['交易日期'])
    # print(df['pay_date'])

    df['transaction_type'] = df['支出类型']
    df['transaction_item'] = df['支出项目']
    df['amount'] = df['金额']
    df['payment'] = df['支付方式']
    df['pay_type'] = df['支付类型']
    df['need'] = df['需要程度']
    return df


def get_db_latest_create_time(table_name="bills") -> (None, datetime):
    """
    获取表中最新更新时间
    :param table_name: 表名
    """
    query = f"""
        SELECT MAX(create_time) AS last_time 
        FROM {table_name}
    """
    result = query_db(query, one=True)
    if result is not None:
        return datetime.strptime(result['last_time'], '%Y-%m-%d %H:%M:%S')
    return result


if __name__ == '__main__':
    with app.app_context():
        db = get_db('database.db')
        df = pd.read_csv('2019账.csv')
        # df = serializer_1718_data(df)
        df = serializer_data(df)
        BILL.columns.remove('id')
        df = df[BILL.columns]
        last_time = get_db_latest_create_time()
        if last_time is not None:
            df = df[df['create_time'] > last_time]
        print(df)
        # df.to_sql('bills', con=db, if_exists='append', index=False)
