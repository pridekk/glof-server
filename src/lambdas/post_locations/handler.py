import json


def lambda_handler(event, context):
    print(f"{event}")

    locations = json.loads(event['body']).get('locations', [])

    return {
        'statusCode': 200,
        'body': json.dumps({"message": f"{len(locations)} inserted"}, ensure_ascii=False)
    }


if __name__ == "__main__":
    event = {
        "authorizationToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY5NGNmYTAxOTgyMDNlMjgwN2Q4MzRkYmE2MjBlZjczZjI4ZTRlMmMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2V0bGFuZG9uZm9vdCIsImF1ZCI6ImdldGxhbmRvbmZvb3QiLCJhdXRoX3RpbWUiOjE2MzY0MTIyMTAsInVzZXJfaWQiOiJFN0pxRE5CY0dPZllld3V2SjJKdTh1b2hQa3AyIiwic3ViIjoiRTdKcUROQmNHT2ZZZXd1dkoySnU4dW9oUGtwMiIsImlhdCI6MTYzNjQxMjIyNCwiZXhwIjoxNjM2NDE1ODI0LCJlbWFpbCI6InByaWRla2tAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInByaWRla2tAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.AXbvt6N-SMHi4dYYPBUYlohqsJLFw9yUy3krWfrVaF4Rmo1kmQOc8j_CaAQDjJ4VPOdp3WP3uGp-NRjcVtH1bge5my2i7R9UjztIBuWGOOQoOOyuSOC2zOZ9OBU4m-lVH9ZIzDg1z-8SRX9RtZuUaU-9axxYobrIqnpgdqEl0muogck-4-cQPhCu-Gr_5DvZvlDPZRgO4EHBFMaLJo48QsuAN9mdo6Uns_7a66wZVt-P-Klw3MLBH9SfM2fxJUj0XlTWwrLwooTJhEmvl0aIzFD19l6HNUYyL7TQDicjasf10U23YMauIodqUrwDLw1DxVHW4GJz55bAi9VdSsgDXg",

    }
    print(lambda_handler(event, None))
