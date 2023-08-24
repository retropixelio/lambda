# import requests

# refresh = 'Atzr|IwEBILsa6gc9eO5eZpoZOj1zVYHgrqXH5F97exWPp5GpV0INMOkLrGggAzTLlox6yWe7Sas-woU3CVIIAO2_mHdNnk0fjyBlixC4I2LpT1Ry5IdU4V1_msJtBkNnEFmeDyw4pGiGEM6NxhCxHwoJY39qB7TT6b5STGc9s1RFtiSo62FbqT2g6BQCyjcAVgRe1CW0669InaUqdVhjmlpQ0otprehega2KJ_sEr8YcGfOQdbv_ihkBjcdab5L2LxQLtojL_E4YU6PkwtvGN4Hp0FJCTLmm'

# response = requests.post(
#     'https://api.amazon.com/auth/o2/token',
#     params={
#         'grant_type': 'refresh_token',
#         'refresh_token': refresh,
#         'client_id': 'amzn1.application-oa2-client.1c0f59a39f3946f5ad6ab115b76da116',
#         'client_secret': 'cb7be17ab3d6077675843a24593c1b384efb43aaee55dbd6c3c9226dcee0b83b'
#     }
# )

# token = response.json()['access_token']

# response = requests.post(
#     'https://api.amazonalexa.com/v3/events',
#     headers={
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {token}'
#     },
#     json={
#         "event": {
#             "header": {
#                 "namespace": "Alexa.Discovery",
#                 "name": "AddOrUpdateReport",
#                 "payloadVersion": "3",
#                 "messageId": "Unique identifier, preferably a version 4 UUID"
#             },
#             "payload": {
#                 "endpoints": [
#                 {
#                     "description": "Tiras Led Inteligentes",
#                     "displayCategories": [
#                         "LIGHT"
#                     ],
#                     "endpointId": "LIGHTlf8yRystroNXcuyXDX5pDw",
#                     "friendlyName": "Luz PC",
#                     "manufacturerName": "Retro Pixel",
#                     "additionalAttributes": {
#                         "manufacturer": "Retro Pixel",
#                         "model": "Pixel Strip",
#                         "serialNumber": "U11112233456",
#                         "firmwareVersion": "1.24.2546",
#                         "softwareVersion": "1.036",
#                         "customIdentifier": "Sample custom ID"
#                     },
#                     "cookie": {},
#                     "connections": [

#                     ],
#                     "capabilities": [
#                         {
#                             "type": "AlexaInterface",
#                             "interface": "Alexa",
#                             "version": "3"
#                         },
#                         {
#                             "type": "AlexaInterface",
#                             "interface": "Alexa.EndpointHealth",
#                             "version": "3",
#                             "properties": {
#                                 "supported": [
#                                     {
#                                         "name": "connectivity"
#                                     }
#                                 ],
#                                 "proactivelyReported": True,
#                                 "retrievable": True
#                             }
#                         },
#                         {
#                             "type": "AlexaInterface",
#                             "interface": "Alexa.ColorController",
#                             "version": "3",
#                             "properties": {
#                                 "supported": [
#                                     {
#                                         "name": "color"
#                                     }
#                                 ],
#                                 "proactivelyReported": True,
#                                 "retrievable": True
#                             }
#                         },
#                         {
#                             "type": "AlexaInterface",
#                             "interface": "Alexa.PowerController",
#                             "version": "3",
#                             "properties": {
#                                 "supported": [
#                                     {
#                                         "name": "powerState"
#                                     }
#                                 ],
#                                 "proactivelyReported": True,
#                                 "retrievable": True
#                             }
#                         }
#                     ]
#                 }
#             ],
#             "scope": {
#                 "type": "BearerToken",
#                 "token": token
#             }
#             }
#         }
#     }
# )

# print(response.status_code)



