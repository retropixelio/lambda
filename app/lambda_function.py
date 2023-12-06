import json

from repos.response import response_object

from domain.event import Request, Connected
from domain.device import DeviceState

from views.ping import PingView
from views.login import LoginView
from views.signup import SignupView
from views.token import TokenView
from views.refresh import RefreshView
from views.devices import DevicesView
from views.set import SetView
from views.query import QueryView
from views.connected import ConnectedView
from views.state import StateView
from views.auth import AuthView
from views.smarthome import SmarthomeView

def lambda_handler(event: dict, _):
    print(json.dumps(event))
    if event.get('eventType'):
        request = Connected.from_dict(event)
        response = ConnectedView()
        return response.get(request)
    if event.get('deviceId'):
        request = DeviceState.from_dict(event)
        response = StateView()
        return response.get(request)
    elif event.get('path'):
        request = Request.from_dict(event)
        urls = {
            '/default/RetroPixelApi/ping': PingView(request),
            '/default/RetroPixelApi/login': LoginView(request),
            '/default/RetroPixelApi/signup': SignupView(request),
            '/default/RetroPixelApi/refresh': RefreshView(request),
            '/default/RetroPixelApi/devices': DevicesView(request),
            '/default/RetroPixelApi/set': SetView(request),
            '/default/RetroPixelApi/query': QueryView(request),
            '/default/RetroPixelApi/auth': AuthView(request),
            '/default/RetroPixelApi/token': TokenView(request),
            '/default/RetroPixelApi/smarthome': SmarthomeView(request),
        }
        request = urls.get(request.path)
        response = request.execute()
        print(response)
        return response if response else response_object({}, status=404)
    return response_object({}, status=404)