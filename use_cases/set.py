from firebase_admin import db
import jwt

from conf import settings
from repos.mqtt import Mqtt
from repos.response import response_object

mqtt = Mqtt()

def set_post(headers, args):
    token = headers.get('authorization')[7:]
    user = jwt.decode(token, settings.SECRET, algorithms=["HS256"])
    if user.get("token_type") == "access": 
        topic = args.get('topic')
        payload = args.get('payload')
        id = topic.split('/')[0]
        mqtt.publish(topic,payload)
        if topic.split('/')[1] == "OnOff":
            #socketio.emit(id,{"branch":"OnOff","id":id,"state":True if payload == "true" else False})
            ref = db.reference(f'Devices/{id}/OnOff')
            ref.set({'on':True if payload == "true" else False})
        if topic.split('/')[1] == "Color":
            #socketio.emit(id,{"branch":"Color","id":id,"state":int(payload)})
            ref = db.reference(f'Devices/{id}/ColorSetting')
            ref.set({'color':{"spectrumRGB":int(payload)}})
        # ref = db.reference(f'Devices/{id}')
        # Online = ref.get()
        # if not Online:
        #     socketio.emit(id,{"branch":"Online","id":id,"state":False})
        #     socketio.emit(id,{"branch":"OnOff","id":id,"state":False})
        return response_object({topic:payload},200)
    return response_object({'message','Invalid token'}, 401)