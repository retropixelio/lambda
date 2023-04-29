from repos.firebase import FirebaseRepository
from repos.response import response_object

class DevicesUseCase:
    def __init__(self, firebase: FirebaseRepository):
        self.__firebase = firebase

    def execute(self):
        devices = self.__firebase.get_user_devices()
        if not devices: 
            return response_object({'list':[],'states':{}},200)
        device_list = []
        device_states = {}
        for device in devices:
            device_list.append(device.id)
            data = self.__firebase.get_device(device.id)
            if not data:
                self.__firebase.set_state("ColorSetting", {"color": {"spectrumRGB": 16777215}})
                self.__firebase.set_state("OnOff", {"on": False})
                self.__firebase.set_state("Online", {"online": False})
                device_states.update({device.id:{
                    "OnOff": False,
                    "Online": False,
                    "Color": 16777215
                }})
            else:
                OnOff = data.OnOff.on
                Online = data.Online.online
                Color = data.ColorSetting.color.spectrumRGB if data.ColorSetting.color.spectrumRGB else 16777215
                device_states.update({
                    device.id:{
                        "name": device.nickname,
                        "OnOff":OnOff,
                        "Online":Online,
                        "Color":int(Color)
                    }
                })
        return response_object({'list':device_list,'states':device_states},200)