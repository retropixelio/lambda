import json
from request_objects.smarthome import Smarthome, Input
from repos.firebase import FirebaseRepository
from repos.mqtt import Mqtt
from repos.response import response_object

class SmarthomeUseCase:
    def __init__(self, firebase: FirebaseRepository, mqtt: Mqtt):
        self.__firebase = firebase
        self.__mqtt = mqtt

    def execute(self, body: Smarthome):
        inputs = body.inputs
        id = body.requestId
        for input in inputs:
            if input.intent == "action.devices.SYNC":
                data = self.__sync(id)
                return response_object(data, 200)
            if input.intent == "action.devices.QUERY":
                data = self.__query(input, id)
                return response_object(data, 200)
            if input.intent == "action.devices.EXECUTE":
                data = self.__excecute(input, id)
                return response_object(data, 200)
            
    def __excecute(self, body: Input, req_id):
        commands = body.payload.commands
        payloads = []
        for command in commands:
            devices = command.devices
            excecution = command.execution
            for device in devices:
                payload = {}
                id = device.id
                payload["ids"] = [id]
                payload["status"] = "SUCCESS"
                for excecute in excecution:
                    payload["states"] = excecute.params
                    payload["states"]["online"] = True
                    if excecute.command == "action.devices.commands.OnOff":
                        self.__mqtt.publish(
                            id,
                            json.dumps({
                                "deviceId": id,
                                "onoff": excecute.params["on"]
                            })
                        )
                    if excecute.command == "action.devices.commands.ColorAbsolute":
                        color = excecute.params['color']['spectrumRGB']
                        rgb = (color // 256 // 256 % 256, color // 256 % 256, color % 256)
                        self.__mqtt.publish(
                            id,
                            json.dumps({
                                "deviceId": id,
                                "color": {
                                    "red": rgb[0],
                                    "green": rgb[1],
                                    "blue": rgb[2]
                                }
                            })
                        )
                device = self.__firebase.get_device(id)
                if not device.Online.online: 
                    payload = {
                        "ids": [id],
                        "status" : "OFFLINE",
                        "on":False
                    }
                payloads.append(payload)
        response = {
            "requestId": req_id,
            "payload": {
                "commands": payloads
            }
        }
        return response
            
    def __query(self, body: Input, req_id):
        payload = {}
        for device in body.payload.devices:
            id = device.id
            data = self.__firebase.get_device(id)
            OnOff = data.OnOff.on
            Online = data.Online.online
            Color = data.ColorSetting.color
            if Online:
                payload[id] = {
                    "on": OnOff,
                    "online": True,
                    "color": Color.to_dict(),
                    "status": "SUCCESS"
                }
            else: 
                payload[id] = {
                    "status": "OFFLINE",
                    "on": False
                }
        response = {
            "requestId": req_id,
            "payload": {
                "devices": payload
            }
        }
        return response
            
    def __sync(self, id):
        return {
            "requestId": id,
            "payload": {
                "agentUserId": self.__firebase.get_user(),
                "devices": [{
                    "id": device.id,
                    "type": "action.devices.types.LIGHT",
                    "traits": [
                        "action.devices.traits.OnOff",
                        "action.devices.traits.ColorSetting"
                    ],
                    "name": {
                        "defaultNames": [
                            "RGB Smart Lights"
                        ],
                        "name": "Smart light",
                        "nicknames": [
                            device.nickname
                        ]
                    },
                    "willReportState": False,
                    "roomHint": device.room,
                    "attributes": {
                        "colorModel": "rgb",
                        "commandOnlyColorSetting": True
                    },
                    "deviceInfo": {
                        "manufacturer": "RectroPixel C.O",
                        "model": "lstrp-01",
                        "hwVersion": "1.0",
                        "swVersion": "1.0"
                    }
                } for device in self.__firebase.get_user_devices()]
            }
        }