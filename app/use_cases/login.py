import bcrypt
import datetime

from repos.response import response_object
from repos.firebase import FirebaseRepository
from request_objects.login import Login
from domain.authentication import TokenDecoded

class LoginUseCase:
    def __init__(self, firebase: FirebaseRepository):
        self.__firebase = firebase

    def execute(self, body: Login):
        verify = {}
        user = body.userid.replace(' ','')
        password = body.password
        id, verify = self.__firebase.get_user_by_email(user)
        if not verify:
            return response_object({
                "status":False, 
                "message":"User not found"
            }, 401)
        if not verify.active:
            return response_object({
                "status":False, 
                "message":"User not active"
            }, 401)
        verify = verify.password
        if bcrypt.checkpw(password.encode('utf8'), verify.encode('utf8')):
            access = TokenDecoded(
                token_type = "access",
                user = id,
                exp = datetime.datetime.now() + datetime.timedelta(hours=24)
            )
            refresh = TokenDecoded(
                token_type = "refresh",
                user = id
            )
            return response_object({
                "status": True,
                "token": access.encode().token,
                "refresh": refresh.encode().token
            }, 201)
        else:
            return response_object({
                "status":False, 
                "message":"Invalid password"
            }, 401)
