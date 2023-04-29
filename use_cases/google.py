from repos.sync import sync
from repos.query import query
from repos.excecute import excecute
from repos.response import response_object

class SmarthomeUseCase:
    def execute(body, user):
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