import jwt
import datetime

from conf import settings
from repos.response import response_object

def refresh_post(query):    
    refresh = query['token']
    token = jwt.decode(refresh, settings.SECRET, algorithms=["HS256"])
    if token["token_type"] != "refresh":
        return response_object({}, 400)
    user = token["user"]
    code = jwt.encode({"token_type": "access","user": user,"exp":datetime.datetime.now() + datetime.timedelta(hours=24)}, settings.SECRET, algorithm="HS256")
    return response_object({"status":True,"token":code,"refresh":refresh}, 201)