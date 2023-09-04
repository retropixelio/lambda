import jwt
import requests
from datetime import datetime

from conf import settings
from domain.device import Device

epoch_time = datetime(1970, 1, 1)
iat = int((datetime.utcnow() - epoch_time).total_seconds())

credentials = {
  "iss": "firebase-adminsdk-k11uo@retropixel-396819.iam.gserviceaccount.com",
  "scope": "https://www.googleapis.com/auth/homegraph",
  "aud": "https://oauth2.googleapis.com/token",
  "exp": iat + 3600,
  "iat": iat
}

secret = "-----BEGIN PRIVATE KEY-----\n" + settings.PRIVATE_KEY.replace("\\n", "\n") + "\n-----END PRIVATE KEY-----\n"
code = jwt.encode(credentials, secret.encode("utf-8"), 'RS256')

class HomeGraphRepository:
    def __init__(self):
        response = requests.post(
            'https://oauth2.googleapis.com/token',
            json={
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": code
            }
        )
        data = response.json()
        if response.ok:
            self.__token = data['access_token']
        else:
            print(data)
            raise Exception("Homegraph not authenticated")

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
        response = requests.post(
            'https://homegraph.googleapis.com/v1/devices:reportStateAndNotification',
            json={
                "agentUserId": user_id,
                "payload": {
                    "devices":{
                        "states":{
                            device.device_id:{
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
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.__token}'
            }
        )
        if not response.ok:
            message = response.json()
            raise Exception(message["error"]["message"])