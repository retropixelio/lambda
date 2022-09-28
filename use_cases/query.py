from firebase_admin import db
import jwt

from conf import settings
from repos.response import response_object

def query_get(headers, args):
    token = headers.get('authorization')[7:]
    user = jwt.decode(token, settings.SECRET, algorithms=["HS256"])
    if user.get("token_type") == "access":
        device = args.get('device')
        ref = db.reference(f'Devices/{device}')
        return response_object(ref.get(), 200)
    return response_object({}, 401)