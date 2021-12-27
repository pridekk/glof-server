import os
import pymysql
from _datetime import datetime, date
MYSQL_URL = os.getenv("GLOF_DB_URL", "spec-glof.cvv3i6uj4giw.us-east-1.rds.amazonaws.com")
MYSQL_USER = os.getenv("GLOF_DB_USER", "admin")
MYSQL_DB = os.getenv("GLOF_DB", "glof")
MYSQL_PASSWORD = os.getenv("GLOF_DB_PASSWORD")

db = pymysql.connect(user=MYSQL_USER, passwd=MYSQL_PASSWORD, host=MYSQL_URL, db=MYSQL_DB, autocommit=True)
cursor = db.cursor()


def get_land_owners(params):
    north = int(params.get("north", 0))
    south = int(params.get("south", 1))
    west = int(params.get("west", 0))
    east = int(params.get("east", 1))

    owners_query = f"SELECT * FROM land_tiles WHERE x between {west} and {east} and y between {north} and {south}"

    cursor.execute(owners_query)

    return sql_fetchall_json(cursor)


def sql_fetchall_json(db_cursor: pymysql.cursors.Cursor):
    """
    Convert the pymysql SELECT result to json format list
    :param db_cursor: pymysql.cursors.Cursor
    :return: Json Array
    """
    keys = []
    for column in db_cursor.description:
        keys.append(column[0])
    key_number = len(keys)

    json_data = []
    for row in db_cursor.fetchall():
        item = dict()
        for q in range(key_number):
            data = row[q]
            if type(data) is datetime:
                data = data.strftime("%Y-%m-%d %H:%M:%S")
            elif type(data) is date:
                data = data.strftime("%Y-%m-%d")
            item[keys[q]] = data
        json_data.append(item)

    return json_data
