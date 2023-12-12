from urllib.parse import parse_qs
import base64
import bcrypt
from jinja2 import Environment, FileSystemLoader
import os

from conf import settings
from repos.firebase import FirebaseRepository
from repos.response import response_object, redirect
from domain.authentication import TokenDecoded

class AuthUseCase:
    def execute(self):
        environment = Environment(
            loader=FileSystemLoader(
                os.path.join(settings.BASE_DIR, "templates"), 
                encoding="utf-8"
            )
        )
        template = environment.get_template('login.html')
        template = template.render(invalid='hidden')
        return response_object(template, 200, 'text/html')

class PostAuthUseCase:
    def __init__(self, firebase: FirebaseRepository):
        self.__firebase = firebase

    def execute(self, body: str, args: dict):
        out = base64.b64decode(body).decode('utf-8')
        form = parse_qs(out)
        environment = Environment(
            loader=FileSystemLoader(
                os.path.join(settings.BASE_DIR, "templates"), 
                encoding="utf-8"
            )
        )
        template = environment.get_template('login.html')
        access_key = form.get('access_key')[0]
        access = self.__firebase.get_credential(access_key)
        url = args.get('redirect_uri')
        state = args.get('state')
        if access:
            user = self.__firebase.search_user(access.user_id)
            code = TokenDecoded(
                user_id = user.user_id,
                token_type = 'access',
            )
            self.__firebase.delete_credential(access_key)
            return redirect(f'{url}?code={code.encode().token}&state={state}')
        else:
            template = template.render(state=state,url=url)
            return response_object(template, 200, 'text/html')