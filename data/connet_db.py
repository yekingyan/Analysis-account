import sqlite3
from contextlib import contextmanager

from flask import g
from flask import current_app
# from app import app


def make_dicts(cursor, row):
    """
    select 查询获得字典而不是元组
    """
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db(db_path=None):
    """
    :param db_path: sqlite路径
    :return: db
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path or current_app.config['DATABASE'])
        db.row_factory = make_dicts
    return db


@contextmanager
def db_manager(db_path=None):
    """上下文管理数据库连接"""
    db = get_db(db_path)
    yield db
    db.close()
    delattr(g, '_database')


def get_db_without_context(db_path=None):
    return sqlite3.connect(db_path or current_app.config['DATABASE'])


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()


# def query_db(query, args=(), one=False):
#     """
#     for user in query_db('select * from users'):
#     print user['username'], 'has the id', user['user_id']
#     """
#     cur = get_db().execute(query, args)
#     rv = cur.fetchall()
#     cur.close()
#     return (rv[0] if rv else None) if one else rv


def query_db(query, args=(), one=False, db_path=None):
    """
    for user in query_db('select * from users'):
    print user['username'], 'has the id', user['user_id']
    """
    with db_manager(db_path) as db:
        cur = db.execute(query, args)
        rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


