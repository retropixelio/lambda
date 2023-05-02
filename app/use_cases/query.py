from repos.firebase import FirebaseRepository
from repos.response import response_object

from request_objects.query import Query

class QueryUseCase:
    def __init__(self, firebase: FirebaseRepository):
        self.__firebase = firebase

    def execute(self, args: Query):
        response = self.__firebase.get_device(args.device)
        return response_object(response.to_dict(), 200)