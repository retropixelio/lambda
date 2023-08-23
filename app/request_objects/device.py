import dataclasses

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class Device(FromDictMixin):
    id: str = None
    nickname: str = None
    room: str = None