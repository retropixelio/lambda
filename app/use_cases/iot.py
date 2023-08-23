from repos.firebase import FirebaseRepository
from repos.response import response_object

from domain.device import Device
from domain.event import Connected

class ConnectedUseCase:
    def __init__(self, firebase: FirebaseRepository):
        self.__firebase = firebase

    def execute(self, payload: Connected):
        device = self.__firebase.get_device(payload.client_id)
        if payload.event_type == "disconnected":
            device.online = False
        if payload.event_type == "connected":
            device.online = True
        self.__firebase.set_state(device)
        return response_object({}, 200)
    
class StateUseCase:
    def __init__(self, firebase: FirebaseRepository):
        self.__firebase = firebase
    
    def execute(self, state: dict):
        device = self.__firebase.get_device(state["deviceId"])
        if device:
            device = device.to_dict()
            device.update(state)
            self.__firebase.set_state(Device.from_dict(device))

