import jwt
import json

from repos.sync import sync
from repos.query import query
from repos.excecute import excecute
from repos.response import response_object

SECRET = 'R1BhE53$yt76$RR1hB5YJM'

def smarthome(headers, body):
    token = headers.get('Authorization')[7:]
    try:
        user = jwt.decode(token, SECRET, algorithms=["HS256"])
        if user["type"] != "access":
            return response_object({}, 401)
    except:
        return response_object({}, 401)
    user = user["user"]
    inputs = body['inputs']
    id = body['requestId']
    for i in inputs:
        if i["intent"] == "action.devices.SYNC":
            data = sync(user,i,id)
            return response_object(data, 200)
        if i["intent"] == "action.devices.QUERY":
            data = query(i,id)
            return response_object(data, 200)
        if i["intent"] == "action.devices.EXECUTE":
            data = excecute(i,id)
            return response_object(data, 200)