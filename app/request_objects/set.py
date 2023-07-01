import dataclasses
from typing import Dict, Any

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class Set(FromDictMixin):
    id: str = None
    state: Dict[str, Any] = dataclasses.field(default_factory=dict)