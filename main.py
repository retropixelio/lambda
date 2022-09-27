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
