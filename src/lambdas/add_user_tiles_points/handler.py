import json
import utils


def lambda_handler(event, context):
    """
    사용자의 타일 포인트 업데이트 로직,
    사용자에 직접 노출되어 있지 않고, 사용자 닫힌 경로 확인 로직에서 호출 처리
    :param event: body에 사용자가 각 타일에 획득한 포인트 정보를 담음
    :param context: 미사용
    """
    print(f"{event}")

    data = json.loads(event.get("body")).get("tiles")

    tiles = [utils.TilePoint(tile) for tile in data]

    utils.add_user_tiles_points(tiles)

    utils.update_land_tiles(tiles)

if __name__ == "__main__":
    event = {
        "authorizationToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY5NGNmYTAxOTgyMDNlMjgwN2Q4MzRkYmE2MjBlZjczZjI4ZTRlMmMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2V0bGFuZG9uZm9vdCIsImF1ZCI6ImdldGxhbmRvbmZvb3QiLCJhdXRoX3RpbWUiOjE2MzY0MTIyMTAsInVzZXJfaWQiOiJFN0pxRE5CY0dPZllld3V2SjJKdTh1b2hQa3AyIiwic3ViIjoiRTdKcUROQmNHT2ZZZXd1dkoySnU4dW9oUGtwMiIsImlhdCI6MTYzNjQxMjIyNCwiZXhwIjoxNjM2NDE1ODI0LCJlbWFpbCI6InByaWRla2tAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInByaWRla2tAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.AXbvt6N-SMHi4dYYPBUYlohqsJLFw9yUy3krWfrVaF4Rmo1kmQOc8j_CaAQDjJ4VPOdp3WP3uGp-NRjcVtH1bge5my2i7R9UjztIBuWGOOQoOOyuSOC2zOZ9OBU4m-lVH9ZIzDg1z-8SRX9RtZuUaU-9axxYobrIqnpgdqEl0muogck-4-cQPhCu-Gr_5DvZvlDPZRgO4EHBFMaLJo48QsuAN9mdo6Uns_7a66wZVt-P-Klw3MLBH9SfM2fxJUj0XlTWwrLwooTJhEmvl0aIzFD19l6HNUYyL7TQDicjasf10U23YMauIodqUrwDLw1DxVHW4GJz55bAi9VdSsgDXg",
        "body": json.dumps({
            "tiles":
                [
                    {
                        "x": 223110,
                        "y": 110001,
                        "user_id":"FE89CeUI8Uh9vdxWGYCj3K3OIXD3",
                        "gained_point": 2
                    },
                    {
                        "x": 219999,
                        "y": 101530,
                        "user_id": "FE89CeUI8Uh9vdxWGYCj3K3OIXD3",
                        "gained_point": 1
                    },
                    {
                        "x": 219999,
                        "y": 101530,
                        "user_id": "FE89CeUI8Uh9vdxWGYCj3K3OIXD3",
                        "gained_point": 10
                    }
                    ,
                    {
                        "x": 219998,
                        "y": 101530,
                        "user_id": "FE89CeUI8Uh9vdxWGYCj3K3OIXD3",
                        "gained_point": 5
                    }
                ]
        })

    }
    print(lambda_handler(event, None))
