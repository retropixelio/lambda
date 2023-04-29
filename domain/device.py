import dataclasses
from typing import List

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class SetOnOff(FromDictMixin):
    on: bool = False

@dataclasses.dataclass
class SetOnline(FromDictMixin):
    online: bool = False

@dataclasses.dataclass
class Color(FromDictMixin):
    name: str = None
    spectrumRGB: int = 0

@dataclasses.dataclass
class SetColor(FromDictMixin):
    color: Color = False

@dataclasses.dataclass
class Device(FromDictMixin):
    OnOff: SetOnOff = None
    ColorSetting: SetColor = None
    Online: SetOnline = None