import json
from firebase_admin import credentials
import firebase_admin

from use_cases.login import login_post
from use_cases.refresh import refresh_post
from use_cases.google import smarthome
from use_cases.set import set_post
from use_cases.devices import devices_get
from use_cases.query import query_get
from use_cases.auth import auth_get
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
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({})
        }
    if path == '/default/RetroPixelApi/login':
        if method == 'POST':
            return login_post(body)
    if path == '/default/RetroPixelApi/refresh':
        if method == 'POST':
            return refresh_post(query)
    if path == '/default/RetroPixelApi/smarthome':
        return smarthome(headers, body)
    if path == '/default/RetroPixelApi/set':
        if method == 'POST':
            return set_post(headers, query)
    if path == '/default/RetroPixelApi/devices':
        if method == 'GET':
            return devices_get(headers)
    if path == '/default/RetroPixelApi/query':
        if method == 'GET':
            return query_get(headers, query)
    if path == '/default/RetroPixelApi/auth':
        if method == 'GET':
            return auth_get()
    return response_object(event, 404)
