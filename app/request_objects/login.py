import dataclasses

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class Login(FromDictMixin):
    userid: str = None
    password: str = None