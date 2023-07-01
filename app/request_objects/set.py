import dataclasses

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class Set(FromDictMixin):
    id: str = None
    state: dict = None