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


def lambda_handler(event, context):
    token = event['authorizationToken']
    print(f"Client token: {token}")

    try:
        decoded_token = auth.verify_id_token(token.replace("Bearer ", ""))
    except Exception as e:
        print(e)
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
    policy.allowMethod(HttpVerb.POST, "/*/locations")

    authResponse = policy.build()

    context = {
        'key': 'value',  # $context.authorizer.key -> value
        'number': 1,
        'bool': True
    }

    authResponse['context'] = context

    return authResponse


if __name__ == "__main__":
    event = {
        "authorizationToken": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjcxMTQzNzFiMmU4NmY4MGM1YzYxNThmNDUzYzk0NTEyNmZlNzM5Y2MiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2V0bGFuZG9uZm9vdCIsImF1ZCI6ImdldGxhbmRvbmZvb3QiLCJhdXRoX3RpbWUiOjE2NDA2NDM4MjksInVzZXJfaWQiOiJFN0pxRE5CY0dPZllld3V2SjJKdTh1b2hQa3AyIiwic3ViIjoiRTdKcUROQmNHT2ZZZXd1dkoySnU4dW9oUGtwMiIsImlhdCI6MTY0MDY0MzgyOSwiZXhwIjoxNjQwNjQ3NDI5LCJlbWFpbCI6InByaWRla2tAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInByaWRla2tAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.gx_y1ihqrzEChCdnUGOdXkD981pPHyx3pY8HnL7joJT1wiIczLKUVKX8L8U5FYWw_JT4ZTAWdoi91KW7TTO_hp3xAXkKgwnmUZ7Vkdfaw-3tLh03eoTtLR0DmBkf9-qTdUczvWs2-Fd6WBhOdNGWx551Dttbd6iQP3ArLZ4svS3dJyToSIm40RwhhcYT_knAawoJbmIJzsAQb0M_HNsfXc1l4xNyN7Ou5UZ4b3g3qKr-b20Q3Tn3LjZ7UXcfZA5MPVIsywCRhQs-GYATQrszlTmvF1INhPrfU3yNjTNWEXFJWsKfFn0F4km9_tAx6Kr6gPgGNsfCRLMlB0lQjUjMGQ",
        "methodArn": "arn:aws:execute-api:ap-northeast-2:565651431982:pagizbj9h1/*/GET/corporates/summary"
    }
    print(lambda_handler(event, None))
