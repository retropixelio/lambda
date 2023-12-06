import dataclasses
from typing import Dict, Any

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class Color(FromDictMixin):
    red: int = 0
    green: int = 0
    blue: int = 0
    type: int = 0

@dataclasses.dataclass
class State(FromDictMixin):
    device_id: str = None
    onoff: bool = None
    ambilight: bool = None
    chrome: int = None
    color: Color = None
    leds: int = None
    speed: int = None
    brightness: int = None
    
@dataclasses.dataclass
class Set(FromDictMixin):
    id: str = None
    state: State = None