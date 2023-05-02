from firebase_admin import db

from domain.user import User, UserDevice
from domain.device import Device

class FirebaseRepository:
    def __init__(self, user):
        self.__user = user

    def get_user(self):
        return self.__user
    
    def get_user_by_email(self, email):
        ref = db.reference(f'Users')
        snapshot = ref.order_by_child('email').equal_to(email).get()
        for key, val in snapshot.items():
            verify = val
            id = key
        return id, User.from_dict(verify)
    
    def get_user_devices(self):
        ref = db.reference(f'Users/{self.__user}/devices')
        devices = ref.get()
        return [UserDevice.from_dict(device) for device in devices]
    
    def get_device(self, device):
        ref = db.reference(f'Devices/{device}')
        device = ref.get()
        return Device.from_dict(device)
    
    def get_fisical(self, device):
        ref = db.reference(f'Fisical/{device}')
        device = ref.get()
        return device

    def set_state(self, device, state, value):
        ref = db.reference(f'Devices/{device}')
        ref.set({state: value})

    def update_state(self, device, state, value):
        ref = db.reference(f'Devices/{device}/{state}')
        ref.set(value)