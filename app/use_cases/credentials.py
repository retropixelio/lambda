import secrets
from datetime import datetime

from domain.user import AccessKey

from repos.firebase import FirebaseRepository
from repos.response import response_object

class CredentialsUseCase:
    def __init__(self, firebase: FirebaseRepository):
        self.__firebase = firebase

    def execute(self):
        user = self.__firebase.get_user_info()
        if user.third_party_credential: self.__firebase.delete_credential(user.third_party_credential)
        token = secrets.token_hex(4)
        access_key = AccessKey(
            third_party_credential=token,
            user_id=user.user_id,
            expiration=int(datetime.utcnow().timestamp() + 30)
        )
        user.third_party_credential = token
        self.__firebase.create_credential(access_key)
        self.__firebase.create_user(user)

        return response_object({
            'token': token,
        }, 200)
    