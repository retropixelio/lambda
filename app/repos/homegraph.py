import jwt
import requests
import time

from conf import settings
from domain.device import Device

iat = int(time.time())
exp = iat + 3600
credentials = {
    'iss': 'firebase-adminsdk-rnn2v@retropixel-96fca.iam.gserviceaccount.com',
    'sub': 'firebase-adminsdk-rnn2v@retropixel-96fca.iam.gserviceaccount.com',
    'aud': 'https://homegraph.googleapis.com/',
    'scope': 'https://www.googleapis.com/auth/homegraph',
    'iat': iat,
    'exp': exp
}
header = {
    'kid': '4ea10d0164c2f9ae3b870acadbbe68c1371a615d'
}
code = jwt.encode(credentials, settings.PRIVATE_KEY.replace('\\n', '\n').encode("utf-8"), 'RS256', header)

class HomeGraphRepository:
    def __init__(self):
        self.__token = code
    
    def request_sync(self, user_id):
        response = requests.post(
            'https://homegraph.googleapis.com/v1/devices:requestSync',
            json={
                "agentUserId": user_id
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.__token}'
            }
        )
        if not response.ok:
            message = response.json()
            raise Exception(message["error"]["message"])
        
    def report_state(self, user_id, device: Device):
        data = {
            "agentUserId": user_id,
            "payload": {
                "devices":{
                    "states":{
                        device.id:{
                            "on": device.onoff,
                            "online": device.online,
                            "brightness": int(device.brightness * 100 / 255),
                            "color": {
                                "spectrumRGB": device.color.p
                            }
                        }
                    }
                }
            }
        }
        response = requests.post(
            'https://homegraph.googleapis.com/v1/devices:reportStateAndNotification',
            json=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.__token}'
            }
        )
        print(response.json())
        if not response.ok:
            message = response.json()
            raise Exception(message["error"]["message"])