import typing

import pymysql

conn = pymysql.Connection()
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)


def query(sql: str) -> typing.Any:
    try:
        return cursor.execute(sql)
    finally:
        cursor.close()
        conn.close()


def operate(sql: str) -> bool:
    try:
        cursor.execute(sql)
        conn.commit()
        return True
    except:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
