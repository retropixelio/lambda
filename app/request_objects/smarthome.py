import dataclasses
from typing import List, Dict

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class Execution(FromDictMixin):
    command: str = None
    params: Dict[str, str] = dataclasses.field(default_factory=dict)

@dataclasses.dataclass
class Device(FromDictMixin):
    id: str = None

@dataclasses.dataclass
class Command(FromDictMixin):
    devices: List[Device] = dataclasses.field(default_factory=list)
    execution: List[Execution] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class Payload(FromDictMixin):
    devices: List[Device] = dataclasses.field(default_factory=list)
    commands: List[Command] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class Input(FromDictMixin):
    intent: str = None
    payload: Payload = None

@dataclasses.dataclass
class Smarthome(FromDictMixin):
    request_id: str = None
    inputs: List[Input] = dataclasses.field(default_factory=list)