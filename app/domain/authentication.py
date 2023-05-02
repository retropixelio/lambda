import dataclasses
import jwt
from datetime import datetime

from conf import settings

@dataclasses.dataclass
class TokenDecoded:
    token_type: str = None
    user: str = None
    exp: datetime = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            token_type = data.get('token_type'),
            user = data.get('user')
        )

    def encode(self):
        if self.exp:
            token = jwt.encode({
                "token_type": self.token_type,
                "user": self.user,
                "exp": self.exp
            }, settings.SECRET, algorithm="HS256")
        else:
            token = jwt.encode({
                "token_type": self.token_type,
                "user": self.user
            }, settings.SECRET, algorithm="HS256")
        return Token(
            token = token
        )

@dataclasses.dataclass
class Token:
    token: str = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            token = data.get('token')
        )

    def decode(self):
        token = TokenDecoded.from_dict(
            jwt.decode(self.token, settings.SECRET, algorithms=["HS256"])
        )
        return token