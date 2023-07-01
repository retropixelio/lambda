import dataclasses
from typing import Dict

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class Set(FromDictMixin):
    id: str = None
    state: Dict[str, str] = dataclasses.field(default_factory=dict)