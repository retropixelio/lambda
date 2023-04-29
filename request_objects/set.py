import dataclasses

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class Set(FromDictMixin):
    topic: str = None
    payload: str = None