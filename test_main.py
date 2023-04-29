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
    token = jwt.encode({"token_type": "access","user": "164521328368ddfbf9eac4cc94","exp":datetime.datetime.now() + datetime.timedelta(hours=24)}, settings.SECRET, algorithm="HS256")
    refresh = jwt.encode({"token_type": "refresh","user": "164521328368ddfbf9eac4cc94"}, settings.SECRET, algorithm="HS256")
    device = 'LIGHTlf8yRystroNXcuyXDX5pDw'

    def test_login(self):
        login_object = request_object(
            '/default/RetroPixelApi/login', 
            method = 'POST', 
            body = {'userid':'andres64372@hotmail.com', 'password': 'medellin1998'}
        )
        response = lambda_handler(login_object, None)
        assert response['statusCode'] == 201

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
            method = 'GET', 
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
        assert response['statusCode'] == 201

    # def test_smarthome_sync(self):
    #     smarthome_object = request_object(
    #         '/default/RetroPixelApi/smarthome',
    #         body={
    #             "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
    #             "inputs": [{
    #             "intent": "action.devices.SYNC"
    #             }]
    #         },
    #         authorization= f'Bearer {self.token}'
    #     )
    #     response = lambda_handler(smarthome_object, None)
    #     assert response['statusCode'] == 200
    
    # def test_smarthome_query(self):
    #     smarthome_object = request_object(
    #         '/default/RetroPixelApi/smarthome',
    #         body={
    #             "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
    #             "inputs": [{
    #             "intent": "action.devices.QUERY",
    #             "payload": {
    #                 "devices": [{
    #                     "id": self.device
    #                 }]
    #             }
    #             }]
    #         },
    #         authorization= f'Bearer {self.token}'
    #     )
    #     response = lambda_handler(smarthome_object, None)
    #     assert response['statusCode'] == 200

    # def test_smarthome_execute_onoff(self):
    #     smarthome_object = request_object(
    #         '/default/RetroPixelApi/smarthome',
    #         body={
    #             "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
    #             "inputs": [{
    #             "intent": "action.devices.EXECUTE",
    #             "payload": {
    #                 "commands": [{
    #                     "devices": [{
    #                         "id": self.device,
    #                     }],
    #                     "execution": [{
    #                         "command": "action.devices.commands.OnOff",
    #                         "params": {
    #                             "on": True
    #                         }
    #                     }]
    #                 }]
    #             }
    #             }]
    #         },
    #         authorization= f'Bearer {self.token}'
    #     )
    #     response = lambda_handler(smarthome_object, None)
    #     result = {
    #         "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
    #         "payload": {
    #             "commands": [{
    #                 "ids": [
    #                     self.device
    #                 ],
    #                 "status": "SUCCESS",
    #                 "states": {
    #                     "on": True,
    #                     "online": True
    #                 }
    #             }]
    #         }
    #     }
    #     assert json.loads(response['body']) == result

    # def test_smarthome_execute_color(self):
    #     smarthome_object = request_object(
    #         '/default/RetroPixelApi/smarthome',
    #         body={
    #             "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
    #             "inputs": [{
    #             "intent": "action.devices.EXECUTE",
    #             "payload": {
    #                 "commands": [{
    #                     "devices": [{
    #                         "id": self.device,
    #                     }],
    #                     "execution": [{
    #                         "command": "action.devices.commands.ColorAbsolute",
    #                         "params": {
    #                             "color": {
    #                                 "spectrumRGB": 16777215
    #                             }
    #                         }
    #                     }]
    #                 }]
    #             }
    #             }]
    #         },
    #         authorization= f'Bearer {self.token}'
    #     )
    #     response = lambda_handler(smarthome_object, None)
    #     result = {
    #         "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
    #         "payload": {
    #             "commands": [{
    #                 "ids": [
    #                     self.device
    #                 ],
    #                 "status": "SUCCESS",
    #                 "states": {
    #                     "color":{
    #                         "spectrumRGB": 16777215
    #                     },
    #                     "online": True
    #                 }
    #             }]
    #         }
    #     }
    #     assert json.loads(response['body']) == result
