import json
import jwt
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
import datetime
from unittest.mock import patch
import bcrypt
from urllib.parse import urlencode
import base64

from conf import settings
from lambda_function import lambda_handler
from domain.user import User, UserDevice, AccessKey
from domain.device import Device
from utils.cert import generate_certificate

user_id = "andres64372@hotmail.com"
password = "medellin1998"
device_id = "1"


data = {
  "iss": "https://securetoken.google.com/retropixel-396819",
  "aud": "retropixel-396819",
  "user_id": "uG9LmlizZvWPalAgyWG70cXG8w03",
  "sub": "uG9LmlizZvWPalAgyWG70cXG8w03",
  "phone_number": "+16505551234",
  "firebase": {
    "identities": {
      "phone": [
        "+16505551234"
      ]
    },
    "sign_in_provider": "phone"
  }
}
public_key, certificate = generate_certificate()
encode = jwt.encode(data, public_key, algorithm='RS256', headers={"alg": "RS256","kid": "be7823ef01bd4d2b962741658d20807efee6de5c","typ": "JWT"})

cert_json = {
  "be7823ef01bd4d2b962741658d20807efee6de5c": certificate.decode("utf8")  
}

class MockMqtt:
    def __init__(self):
        pass

    def publish(self, *_):
        pass

device = Device.from_dict({
    "deviceId": "1",
    "online": True,
    "ip": "0.0.0.0",
    "onoff": True,
    "ambilight": True,
    "chrome": 0,
    "color": {
        "p": 16777215,
        "s": 16777215,
        "t": 16777215,
    },
    "brightness": 100,
    "speed": 1000,
})

devices = [UserDevice(
    id = '1',
    nickname = 'device',
    room = 'room',
)]

user = User(
    devices = devices,
    user_id = user_id,
)

credential = AccessKey(
    third_party_credential='abc123',
    user_id=user_id,
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

class MockRequest:
    def json():
        return cert_json

@patch("repos.mqtt.Mqtt.publish", return_value=None)
@patch("domain.authentication.requests.get", return_value=MockRequest)
@patch("repos.firebase.FirebaseRepository.get_user_info", return_value=user)
@patch("repos.firebase.FirebaseRepository.search_user", return_value=user)
@patch("repos.firebase.FirebaseRepository.set_device", return_value=None)
@patch("repos.firebase.FirebaseRepository.get_device", return_value=device)
@patch("repos.firebase.FirebaseRepository.set_state", return_value=None)
@patch("repos.firebase.FirebaseRepository.create_user", return_value=None)
@patch("repos.firebase.FirebaseRepository.update_state", return_value=None)
@patch("repos.firebase.FirebaseRepository.get_credential", return_value=credential)
@patch("repos.firebase.FirebaseRepository.delete_credential", return_value=None)
@patch("repos.homegraph.HomeGraphRepository.request_sync", return_value=None)
@patch("repos.homegraph.HomeGraphRepository.report_state", return_value=None)
class TestGlobal:
    firebase = encode
    token = jwt.encode({"token_type": "access","user_id": user_id,"exp":datetime.datetime.now() + datetime.timedelta(hours=24)}, settings.SECRET, algorithm="HS256")
    refresh = jwt.encode({"token_type": "refresh","user_id": user_id}, settings.SECRET, algorithm="HS256")
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
        form = {'access_key': ['abc123']}
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
    
    def test_devices(self, *_):
        refresh_object = request_object(
            '/default/RetroPixelApi/devices',
            method = 'GET', 
            authorization= f'Bearer {self.firebase}'
        )
        response = lambda_handler(refresh_object, None)
        assert response['statusCode'] == 200

    def test_devices(self, *_):
        refresh_object = request_object(
            '/default/RetroPixelApi/devices',
            method = 'POST',
            body = {
                'id': 'new_id',
                'nickname': 'new_nickname',
                'roon': 'new_roon',
            }, 
            authorization= f'Bearer {self.firebase}'
        )
        response = lambda_handler(refresh_object, None)
        assert response['statusCode'] == 201

    def test_query(self, *_):
        refresh_object = request_object(
            '/default/RetroPixelApi/query',
            query={'device':self.device},
            authorization= f'Bearer {self.firebase}'
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
            authorization= f'Bearer {self.firebase}'
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
