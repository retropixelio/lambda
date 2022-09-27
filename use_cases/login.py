import bcrypt
import jwt
import datetime
from firebase_admin import db

from conf import settings
from repos.response import response_object

def login_post(body):
    verify = {}
    user = body['userid'].replace(' ','')
    password = body['password']
    ref = db.reference(f'Users')
    snapshot = ref.order_by_child('email').equal_to(user).get()
    for key, val in snapshot.items():
        verify = val
        id = key
    print(verify)
    if not verify:
        return response_object({"status":False, "message":"User not found"},401)
    if not verify["active"]:
        return response_object({"status":False, "message":"User not active"},401)
    verify = verify["password"]
    if bcrypt.checkpw(password.encode('utf8'), verify.encode('utf8')):
        code = jwt.encode({"token_type": "access","user": id,"exp":datetime.datetime.now() + datetime.timedelta(hours=24)}, settings.SECRET, algorithm="HS256")
        refresh = jwt.encode({"token_type": "refresh","user": id}, settings.SECRET, algorithm="HS256")
        return response_object({"status":True,"token":code,"refresh":refresh}, 200)
    else:
        return response_object({"status":False, "message":"Invalid password"}, 401)
