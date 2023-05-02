import dataclasses

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class Query(FromDictMixin):
    device: str = None