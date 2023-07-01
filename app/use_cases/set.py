import json
from typing import List

from repos.firebase import FirebaseRepository
from repos.mqtt import Mqtt
from repos.response import response_object
from request_objects.set import Set

class SetUseCase:
    def __init__(self, firebase: FirebaseRepository, mqtt: Mqtt):
        self.__firebase = firebase
        self.__mqtt = mqtt

    def execute(self, devices: List[Set]):
        for device in devices:
            id = device.id
            state = device.state
            if not state.get('deviceId'):
                raise response_object({'message': 'Missing deviceId'}, 400)
            self.__mqtt.publish(id, json.dumps(state))
            # if topic.split('/')[1] == "OnOff":
            #     #socketio.emit(id,{"branch":"OnOff","id":id,"state":True if payload == "true" else False})
            #     self.__firebase.update_state(
            #         id, 
            #         "OnOff", 
            #         {'on': True if payload == "true" else False}
            #     )
            # if topic.split('/')[1] == "Color":
            #     #socketio.emit(id,{"branch":"Color","id":id,"state":int(payload)})
            #     self.__firebase.update_state(
            #         id, 
            #         "ColorSetting", 
            #         {'color':{"spectrumRGB":int(payload)}}
            #     )
            # ref = db.reference(f'Devices/{id}')
            # Online = ref.get()
            # if not Online:
            #     socketio.emit(id,{"branch":"Online","id":id,"state":False})
            #     socketio.emit(id,{"branch":"OnOff","id":id,"state":False})
        return response_object({}, 201)