from datetime import timedelta
import pandas as pd

from data.connet_db import get_db
from models.bill import BILL
from libs.db_tools import get_db_latest_create_time

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
    need_columns = filter(lambda x: x not in ['id', 'auto_add_time'], BILL.columns)
    df = df[need_columns]
    return df


def serializer_now_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    2019年表格用的字段不同
    直接下载csv和下载excel再转csv会让时间相关字段不同需要try一手
    """
    # print(df['時間戳記'])
    try:
        df['am_add_time'] = pd.to_datetime(df['時間戳記'], format='%Y年%m月%d日 上午%H:%M:%S', errors='coerce')
        df['pm_add_time'] = pd.to_datetime(df['時間戳記'], format='%Y年%m月%d日 下午%H:%M:%S', errors='coerce')
        df['pm_add_time'] = pd.DatetimeIndex(df['pm_add_time']) + timedelta(hours=12)
        df['create_time'] = df.apply(lambda x: x.pm_add_time if isinstance(x.am_add_time, pd._libs.NaTType) else x.am_add_time, axis=1)
    except ValueError:
        df['create_time'] = pd.to_datetime(df['時間戳記'])
    # print(df['create_time'])

    # print(df['交易日期'])
    try:
        df['pay_date'] = pd.to_datetime(df['交易日期'])
    except ValueError:
        df['pay_date'] = pd.to_datetime(df['交易日期'], format='%Y年%m月%d日')
    # print(df['pay_date'])

    df['transaction_type'] = df['交易分类']
    df['transaction_item'] = df['支出项目']
    df['amount'] = df['金额']
    df['payment'] = df['支付方式']
    df['pay_type'] = df['支付类型']
    df['need'] = df['需要程度']
    need_columns = filter(lambda x: x not in ['id', 'auto_add_time'], BILL.columns)
    df = df[need_columns]
    return df


def serializer_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    解析原始读csv的数据为可直接存数据库的格式
    """
    try:
        df_parse = serializer_now_data(df)
    except ValueError:
        df_parse = serializer_1718_data(df)
    return df_parse


def create_or_append_df_to_sql(df: pd.DataFrame, table_name="bills") -> pd.DataFrame:
    """
    添加数据到表，如果表不存在将自动创建
    :return 增量添加进的数据
    """
    df = serializer_data(df)
    last_time = get_db_latest_create_time()
    if last_time is not None:
        df = df[df['create_time'] > last_time]
    db = get_db()
    df.to_sql(table_name, con=db, if_exists='append', index=False)
    return df


# if __name__ == '__main__':
#     from app import app
#     with app.app_context():
#         db = get_db('database.db')
#         df = pd.read_csv('2019账.csv')
#         create_or_append_df_to_sql(df)
