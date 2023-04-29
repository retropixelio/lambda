import dataclasses
from typing import Dict
import json

from utils.dataclass_classmethods import FromDictMixin

@dataclasses.dataclass
class Headers(FromDictMixin):
    authorization: str = None
    Content_Type: str = None

@dataclasses.dataclass
class Request(FromDictMixin):
    resource: str = None
    path: str = None
    httpMethod: str = None
    headers: Headers = None
    queryStringParameters: Dict[str, str] = dataclasses.field(default_factory=dict)
    multiValueQueryStringParameters: Dict[str, str] = dataclasses.field(default_factory=dict)
    body: str = None

    def json(self):
        return json.loads(self.body)
    
@dataclasses.dataclass
class Connected(FromDictMixin):
    eventType: str = None
    clientId: str = None
    device: str = None