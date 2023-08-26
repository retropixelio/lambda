from repos.firebase import FirebaseRepository
from repos.homegraph import HomeGraphRepository
from repos.response import response_object

from domain.device import Device
from domain.event import Connected

class ConnectedUseCase:
    def __init__(self, firebase: FirebaseRepository, homegraph: HomeGraphRepository):
        self.__firebase = firebase
        self.__homegraph = homegraph

    def execute(self, payload: Connected):
        device = self.__firebase.get_device(payload.client_id)
        if payload.event_type == "disconnected":
            device.online = False
        if payload.event_type == "connected":
            device.online = True
        self.__firebase.set_state(device)
        for user in device.users:
            self.__homegraph.report_state(user, device)
        return response_object({}, 200)
    
class StateUseCase:
    def __init__(self, firebase: FirebaseRepository, homegraph: HomeGraphRepository):
        self.__firebase = firebase
        self.__homegraph = homegraph
    
    def execute(self, state: dict):
        device = self.__firebase.get_device(state["deviceId"])
        if device:
            device = device.to_dict()
            if state.get('color'):
                color = state['color']['red']*256*256 + state['color']['green']*256 + state['color']['blue']
                if state['color']['type'] == 0:
                    device['color']['p'] = color
                elif state['color']['type'] == 1:
                    device['color']['s'] = color
                elif state['color']['type'] == 2:
                    device['color']['t'] = color
            else:
                device.update(state)
            device = Device.from_dict(device)
            self.__firebase.set_state(device)
            for user in device.users:
                self.__homegraph.report_state(user, device)

