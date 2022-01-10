import os
from typing import Tuple
import pymysql
import math
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

    owners_query = f"SELECT x,y,owner_id FROM land_tiles WHERE x between {west} and {east} and y between {north} and {south}"

    cursor.execute(owners_query)

    sql_return_values = sql_fetchall_json(cursor)
    owners = []
    for owner in sql_return_values:
        owners.append(TileOwner(owner["x"], owner["y"], owner["owner_id"]).to_json())
    return owners


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


class TileOwner(object):
    tile_x: int
    tile_y: int
    owner_id: int
    center_x: float
    center_y: float

    def __init__(self, x: int, y: int, owner_id: int):
        self.tile_x = x
        self.tile_y = y
        self.owner_id = owner_id
        self.center_x, self.center_y = self.num2deg()

    def num2deg(self, zoom: int = 18) -> Tuple:
        """
        타일의 센터 좌표 계산
        :param zoom: 줌 기본 18
        :return: 센터 좌표 Tuple
        """
        n = 2.0 ** zoom
        lon_deg = self.tile_x / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * self.tile_y / n)))
        lat_deg = math.degrees(lat_rad)
        return lat_deg, lon_deg

    def to_json(self):
        return self.__dict__
