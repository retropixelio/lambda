import jwt
from urllib.parse import parse_qs
import datetime

from conf import settings
from repos.response import response_object

def token_post(data):
    grant_type = data['grant_type'][0]
    if grant_type == 'authorization_code':
        code = data['code'][0]
        try:
            user = jwt.decode(code, settings.SECRET, algorithms=["HS256"])
        except:
            return response_object({'message','Invalid token'}, 401)
        access = jwt.encode({"token_type":"access","user": user["user"],"exp":datetime.datetime.now() + datetime.timedelta(hours=24)}, settings.SECRET, algorithm="HS256")
        refresh = jwt.encode({"token_type":"refresh","user": user["user"]}, settings.SECRET, algorithm="HS256")
        payload = {
            "token_type": "Bearer",
            "access_token": access,
            "refresh_token": refresh,
            "expires_in": 24*3600
        }
        return response_object(payload, 200)
    elif grant_type == 'refresh_token':
        code = data['refresh_token'][0]
        try:
            user = jwt.decode(code, settings.SECRET, algorithms=["HS256"])
        except:
            return response_object({'message','Invalid token'}, 401)
        access = jwt.encode({"token_type":"access","user": user["user"],"exp":datetime.datetime.now() + datetime.timedelta(hours=24)}, settings.SECRET, algorithm="HS256")
        payload = {
            "token_type": "Bearer",
            "access_token": access,
            "expires_in": 24*3600
        }
        return response_object(payload, 200)
    else: 
        return response_object({'message','Bad request'}, 400)