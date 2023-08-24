import dataclasses
from typing import List

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class Color(FromDictMixin):
    s: int = 0
    p: int = 0
    t: int = 0

@dataclasses.dataclass
class Device(FromDictMixin):
    device_id: str = None
    users: List[str] = dataclasses.field(default_factory=list)
    online: bool = False
    ip: str = None
    onoff: bool = False
    ambilight: bool = False
    chrome: int = 0
    color: Color = None
    brightness: int = 0
    speed: int = 0
    name: str = None