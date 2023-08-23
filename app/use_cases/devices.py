from request_objects.device import Device as DeviceRequest
from domain.user import UserDevice
from domain.device import Device, Color

from repos.firebase import FirebaseRepository
from repos.response import response_object

class DevicesUseCase:
    def __init__(self, firebase: FirebaseRepository):
        self.__firebase = firebase

    def execute(self):
        user = self.__firebase.get_user_info()
        if not user.devices: 
            return response_object({
                'list': [],
                'states': {}
            }, 200)
        device_list = []
        device_states = {}
        for device in user.devices:
            device_list.append(device.id)
            data = self.__firebase.get_device(device.id)
            if not data:
                data = Device(
                    device_id = device.id,
                    name = device.nickname,
                    online = False,
                    ip = "0.0.0.0",
                    onoff = False,
                    ambilight = False,
                    chrome = 0,
                    color = Color(
                        p = 16777215,
                        s = 16777215,
                        t = 16777215,
                    ),
                    brightness = 100,
                    speed = 1000,
                )
                self.__firebase.set_state(data)
            device_states.update({
                device.id: data.to_dict(),
            })
        return response_object({
            'list': device_list,
            'states': device_states
        }, 200)
    
class AddDeviceUseCase:
    def __init__(self, firebase: FirebaseRepository):
        self.__firebase = firebase
    
    def execute(self, device: DeviceRequest):
        user = self.__firebase.get_user_info()
        user.devices.append(UserDevice(
            id = device.id,
            nickname = device.nickname,
            room = device.room
        ))
        self.__firebase.create_user(user)
        return response_object({}, 201)