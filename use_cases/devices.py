from firebase_admin import db
import jwt

from conf import settings
from repos.response import response_object

def devices_get(headers):
    token = headers.get('authorization')[7:]
    user = jwt.decode(token, settings.SECRET, algorithms=["HS256"])
    user = user["user"]
    ref = db.reference(f'Users/{user}/devices')
    devices = ref.get()
    if not devices: 
        return response_object({'list':[],'states':{}},200)
    device_list = []
    device_states = {}
    for device in devices:
        device_list.append(device["id"])
        ref = db.reference(f'Devices/{device["id"]}')
        data = ref.get()
        if not data:
            ref.set(
                {
                    "ColorSetting":{"color":{"spectrumRGB":16777215}},
                    "OnOff":{"on":False},
                    "Online":{"online":False},
                }
            )
            device_states.update({device["id"]:{
                "name": device["nickname"],
                "OnOff":False,
                "Online":False,
                "Color":16777215
            }})
        else:
            OnOff = data['OnOff']["on"]
            Online = data['Online']["online"]
            Color = data["ColorSetting"]["color"]["spectrumRGB"] if data["ColorSetting"]["color"].get('spectrumRGB') else 16777215
            device_states.update({device["id"]:{
                "name": device["nickname"],
                "OnOff":OnOff,
                "Online":Online,
                "Color":int(Color)
            }})
    return response_object({'list':device_list,'states':device_states},200)