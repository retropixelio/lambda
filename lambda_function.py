import json
from firebase_admin import credentials
import firebase_admin
from jinja2 import Environment, FileSystemLoader
import os
import base64
from urllib.parse import parse_qs

from use_cases.login import login_post
from use_cases.refresh import refresh_post
from use_cases.google import smarthome
from use_cases.set import set_post
from use_cases.devices import devices_get
from use_cases.query import query_get
from use_cases.auth import auth_get, auth_post
from use_cases.token import token_post
from use_cases.iot import connected
from repos.response import response_object

cred = credentials.Certificate("service-account.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://retropixel-8f415-default-rtdb.firebaseio.com/'
})

def lambda_handler(event, context):
    if event.get('eventType'):
        return connected(event)
    path = event['path']
    method = event['httpMethod']
    query = event['queryStringParameters']
    headers = event['headers']
    if headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        body = event['body']
    else:
        body = json.loads(event['body']) if event.get('body') else {}
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
            return refresh_post(body)
    if path == '/default/RetroPixelApi/smarthome':
        return smarthome(headers, body)
    if path == '/default/RetroPixelApi/set':
        if method == 'POST':
            return set_post(headers, body)
    if path == '/default/RetroPixelApi/devices':
        if method == 'GET':
            return devices_get(headers)
    if path == '/default/RetroPixelApi/query':
        if method == 'GET':
            return query_get(headers, query)
    if path == '/default/RetroPixelApi/token':
        if method == 'POST':
            out = base64.b64decode(body).decode('utf-8')
            form = parse_qs(out)
            return token_post(form)
    if path == '/default/RetroPixelApi/auth':
        environment = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"), encoding="utf-8"))
        template = environment.get_template('login.html')
        if method == 'GET':
            return auth_get(template)
        if method == 'POST':
            out = base64.b64decode(body).decode('utf-8')
            form = parse_qs(out)
            return auth_post(template, form, query)
    return response_object(event, 404)
