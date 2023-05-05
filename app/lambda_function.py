from firebase_admin import credentials
import firebase_admin
import json

from conf import settings

from repos.response import response_object

from domain.event import Request, Connected

from views.ping import Ping
from views.login import LoginView
from views.token import TokenView
from views.refresh import RefreshView
from views.devices import DevicesView
from views.set import SetView
from views.query import QueryView
from views.connected import ConnectedView
from views.auth import AuthView
from views.smarthome import SmarthomeView

firebase_admin.initialize_app(
    credentials.Certificate(settings.BASE_DIR / "service-account.json"),
    {
        'databaseURL': 'https://retropixel-8f415-default-rtdb.firebaseio.com/'
    }
)

def lambda_handler(event, _):
    print(json.loads(event))
    if event.get('eventType'):
        request = Connected.from_dict(event)
        response = ConnectedView()
        return response.get(request)
    else:
        request = Request.from_dict(event)
        urls = {
            '/default/RetroPixelApi/ping': Ping(request),
            '/default/RetroPixelApi/login': LoginView(request),
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
    
