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
        user = self.__firebase.get_user_by_email(user)
        if not user:
            return response_object({
                "status":False, 
                "message":"User not found"
            }, 401)
        if not user.active:
            return response_object({
                "status":False, 
                "message":"User not active"
            }, 401)
        verify = user.password
        if bcrypt.checkpw(password.encode('utf8'), verify.encode('utf8')):
            access = TokenDecoded(
                token_type = "access",
                user = user.user_id,
                exp = datetime.datetime.now() + datetime.timedelta(hours=24)
            )
            refresh = TokenDecoded(
                token_type = "refresh",
                user = user.user_id
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
