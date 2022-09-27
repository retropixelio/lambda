# from multiprocessing import context
# from flask import Flask, request, jsonify, render_template, redirect
# # from flask_mqtt import Mqtt
# from flask_cors import CORS
# from flask_socketio import SocketIO
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# import bcrypt
# import jwt
# import urllib.parse
# import datetime
# import os
# import threading
# from secrets import token_hex
# import time

# from conf import settings
# from repos.sync import sync
# from repos.query import query
# from repos.excecute import excecute
# from repos.mqtt import Mqtt

# app = Flask(__name__)

# # app.config['MQTT_CLIENT_ID'] = 'localhost'
# # app.config['MQTT_BROKER_URL'] = 'retropixel.cyou'
# # app.config['MQTT_BROKER_PORT'] = 1883
# # app.config['MQTT_USERNAME'] = 'admin'
# # app.config['MQTT_PASSWORD'] = 'public'
# # app.config['MQTT_KEEPALIVE'] = 30
# # app.config['MQTT_TLS_ENABLED'] = False

# SECRET = 'R1BhE53$yt76$RR1hB5YJM'

# CORS(app)
# mqtt = Mqtt()
# socketio = SocketIO(app, cors_allowed_origins='*')

# @app.route('/register', methods=['POST'])
# def register():
#     name = request.get_json()["name"]
#     last = request.get_json()["last"]
#     email = request.get_json()["email"]
#     password = bcrypt.hashpw(request.get_json()["password"].encode('utf8'),bcrypt.gensalt()).decode('utf8')
#     data = {"devices":[],"name":name,"last":last,"email":email,"password":password,"active":False}
#     ref = db.reference('Users')
#     id = str(int(datetime.datetime.timestamp(datetime.datetime.now())))+token_hex(8)
#     ref.child(id).set(data)
#     token = jwt.encode({"email": email,"exp":datetime.datetime.now() + datetime.timedelta(minutes=15)}, SECRET, algorithm="HS256")
#     return ' ',201

# @app.route('/activate')
# def active():
#     try:
#         token = request.args.get('token')
#     except:
#         return ' ',404
#     ref = db.reference(f'Users')
#     snapshot = ref.order_by_child('email').equal_to(token["email"]).get()
#     for key, val in snapshot.items():
#         id = key
#     ref = db.reference(f"Users/{id}")
#     ref.set({'active':True})
#     return redirect("https://retropixel.tk", code=302)

# @app.route('/')
# def index():
#     return redirect('https://retropixel.tk')

# @app.route('/auth',methods=['GET', 'POST'])
# def auth():
#     if request.method == 'GET':
#         return render_template('login.html',invalid='hidden')
#     elif request.method == 'POST':
#         user = request.form.get('userid')
#         password = request.form.get('password')
#         url = request.args.get('redirect_uri')
#         state = request.args.get('state')
#         ref = db.reference(f'Users')
#         snapshot = ref.order_by_child('email').equal_to(user).get()
#         verify = None
#         for key, val in snapshot.items():
#             verify = val
#             id = key
#         if not verify: return render_template('login.html',state=state,url=url)
#         verify = verify["password"]
#         if bcrypt.checkpw(password.encode('utf8'), verify.encode('utf8')):
#             code = jwt.encode({"user": id}, SECRET, algorithm="HS256")
#             return redirect(f'{url}?code={code}&state={state}')
#         else:
#             return render_template('login.html',state=state,url=url)
#     else: return 'Bad request',400

# @app.route('/token',methods=['POST'])
# def token():
#     data = urllib.parse.parse_qs(request.get_data().decode('utf-8'))
#     grant_type = data['grant_type'][0]
#     if grant_type == 'authorization_code':
#         code = data['code'][0]
#         try:
#             user = jwt.decode(code, SECRET, algorithms=["HS256"])
#         except:
#             return 'Invalid token',401
#         access = jwt.encode({"type":"access","user": user["user"],"exp":datetime.datetime.now() + datetime.timedelta(hours=24)}, SECRET, algorithm="HS256")
#         refresh = jwt.encode({"type":"refresh","user": user["user"]}, SECRET, algorithm="HS256")
#         payload = {
#             "token_type": "Bearer",
#             "access_token": access,
#             "refresh_token": refresh,
#             "expires_in": 24*3600
#         }
#         return jsonify(payload)
#     elif grant_type == 'refresh_token':
#         code = data['refresh_token'][0]
#         try:
#             user = jwt.decode(code, SECRET, algorithms=["HS256"])
#         except:
#             return 'Invalid token',401
#         access = jwt.encode({"type":"access","user": user["user"],"exp":datetime.datetime.now() + datetime.timedelta(hours=24)}, SECRET, algorithm="HS256")
#         payload = {
#             "token_type": "Bearer",
#             "access_token": access,
#             "expires_in": 24*3600
#         }
#         return jsonify(payload)
#     else: return 'Bad request',400

