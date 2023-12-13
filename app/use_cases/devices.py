from request_objects.device import Device as DeviceRequest
from domain.user import UserDevice

from repos.firebase import FirebaseRepository
from repos.homegraph import HomeGraphRepository
from repos.response import response_object

class DevicesUseCase:
    def __init__(self, firebase: FirebaseRepository):
        self.__firebase = firebase

    def execute(self):
        user = self.__firebase.get_user_info()
        if not user or not user.devices: 
            return response_object({
                'list': [],
                'states': {}
            }, 200)
        device_list = []
        device_states = {}
        for device in user.devices:
            data = self.__firebase.get_device(device.id)
            data.name = device.nickname
            data.room = device.room
            device_list.append(data.id)
            device_states.update({
                data.id: data.to_dict(),
            })
        return response_object({
            'list': device_list,
            'states': device_states
        }, 200)
    
class AddDeviceUseCase:
    def __init__(self, firebase: FirebaseRepository, homegraph: HomeGraphRepository):
        self.__firebase = firebase
        self.__homegraph = homegraph
    
    def execute(self, request: DeviceRequest):
        user = self.__firebase.get_user_info()
        if request.id not in [user_device.id for user_device in user.devices]:
            user.devices.append(UserDevice(
                id = request.id,
                nickname = request.nickname,
                room = request.room
            ))
            device = self.__firebase.get_device(request.id)
            device.users.append(user.user_id)
            device.users = list(set(device.users))
            self.__firebase.create_user(user)
            self.__homegraph.request_sync(user.user_id)
            return response_object({'message': 'Device paired'}, 201)
        else:
            return response_object({'message': 'Device already paired'}, 400)
    
class DeleteDeviceUseCase:
    def __init__(self, firebase: FirebaseRepository, homegraph: HomeGraphRepository):
        self.__firebase = firebase
        self.__homegraph = homegraph
    
    def execute(self, request: DeviceRequest):
        user = self.__firebase.get_user_info()
        device = self.__firebase.get_device(request.id)
        user.devices = [
            user_device 
            for user_device in user.devices 
            if user_device.id != request.id
        ]
        device.users = [
            item
            for item in device.users
            if item != user.user_id
        ]
        self.__firebase.create_user(user) 
        self.__homegraph.request_sync(user.user_id)
        return response_object({}, 201)