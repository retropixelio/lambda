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
        print(devices)
        for device in devices:
            self.__mqtt.publish(
                device.id, 
                json.dumps(
                    {key: value for key,value in device.state.to_dict().items() if value is not None}
                )
            )
        return response_object({}, 201)