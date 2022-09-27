import json
from firebase_admin import credentials
import firebase_admin

from use_cases.login import login_post
from use_cases.refresh import refresh_post
from use_cases.google import smarthome
from repos.response import response_object

cred = credentials.Certificate("service-account.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://retropixel-8f415-default-rtdb.firebaseio.com/'
})

def lambda_handler(event, context):
    body = json.loads(event['body']) if event.get('body') else {}
    path = event['path']
    method = event['httpMethod']
    query = event['queryStringParameters']
    headers = event['headers']
    if path == '/default/RetroPixelApi/login':
        return login_post(body)
    if path == '/default/RetroPixelApi/refresh':
        return refresh_post(query)
    if path == '/default/RetroPixelApi/smarthome':
        return smarthome(headers, body)
    return response_object(event, 200)
