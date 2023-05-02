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

    def execute(self, body, args):
        out = base64.b64decode(body).decode('utf-8')
        form = parse_qs(out)
        environment = Environment(
            loader=FileSystemLoader(
                os.path.join(settings.BASE_DIR, "templates"), 
                encoding="utf-8"
            )
        )
        template = environment.get_template('login.html')
        user = form.get('userid')[0]
        password = form.get('password')[0]
        url = args.get('redirect_uri')
        state = args.get('state')
        id, verify = self.__firebase.get_user_by_email(user)
        if not verify: 
            template = template.render(state=state,url=url)
            return response_object(template, 200, 'text/html')
        verify = verify.password
        if bcrypt.checkpw(password.encode('utf-8'), verify.encode('utf-8')):
            code = TokenDecoded(
                user = id,
                token_type = 'access',
            )
            return redirect(f'{url}?code={code.encode().token}&state={state}')
        else:
            template = template.render(state=state,url=url)
            return response_object(template, 200, 'text/html')