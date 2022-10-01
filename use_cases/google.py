import jwt

from repos.sync import sync
from repos.query import query
from repos.excecute import excecute
from repos.response import response_object
from conf import settings

def smarthome(headers, body):
    token = headers.get('authorization')[7:]
    try:
        user = jwt.decode(token, settings.SECRET, algorithms=["HS256"])
        if user["token_type"] != "access":
            return response_object({}, 401)
    except:
        return response_object({}, 401)
    user = user["user"]
    inputs = body['inputs']
    id = body['requestId']
    for i in inputs:
        if i["intent"] == "action.devices.SYNC":
            data = sync(user,id)
            return response_object(data, 200)
        if i["intent"] == "action.devices.QUERY":
            data = query(i,id)
            return response_object(data, 200)
        if i["intent"] == "action.devices.EXECUTE":
            data = excecute(i,id)
            return response_object(data, 200)