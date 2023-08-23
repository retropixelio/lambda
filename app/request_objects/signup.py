import dataclasses

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class SignUp(FromDictMixin):
    first_name: str = None
    last_name: str = None
    email: str = None
    password: str = None