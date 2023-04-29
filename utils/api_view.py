from domain.event import Request
from domain.authentication import Token
from repos.response import response_object

class TokenAuthentication:
    def authenticate(self, request: Request):
        try:
            token = Token(token=request.headers.authorization[7:])
            user = token.decode()
            return user.user
        except:
            return False

class APIView:
    authentication_classes = []

    def __init__(self, request: Request):
        self.request = request
        self.user = None

    def execute(self):
        for auth in self.authentication_classes:
            user = auth().authenticate(self.request)
            if user:
                self.user = user
            else:
                return response_object({}, 401)
        if self.request.httpMethod == 'OPTIONS':
            return{
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                }
            }
        if self.request.httpMethod.lower() in dir(self):
            function = getattr(self, self.request.httpMethod.lower())
            return function()
        return response_object({}, 405)