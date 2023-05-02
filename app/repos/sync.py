
def sync(user,id):
    ref = db.reference(f'Users/{user}/devices')
    state = ref.get()
    print(user)
    devices = []
    for i in state:
        devices.append({
            "id": i["id"],
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
                    i["nickname"]
                ]
            },
            "willReportState": True,
            "roomHint": i["room"],
            "attributes": {
                "colorModel": "rgb",
                "commandOnlyColorSetting": True
            },
            "deviceInfo": {
                "manufacturer": "RectroPixel c.o",
                "model": "lstrp-01",
                "hwVersion": "1.0",
                "swVersion": "1.0"
            }
        })
    response = {
        "requestId": id,
        "payload": {
            "agentUserId": user,
            "devices": devices
        }
    }
    return response