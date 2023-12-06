from repos.firebase import FirebaseRepository
from repos.homegraph import HomeGraphRepository
from repos.response import response_object

from domain.device import Device, DeviceState, Color
from domain.event import Connected

class ConnectedUseCase:
    def __init__(self, firebase: FirebaseRepository, homegraph: HomeGraphRepository):
        self.__firebase = firebase
        self.__homegraph = homegraph

    def execute(self, payload: Connected):
        payload.client_id = payload.client_id[:20]
        device = self.__firebase.get_device(payload.client_id)
        if not device:
            device = Device()
            device.device_id = payload.client_id
            device.color = Color()
            device.brightness = 255 # ESP32 bug (delete this line)
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
    
    def execute(self, state: DeviceState):
        state.device_id = state.device_id[:20]
        device = self.__firebase.get_device(state.device_id)
        if state.device_id is not None: device.device_id=state.device_id
        if state.online is not None: device.online=state.online
        if state.ip is not None: device.ip=state.ip
        if state.onoff is not None: device.onoff=state.onoff
        if state.ambilight is not None: device.ambilight=state.ambilight
        if state.chrome is not None: device.chrome=state.chrome
        if state.color and state.color.p is not None: device.color.p=state.color.p
        if state.color and state.color.s is not None: device.color.s=state.color.s
        if state.color and state.color.t is not None: device.color.t=state.color.t
        if state.color and state.color.type == 0: device.color.p = state.color.red*256*256 + state.color.green*256 + state.color.blue
        if state.color and state.color.type == 1: device.color.s = state.color.red*256*256 + state.color.green*256 + state.color.blue
        if state.color and state.color.type == 2: device.color.t = state.color.red*256*256 + state.color.green*256 + state.color.blue
        if state.brightness is not None and state.ip is None: 
            device.brightness=state.brightness # ESP32 Bug (delete 'and state.ip is None')
        if state.speed is not None: device.speed=state.speed
        self.__firebase.set_state(device)
        for user in device.users:
            self.__homegraph.report_state(user, device)

