import json
import jwt
import datetime
from unittest.mock import patch
import bcrypt
from urllib.parse import urlencode
import base64

from conf import settings
from lambda_function import lambda_handler
from domain.user import User, UserDevice
from domain.device import Device

user_id = "164521328368ddfbf9eac4cc94"
email = "andres64372@hotmail.com"
password = "medellin1998"
device_id = "LIGHTlf8yRystroNXcuyXDX5pDw"

fisical = [device_id]

class MockMqtt:
    def __init__(self):
        pass

    def publish(self, *_):
        pass

device = Device.from_dict({
    'OnOff': {
        'on': True
    },
    'ColorSetting': {
        'color':{
            'name': 'color',
            'spectrumRGB': 0
        }
    },
    'Online': {
        'online': True
    }
})

devices = [UserDevice(
    id = '1',
    nickname = 'device',
    room = 'room',
)]

user = user_id, User(
    active = True,
    devices = devices,
    email = email,
    name = 'Andres',
    last = 'Herrera',
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
)

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

def get_user_by_email(id):
    if id == email:
        return user
    else:
        return (None, None)

@patch("repos.mqtt.Mqtt.publish", return_value=None)
@patch("repos.firebase.FirebaseRepository.get_user_by_email", side_effect=get_user_by_email)
@patch("repos.firebase.FirebaseRepository.get_user_devices", return_value=devices)
@patch("repos.firebase.FirebaseRepository.get_device", return_value=device)
@patch("repos.firebase.FirebaseRepository.get_fisical", return_value=fisical)
@patch("repos.firebase.FirebaseRepository.set_state", return_value=None)
@patch("repos.firebase.FirebaseRepository.update_state", return_value=None)
class TestGlobal:
    token = jwt.encode({"token_type": "access","user": user_id,"exp":datetime.datetime.now() + datetime.timedelta(hours=24)}, settings.SECRET, algorithm="HS256")
    refresh = jwt.encode({"token_type": "refresh","user": user_id}, settings.SECRET, algorithm="HS256")
    device = device_id

    def test_auth(self, *_):
        login_object = request_object(
            '/default/RetroPixelApi/auth', 
            query={
                'client_id': 'andres64372', 
                'redirect_uri': 'https://oauth-redirect.googleusercontent.com/r/retropixel-8f415', 
                'response_type': 'code', 
                'state': 'AEZvaVHDPEYOEoMZ5cbhFp2RJxaNZXHNaomAjuNx2h_wLbjqCFkQQFIQNvRRI1TTSnkQK9MRIoZ_vfH5ijm4oUXK1qR0nHcWRrBgw9HAIcrBP2O5oeE02LTI8uQtlkOHle1zZFGWn7fil0yKipP1GsSNPsXzmpU7onguAaO3lL-Fj3HPlTpAj23NKXBC7_yOV1jDMN10cUpkv8iXpmFXZRdovBV9ikYwTI8oXCbVntmwVEZjtqxrlv5dZd87a5Klx_bNa9TUehj66ujCQJnv9zVuZL-vARZZZXEFxEXiR099XtXlY7Sc-WOFI-8h22Mh5TqA7AjMbiGgAuDcHugGETCq9k-8asjN52IypfJLVSOC7oBfHIx3bA_tccG49nlZVNpg886NT1P-yAvVcmR9QR9Kz8NP_jt2_vgO21h31n2KyTNiWBn63IGN8_iG8FNmICkUBj3iVHgeYnE1SBsV3sf4deiqlzA2GzB5f-5J4vs1gKfPdqH71dpK4pd_sz6j2jXAMlVBSAA_J_fJRyfzkIbFac4y5zY3lKvjQy44GvneGpDCABvNHw9gbv3pIm28yJEanCsJzEUlzopo4jFvDCftneEawa-RR63cAPH9WtSs6-9aGU4UZFgltiP-fuT_hipK1Q_FdahcU8_zgIjCBSG0PyP5cILh39rf1tSPenscKan6mmdx6Ck'
            }, 
            body = 'dXNlcmlkPWFuZHJlczY0MzcyJTQwaG90bWFpbC5jb20mcGFzc3dvcmQ9bWVkZWxsaW4xOTk4'
        )
        response = lambda_handler(login_object, None)
        assert response['statusCode'] == 200

    def test_auth_post(self, *_):
        form = {'userid': [email], 'password': [password]}
        body = base64.b64encode(urlencode(form, doseq=True).encode('utf-8')).decode('utf-8')
        login_object = request_object(
            '/default/RetroPixelApi/auth', 
            method = 'POST',
            query={
                'client_id': 'andres64372', 
                'redirect_uri': 'https://oauth-redirect.googleusercontent.com/r/retropixel-8f415', 
                'response_type': 'code', 
                'state': 'AEZvaVHDPEYOEoMZ5cbhFp2RJxaNZXHNaomAjuNx2h_wLbjqCFkQQFIQNvRRI1TTSnkQK9MRIoZ_vfH5ijm4oUXK1qR0nHcWRrBgw9HAIcrBP2O5oeE02LTI8uQtlkOHle1zZFGWn7fil0yKipP1GsSNPsXzmpU7onguAaO3lL-Fj3HPlTpAj23NKXBC7_yOV1jDMN10cUpkv8iXpmFXZRdovBV9ikYwTI8oXCbVntmwVEZjtqxrlv5dZd87a5Klx_bNa9TUehj66ujCQJnv9zVuZL-vARZZZXEFxEXiR099XtXlY7Sc-WOFI-8h22Mh5TqA7AjMbiGgAuDcHugGETCq9k-8asjN52IypfJLVSOC7oBfHIx3bA_tccG49nlZVNpg886NT1P-yAvVcmR9QR9Kz8NP_jt2_vgO21h31n2KyTNiWBn63IGN8_iG8FNmICkUBj3iVHgeYnE1SBsV3sf4deiqlzA2GzB5f-5J4vs1gKfPdqH71dpK4pd_sz6j2jXAMlVBSAA_J_fJRyfzkIbFac4y5zY3lKvjQy44GvneGpDCABvNHw9gbv3pIm28yJEanCsJzEUlzopo4jFvDCftneEawa-RR63cAPH9WtSs6-9aGU4UZFgltiP-fuT_hipK1Q_FdahcU8_zgIjCBSG0PyP5cILh39rf1tSPenscKan6mmdx6Ck'
            }, 
            body = body
        )
        response = lambda_handler(login_object, None)
        assert response['statusCode'] == 301

    def test_auth_post_email(self, *_):
        form = {'userid': ['fake'], 'password': [password]}
        body = base64.b64encode(urlencode(form, doseq=True).encode('utf-8')).decode('utf-8')
        login_object = request_object(
            '/default/RetroPixelApi/auth', 
            method = 'POST',
            query={
                'client_id': 'andres6437', 
                'redirect_uri': 'https://oauth-redirect.googleusercontent.com/r/retropixel-8f415', 
                'response_type': 'code', 
                'state': 'AEZvaVHDPEYOEoMZ5cbhFp2RJxaNZXHNaomAjuNx2h_wLbjqCFkQQFIQNvRRI1TTSnkQK9MRIoZ_vfH5ijm4oUXK1qR0nHcWRrBgw9HAIcrBP2O5oeE02LTI8uQtlkOHle1zZFGWn7fil0yKipP1GsSNPsXzmpU7onguAaO3lL-Fj3HPlTpAj23NKXBC7_yOV1jDMN10cUpkv8iXpmFXZRdovBV9ikYwTI8oXCbVntmwVEZjtqxrlv5dZd87a5Klx_bNa9TUehj66ujCQJnv9zVuZL-vARZZZXEFxEXiR099XtXlY7Sc-WOFI-8h22Mh5TqA7AjMbiGgAuDcHugGETCq9k-8asjN52IypfJLVSOC7oBfHIx3bA_tccG49nlZVNpg886NT1P-yAvVcmR9QR9Kz8NP_jt2_vgO21h31n2KyTNiWBn63IGN8_iG8FNmICkUBj3iVHgeYnE1SBsV3sf4deiqlzA2GzB5f-5J4vs1gKfPdqH71dpK4pd_sz6j2jXAMlVBSAA_J_fJRyfzkIbFac4y5zY3lKvjQy44GvneGpDCABvNHw9gbv3pIm28yJEanCsJzEUlzopo4jFvDCftneEawa-RR63cAPH9WtSs6-9aGU4UZFgltiP-fuT_hipK1Q_FdahcU8_zgIjCBSG0PyP5cILh39rf1tSPenscKan6mmdx6Ck'
            }, 
            body = body
        )
        response = lambda_handler(login_object, None)
        assert response['statusCode'] == 200

    def test_auth_post_pwd(self, *_):
        form = {'userid': [email], 'password': ['fake']}
        body = base64.b64encode(urlencode(form, doseq=True).encode('utf-8')).decode('utf-8')
        login_object = request_object(
            '/default/RetroPixelApi/auth', 
            method = 'POST',
            query={
                'client_id': 'andres6437', 
                'redirect_uri': 'https://oauth-redirect.googleusercontent.com/r/retropixel-8f415', 
                'response_type': 'code', 
                'state': 'AEZvaVHDPEYOEoMZ5cbhFp2RJxaNZXHNaomAjuNx2h_wLbjqCFkQQFIQNvRRI1TTSnkQK9MRIoZ_vfH5ijm4oUXK1qR0nHcWRrBgw9HAIcrBP2O5oeE02LTI8uQtlkOHle1zZFGWn7fil0yKipP1GsSNPsXzmpU7onguAaO3lL-Fj3HPlTpAj23NKXBC7_yOV1jDMN10cUpkv8iXpmFXZRdovBV9ikYwTI8oXCbVntmwVEZjtqxrlv5dZd87a5Klx_bNa9TUehj66ujCQJnv9zVuZL-vARZZZXEFxEXiR099XtXlY7Sc-WOFI-8h22Mh5TqA7AjMbiGgAuDcHugGETCq9k-8asjN52IypfJLVSOC7oBfHIx3bA_tccG49nlZVNpg886NT1P-yAvVcmR9QR9Kz8NP_jt2_vgO21h31n2KyTNiWBn63IGN8_iG8FNmICkUBj3iVHgeYnE1SBsV3sf4deiqlzA2GzB5f-5J4vs1gKfPdqH71dpK4pd_sz6j2jXAMlVBSAA_J_fJRyfzkIbFac4y5zY3lKvjQy44GvneGpDCABvNHw9gbv3pIm28yJEanCsJzEUlzopo4jFvDCftneEawa-RR63cAPH9WtSs6-9aGU4UZFgltiP-fuT_hipK1Q_FdahcU8_zgIjCBSG0PyP5cILh39rf1tSPenscKan6mmdx6Ck'
            }, 
            body = body
        )
        response = lambda_handler(login_object, None)
        assert response['statusCode'] == 200

    def test_token_auth(self, *_):
        form = {'grant_type': ['authorization_code'], 'code': [self.token]}
        body = base64.b64encode(urlencode(form, doseq=True).encode('utf-8')).decode('utf-8')
        login_object = request_object(
            '/default/RetroPixelApi/token', 
            method = 'POST',
            body = body
        )
        response = lambda_handler(login_object, None)
        assert response['statusCode'] == 200
    
    def test_token_refresh(self, *_):
        form = {'grant_type': ['refresh_token'], 'refresh_token': [self.refresh]}
        body = base64.b64encode(urlencode(form, doseq=True).encode('utf-8')).decode('utf-8')
        login_object = request_object(
            '/default/RetroPixelApi/token', 
            method = 'POST',
            body = body
        )
        response = lambda_handler(login_object, None)
        assert response['statusCode'] == 200

    def test_login(self, *_):
        login_object = request_object(
            '/default/RetroPixelApi/login', 
            method = 'POST', 
            body = {'userid':'andres64372@hotmail.com', 'password': password}
        )
        response = lambda_handler(login_object, None)
        assert response['statusCode'] == 201

    def test_refresh_fail(self, *_):
        refresh_object = request_object(
            '/default/RetroPixelApi/refresh', 
            method = 'POST', 
            body = {'token': self.token}
        )
        response = lambda_handler(refresh_object, None)
        assert response['statusCode'] == 400
    
    def test_refresh_success(self, *_):
        refresh_object = request_object(
            '/default/RetroPixelApi/refresh', 
            method = 'POST', 
            body = {'token': self.refresh}
        )
        response = lambda_handler(refresh_object, None)
        assert response['statusCode'] == 201
    
    def test_devices(self, *_):
        refresh_object = request_object(
            '/default/RetroPixelApi/devices',
            method = 'GET', 
            authorization= f'Bearer {self.token}'
        )
        response = lambda_handler(refresh_object, None)
        assert response['statusCode'] == 200

    def test_query(self, *_):
        refresh_object = request_object(
            '/default/RetroPixelApi/query',
            query={'device':self.device},
            authorization= f'Bearer {self.token}'
        )
        response = lambda_handler(refresh_object, None)
        assert response['statusCode'] == 200

    def test_set(self, *args):
        refresh_object = request_object(
            '/default/RetroPixelApi/set',
            method = 'POST', 
            body=[{
                'id': self.device,
                'state': {
                    'deviceId': self.device,
                    'onoff': True
                }
            }],
            authorization= f'Bearer {self.token}'
        )
        response = lambda_handler(refresh_object, None)
        args[-1].assert_called_with(self.device, json.dumps({'deviceId': self.device,'onoff': True}))
        assert response['statusCode'] == 201

    def test_smarthome_sync(self, *_):
        smarthome_object = request_object(
            '/default/RetroPixelApi/smarthome',
            method='POST',
            body={
                "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
                "inputs": [{
                "intent": "action.devices.SYNC"
                }]
            },
            authorization= f'Bearer {self.token}'
        )
        response = lambda_handler(smarthome_object, None)
        assert response['statusCode'] == 200
  
    def test_smarthome_query(self, *_):
        smarthome_object = request_object(
            '/default/RetroPixelApi/smarthome',
            method='POST',
            body={
                "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
                "inputs": [{
                "intent": "action.devices.QUERY",
                "payload": {
                    "devices": [{
                        "id": self.device
                    }]
                }
                }]
            },
            authorization= f'Bearer {self.token}'
        )
        response = lambda_handler(smarthome_object, None)
        assert response['statusCode'] == 200

    def test_smarthome_execute_onoff(self, *_):
        smarthome_object = request_object(
            '/default/RetroPixelApi/smarthome',
            method='POST',
            body={
                "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
                "inputs": [{
                "intent": "action.devices.EXECUTE",
                "payload": {
                    "commands": [{
                        "devices": [{
                            "id": self.device,
                        }],
                        "execution": [{
                            "command": "action.devices.commands.OnOff",
                            "params": {
                                "on": True
                            }
                        }]
                    }]
                }
                }]
            },
            authorization= f'Bearer {self.token}'
        )
        response = lambda_handler(smarthome_object, None)
        result = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "payload": {
                "commands": [{
                    "ids": [
                        self.device
                    ],
                    "status": "SUCCESS",
                    "states": {
                        "on": True,
                        "online": True
                    }
                }]
            }
        }
        assert json.loads(response['body']) == result

    def test_smarthome_execute_color(self, *_):
        smarthome_object = request_object(
            '/default/RetroPixelApi/smarthome',
            method='POST',
            body={
                "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
                "inputs": [{
                "intent": "action.devices.EXECUTE",
                "payload": {
                    "commands": [{
                        "devices": [{
                            "id": self.device,
                        }],
                        "execution": [{
                            "command": "action.devices.commands.ColorAbsolute",
                            "params": {
                                "color": {
                                    "spectrumRGB": 16777215
                                }
                            }
                        }]
                    }]
                }
                }]
            },
            authorization= f'Bearer {self.token}'
        )
        response = lambda_handler(smarthome_object, None)
        result = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "payload": {
                "commands": [{
                    "ids": [
                        self.device
                    ],
                    "status": "SUCCESS",
                    "states": {
                        "color":{
                            "spectrumRGB": 16777215
                        },
                        "online": True
                    }
                }]
            }
        }
        assert json.loads(response['body']) == result

    def test_state(self, *_):
        smarthome_object = {
            'deviceId': self.device,
            'onoff': True
        }
        response = lambda_handler(smarthome_object, None)
        assert response == None
