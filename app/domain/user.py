import dataclasses
from typing import List

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class UserDevice(FromDictMixin):
    id: str = None
    nickname: str = None
    room: str = None

@dataclasses.dataclass
class User(FromDictMixin):
    active: bool = False
    devices: List[UserDevice] = dataclasses.field(default_factory=list)
    email: str = None
    name: str = None
    last: str = None
    password: str = None