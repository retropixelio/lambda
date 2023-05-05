from firebase_admin import db

from repos.mqtt import Mqtt
from repos.firebase import FirebaseRepository
from repos.response import response_object

from domain.event import Connected

class ConnectedUseCase:
    def __init__(self, firebase: FirebaseRepository, mqtt: Mqtt):
        self.__firebase = firebase
        self.__mqtt = mqtt

    def execute(self, payload: Connected):
        if payload.eventType == "disconnected" and payload.clientId.startswith("LIGHT"):
            device_list = self.__firebase.get_fisical(payload.clientId)
            for device in device_list:
                self.__firebase.update_state(device, 'Online', {'online': False})
                # socketio.emit(device,{"branch":"Online","id":device,"state":False})
        if payload.eventType == "connected" and payload.clientId.startswith("LIGHT"):
            device_list = self.__firebase.get_fisical(payload.clientId)
            for device in device_list:
                self.__firebase.update_state(device, 'Online', {'online': True})
                data = self.__firebase.get_device(device)
                OnOff = "true" if data.OnOff.on else "false"
                Color = data.ColorSetting.color.spectrumRGB if data.ColorSetting.color.spectrumRGB else 16777215
                self.__mqtt.publish(f"{device}/OnOff",OnOff)
                self.__mqtt.publish(f"{device}/Color",str(Color))
        return response_object({}, 200)