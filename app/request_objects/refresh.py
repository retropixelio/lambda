import dataclasses

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class Refresh(FromDictMixin):
    token: str = None