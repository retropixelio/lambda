smarthome = {
    "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
    "inputs": [{
      "intent": "action.devices.QUERY",
      "payload": {
        "devices": [{
          "id": "123",
          "customData": {
            "fooValue": 74,
            "barValue": True,
            "bazValue": "foo"
          }
        }, {
          "id": "456",
          "customData": {
            "fooValue": 12,
            "barValue": False,
            "bazValue": "bar"
          }
        }]
      }
    }]
}

from domain.smarthome import Smarthome

response = Smarthome.from_dict(smarthome)
print(response)