# @app.route('/connected',methods=['POST'])
# def connected():
#     payload = request.get_json()
#     if payload["eventType"] == "disconnected" and payload['clientId'].startswith("LIGHT"):
#         ref = db.reference(f"Fisical/{payload['clientId']}")
#         device_list = ref.get()
#         for device in device_list:
#             ref = db.reference(f"Devices/{device}/Online")
#             ref.set({'online':False})
#             socketio.emit(device,{"branch":"Online","id":device,"state":False})
#     if payload["eventType"] == "connected" and payload['clientId'].startswith("LIGHT"):
#         ref = db.reference(f"Fisical/{payload['clientId']}")
#         device_list = ref.get()
#         for device in device_list:
#             ref = db.reference(f"Devices/{device}/Online")
#             ref.set({'online':True})
#             socketio.emit(device,{"branch":"Online","id":device,"state":True})
#     if payload["eventType"] == "publish":
#         ref = db.reference(f"Fisical/{payload['device']}")
#         device_list = ref.get()
#         for device in device_list:
#             ref = db.reference(f"Devices/{device}")
#             data = ref.get()
#             OnOff = "true" if data["OnOff"]["on"] else "false"
#             Color = data["ColorSetting"]["color"]["spectrumRGB"] if data["ColorSetting"]["color"].get("spectrumRGB") else 16777215
#             mqtt.publish(f"{device}/OnOff",OnOff)
#             mqtt.publish(f"{device}/Color",Color)
#         # if payload["topic"].split('/')[1] == "OnOff":
#         #     id = payload['topic'].split('/')[0]
#         #     socketio.emit(id,{"branch":"OnOff","id":id,"state":True if payload["payload"] == "true" else False})
#         # if payload["topic"].split('/')[1] == "Color":
#         #     id = payload['topic'].split('/')[0]
#         #     socketio.emit(id,{"branch":"Color","id":id,"state":int(payload["payload"])})
#     return ' ',200

request = {
    "version": "1.0",
    "resource": "/RetroPixelApi",
    "path": "/default/RetroPixelApi/auth",
    "httpMethod": "GET",
    "headers": {
        "Content-Length": "76",
        "Content-Type": "application/json",
        "Host": "a60h4yl2h0.execute-api.us-east-1.amazonaws.com",
        "Postman-Token": "2c77d674-f433-4491-949b-ad94e5502dc9",
        "User-Agent": "PostmanRuntime/7.28.3",
        "X-Amzn-Trace-Id": "Root=1-63332e86-77cfca721cc249ff6e4ce16d",
        "X-Forwarded-For": "201.221.176.16",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br"
    },
    "multiValueHeaders": {
        "Content-Length": [
            "76"
        ],
        "Content-Type": [
            "application/json"
        ],
        "Host": [
            "a60h4yl2h0.execute-api.us-east-1.amazonaws.com"
        ],
        "Postman-Token": [
            "2c77d674-f433-4491-949b-ad94e5502dc9"
        ],
        "User-Agent": [
            "PostmanRuntime/7.28.3"
        ],
        "X-Amzn-Trace-Id": [
            "Root=1-63332e86-77cfca721cc249ff6e4ce16d"
        ],
        "X-Forwarded-For": [
            "201.221.176.16"
        ],
        "X-Forwarded-Port": [
            "443"
        ],
        "X-Forwarded-Proto": [
            "https"
        ],
        "accept": [
            "*/*"
        ],
        "accept-encoding": [
            "gzip, deflate, br"
        ]
    },
    "queryStringParameters": None,
    "multiValueQueryStringParameters": None,
    "requestContext": {
        "accountId": "247499575159",
        "apiId": "a60h4yl2h0",
        "domainName": "a60h4yl2h0.execute-api.us-east-1.amazonaws.com",
        "domainPrefix": "a60h4yl2h0",
        "extendedRequestId": "ZIQ1Gg_joAMEVpQ=",
        "httpMethod": "POST",
        "identity": {
            "accessKey": None,
            "accountId": None,
            "caller": None,
            "cognitoAmr": None,
            "cognitoAuthenticationProvider": None,
            "cognitoAuthenticationType": None,
            "cognitoIdentityId": None,
            "cognitoIdentityPoolId": None,
            "principalOrgId": None,
            "sourceIp": "201.221.176.16",
            "user": None,
            "userAgent": "PostmanRuntime/7.28.3",
            "userArn": None
        },
        "path": "/default/RetroPixelApi",
        "protocol": "HTTP/1.1",
        "requestId": "ZIQ1Gg_joAMEVpQ=",
        "requestTime": "27/Sep/2022:17:10:30 +0000",
        "requestTimeEpoch": 1664298630836,
        "resourceId": "ANY /RetroPixelApi",
        "resourcePath": "/RetroPixelApi",
        "stage": "default"
    },
    "pathParameters": None,
    "stageVariables": None,
    "body": "{\r\n    \"userid\":\"andres64372@hotmail.com\",\r\n    \"password\":\"medellin1998\"\r\n}",
    "isBase64Encoded": None
}

from lambda_function import lambda_handler

response = lambda_handler(request, None)
print(response)
