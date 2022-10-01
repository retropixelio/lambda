import json
import pytest
import jwt
import datetime

from conf import settings
from lambda_function import lambda_handler

def request_object(path, method = 'GET', authorization = None, query = None, body = None):
    return {
        "path": path,
        "httpMethod": method,
        "headers": {
            'Content-Type': 'application/json',
            'authorization': authorization
        },
        "queryStringParameters": query,
        "body": json.dumps(body),
    }

class TestGlobal:
    token = jwt.encode({"token_type": "access","user": "2F164521328368ddfbf9eac4cc94","exp":datetime.datetime.now() + datetime.timedelta(hours=24)}, settings.SECRET, algorithm="HS256")
    refresh = jwt.encode({"token_type": "refresh","user": "2F164521328368ddfbf9eac4cc94"}, settings.SECRET, algorithm="HS256")
    device = 'LIGHT_aznnl6JAJUxIyPFKgGDEA'

    def test_login(self):
        login_object = request_object(
            '/default/RetroPixelApi/login', 
            method = 'POST', 
            body = {'userid':'andres64372@hotmail.com', 'password': 'medellin1998'}
        )
        response = lambda_handler(login_object, None)
        assert response['statusCode'] == 200

    def test_refresh_fail(self):
        refresh_object = request_object(
            '/default/RetroPixelApi/refresh', 
            method = 'POST', 
            body = {'token': self.token}
        )
        response = lambda_handler(refresh_object, None)
        assert response['statusCode'] == 400
    
    def test_refresh_success(self):
        refresh_object = request_object(
            '/default/RetroPixelApi/refresh', 
            method = 'POST', 
            body = {'token': self.refresh}
        )
        response = lambda_handler(refresh_object, None)
        assert response['statusCode'] == 201
    
    def test_devices(self):
        refresh_object = request_object(
            '/default/RetroPixelApi/devices',
            authorization= f'Bearer {self.token}'
        )
        response = lambda_handler(refresh_object, None)
        assert response['statusCode'] == 200

    def test_query(self):
        refresh_object = request_object(
            '/default/RetroPixelApi/query',
            query={'device':self.device},
            authorization= f'Bearer {self.token}'
        )
        response = lambda_handler(refresh_object, None)
        assert response['statusCode'] == 200

    def test_set(self):
        refresh_object = request_object(
            '/default/RetroPixelApi/set',
            method = 'POST', 
            body=[{
                'topic': f"{self.device}/OnOff",
                'payload': 'true'
            }],
            authorization= f'Bearer {self.token}'
        )
        response = lambda_handler(refresh_object, None)
        assert response['statusCode'] == 200
        
