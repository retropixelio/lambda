import datetime

from repos.response import response_object
from request_objects.refresh import Refresh
from domain.authentication import Token, TokenDecoded

class RefreshUseCase:
    def execute(self, body: Refresh):   
        refresh_token = Token(token = body.token)
        refresh = refresh_token.decode()
        if refresh.token_type != "refresh":
            return response_object({}, 400)
        user = refresh.user
        access_token = TokenDecoded(
            token_type = 'access',
            user = user,
            exp = datetime.datetime.now() + datetime.timedelta(hours=24)
        )
        token = access_token.encode()
        return response_object({
            "status": True,
            "token": token.token,
            "refresh": body.token
        }, 201)