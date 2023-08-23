import bcrypt

from repos.response import response_object
from repos.firebase import FirebaseRepository
from request_objects.signup import SignUp
from domain.user import User

class SignUpUseCase:
    def __init__(self, firebase: FirebaseRepository):
        self.__firebase = firebase

    def execute(self, body: SignUp):
        verify = self.__firebase.get_user_by_email(body.email)
        if verify:
            return response_object({
                "status":False, 
                "message":"User already exists"
            }, 401)
        password = bcrypt.hashpw(
            body.password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        user = User(
            user_id=body.email,
            first_name=body.first_name,
            last_name=body.last_name,
            password=password,
        )
        error = self.__firebase.create_user(user)
        if not error:
            return response_object({
                "status": True,
            }, 201)
        else:
            return response_object({
                "status":False, 
                "message":error
            }, 401)