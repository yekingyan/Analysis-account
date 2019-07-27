import re


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
