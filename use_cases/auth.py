from firebase_admin import db
import jwt
import bcrypt
from jinja2 import Environment, FileSystemLoader
import os

from conf import settings
from repos.response import response_object, redirect

def auth_get():
    environment = Environment(loader=FileSystemLoader(os.path.join(settings.BASE_DIR,"templates/")))
    template = environment.get_template('login.html')
    template = template.render(invalid='hidden')
    return response_object(template, 200, 'text/html')

def auth_post(form, args):
    environment = Environment(loader=FileSystemLoader(os.path.join(settings.BASE_DIR,"templates/")))
    template = environment.get_template('login.html')
    user = form.get('userid')
    password = form.get('password')
    url = args.get('redirect_uri')
    state = args.get('state')
    ref = db.reference(f'Users')
    snapshot = ref.order_by_child('email').equal_to(user).get()
    verify = None
    for key, val in snapshot.items():
        verify = val
        id = key
    if not verify: 
        template = template.render(state=state,url=url)
        return response_object(template, 200, 'text/html')
    verify = verify["password"]
    if bcrypt.checkpw(password.encode('utf8'), verify.encode('utf8')):
        code = jwt.encode({"user": id}, settings.SECRET, algorithm="HS256")
        return redirect(f'{url}?code={code}&state={state}')
    else:
        template = template.render(state=state,url=url)
        return response_object(template, 200, 'text/html')