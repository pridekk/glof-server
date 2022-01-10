import os
from typing import Dict, List
import pymysql
MYSQL_URL = os.getenv("GLOF_DB_URL", "spec-glof.cvv3i6uj4giw.us-east-1.rds.amazonaws.com")
MYSQL_USER = os.getenv("GLOF_DB_USER", "admin")
MYSQL_DB = os.getenv("GLOF_DB", "glof")
MYSQL_PASSWORD = os.getenv("GLOF_DB_PASSWORD", "glofadm1!")

db = pymysql.connect(user=MYSQL_USER, passwd=MYSQL_PASSWORD, host=MYSQL_URL, db=MYSQL_DB)
cursor = db.cursor()

class TilePoint(object):
    x: int
    y: int
    user_id: str
    gained_point: int

    def __init__(self, x: int, y: int, user_id: str, gained_point: int):
        self.x = x
        self.y = y
        self.user_id = user_id
        self.gained_point = gained_point

    def __init__(self, data: Dict):
        self.x = data.get("x")
        self.y = data.get("y")
        self.user_id = data.get("user_id")
        self.gained_point = data.get("gained_point")

    def to_json(self):
        return self.__dict__

    def to_sql_insert_value(self):
        return f"({self.x}, {self.y}, '{self.user_id}', {self.gained_point} , NOW())"

    def get_x_y(self):
        return self.x, self.y


def add_user_tiles_points(tiles: List[TilePoint]):
    sql = ""
    for tile in tiles:
        sql += tile.to_sql_insert_value() + ","

    sql = sql[:-1]
    sql = f"INSERT INTO user_tile_points (x, y, user_id, gained_point, updated_at) VALUES {sql} " \
          f"ON DUPLICATE KEY UPDATE gained_point = gained_point + values(gained_point), updated_at = NOW()"

    cursor.execute(sql)
    db.commit()

def update_land_tiles(tiles: List[TilePoint]):
    updated_tiles = set([tile.get_x_y() for tile in tiles])

    for tile in updated_tiles:
        sql = f"INSERT INTO land_tiles (x, y, owner_id) SELECT up.x, up.y, user_id FROM user_tile_points up JOIN " \
              f"(SELECT x, y, MAX(gained_point) AS gp FROM user_tile_points WHERE x = {tile[0]} and y = {tile[1]} GROUP BY x, y) uc " \
              f"ON up.x = uc.x AND up.y = uc.y AND up.gained_point = uc.gp " \
              f"ON DUPLICATE KEY UPDATE owner_id = VALUES(owner_id), updated_at = NOW();"
        cursor.execute(sql)

    test = db.commit()

    return updated_tiles

