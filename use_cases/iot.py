from firebase_admin import db

from repos.mqtt import Mqtt
from repos.response import response_object

mqtt = Mqtt()

def connected(payload):
    if payload["eventType"] == "disconnected" and payload['clientId'].startswith("LIGHT"):
        ref = db.reference(f"Fisical/{payload['clientId']}")
        device_list = ref.get()
        for device in device_list:
            ref = db.reference(f"Devices/{device}/Online")
            ref.set({'online':False})
            # socketio.emit(device,{"branch":"Online","id":device,"state":False})
    if payload["eventType"] == "connected" and payload['clientId'].startswith("LIGHT"):
        ref = db.reference(f"Fisical/{payload['clientId']}")
        device_list = ref.get()
        for device in device_list:
            ref = db.reference(f"Devices/{device}/Online")
            ref.set({'online':True})
            # socketio.emit(device,{"branch":"Online","id":device,"state":True})
    if payload["eventType"] == "publish":
        ref = db.reference(f"Fisical/{payload['device']}")
        device_list = ref.get()
        for device in device_list:
            ref = db.reference(f"Devices/{device}")
            data = ref.get()
            OnOff = "true" if data["OnOff"]["on"] else "false"
            Color = data["ColorSetting"]["color"]["spectrumRGB"] if data["ColorSetting"]["color"].get("spectrumRGB") else 16777215
            mqtt.publish(f"{device}/OnOff",OnOff)
            mqtt.publish(f"{device}/Color",str(Color))
        # if payload["topic"].split('/')[1] == "OnOff":
        #     id = payload['topic'].split('/')[0]
        #     socketio.emit(id,{"branch":"OnOff","id":id,"state":True if payload["payload"] == "true" else False})
        # if payload["topic"].split('/')[1] == "Color":
        #     id = payload['topic'].split('/')[0]
        #     socketio.emit(id,{"branch":"Color","id":id,"state":int(payload["payload"])})
    return response_object({}, 200)