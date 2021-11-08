import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import json
import boto3
from utils import HttpVerb, AuthPolicy

params = boto3.client('ssm', 'us-east-1').get_parameter(Name='/glof/dev/firebase_service_key', WithDecryption=True)
service_key = json.loads(params.get('Parameter').get('Value'))

cred = credentials.Certificate(service_key)
firebase_admin.initialize_app(cred)


def handler(event, context):
    token = event['authorizationToken']
    print(f"Client token: {token}")

    try:
        decoded_token = auth.verify_id_token(token)
    except Exception as e:
        raise Exception("Unauthorized")

    principalId = decoded_token.get("user_id")

    tmp = event['methodArn'].split(':')
    apiGatewayArnTmp = tmp[5].split('/')
    awsAccountId = tmp[4]

    policy = AuthPolicy(principalId, awsAccountId)
    policy.restApiId = apiGatewayArnTmp[0]
    policy.region = tmp[3]
    policy.stage = apiGatewayArnTmp[1]
    policy.allowMethod(HttpVerb.GET, "/*")

    authResponse = policy.build()

    context = {
        'key': 'value',  # $context.authorizer.key -> value
        'number': 1,
        'bool': True
    }
    # context['arr'] = ['foo'] <- this is invalid, APIGW will not accept it
    # context['obj'] = {'foo':'bar'} <- also invalid

    authResponse['context'] = context

    return authResponse


if __name__ == "__main__":
    event = {
        "authorizationToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY5NGNmYTAxOTgyMDNlMjgwN2Q4MzRkYmE2MjBlZjczZjI4ZTRlMmMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2V0bGFuZG9uZm9vdCIsImF1ZCI6ImdldGxhbmRvbmZvb3QiLCJhdXRoX3RpbWUiOjE2MzY0MTIyMTAsInVzZXJfaWQiOiJFN0pxRE5CY0dPZllld3V2SjJKdTh1b2hQa3AyIiwic3ViIjoiRTdKcUROQmNHT2ZZZXd1dkoySnU4dW9oUGtwMiIsImlhdCI6MTYzNjQxMjIyNCwiZXhwIjoxNjM2NDE1ODI0LCJlbWFpbCI6InByaWRla2tAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInByaWRla2tAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.AXbvt6N-SMHi4dYYPBUYlohqsJLFw9yUy3krWfrVaF4Rmo1kmQOc8j_CaAQDjJ4VPOdp3WP3uGp-NRjcVtH1bge5my2i7R9UjztIBuWGOOQoOOyuSOC2zOZ9OBU4m-lVH9ZIzDg1z-8SRX9RtZuUaU-9axxYobrIqnpgdqEl0muogck-4-cQPhCu-Gr_5DvZvlDPZRgO4EHBFMaLJo48QsuAN9mdo6Uns_7a66wZVt-P-Klw3MLBH9SfM2fxJUj0XlTWwrLwooTJhEmvl0aIzFD19l6HNUYyL7TQDicjasf10U23YMauIodqUrwDLw1DxVHW4GJz55bAi9VdSsgDXg",
        "methodArn": "arn:aws:execute-api:ap-northeast-2:565651431982:pagizbj9h1/*/GET/corporates/summary"
    }
    print(handler(event, None))
