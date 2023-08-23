import json
from typing import List

from repos.firebase import FirebaseRepository
from repos.mqtt import Mqtt
from repos.response import response_object
from request_objects.set import Set

class SetUseCase:
    def __init__(self, mqtt: Mqtt):
        self.__mqtt = mqtt

    def execute(self, devices: List[Set]):
        for device in devices:
            id = device.id
            state = device.state
            state['deviceId'] = id
            self.__mqtt.publish(id, json.dumps(state))
        return response_object({}, 201)