import re
from datetime import datetime

from data.connet_db import query_db


def validate_ordering(ordering: str, columns: list) -> bool:
    """
    order by 防注入
    order by 使用插入对象名称而不是值，因此无法使用'?'占位符
    :param ordering: 传入的排序值
    :param columns: 表中的列名
    :return:
    """
    field = re.match(r'[-|+]?(\w+)', ordering).groups()[0]
    return True if field in columns else False


def get_db_latest_create_time(table_name="bills") -> (None, datetime):
    """
    获取表中最新更新时间, 最新的create_time
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


def get_db_latest_auto_add_time(table_name="bills") -> (None, datetime):
    """
    最后添加数据的时间，最新的auto_add_time
    :param table_name: 表名
    """
    query = f"""
            SELECT MAX(auto_add_time) AS last_time 
            FROM {table_name}
        """
    result = query_db(query, one=True)
    if result is not None:
        return datetime.strptime(result['last_time'], '%Y-%m-%d %H:%M:%S')
    return result
