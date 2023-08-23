from utils.api_view import APIView, TokenAuthentication

from repos.firebase import FirebaseRepository

from use_cases.query import QueryUseCase

from request_objects.query import Query

class QueryView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self):
        request_obj = Query.from_dict(self.request.query_string_parameters)
        firebase_repo = FirebaseRepository(self.user)
        use_case = QueryUseCase(firebase_repo)
        response = use_case.execute(request_obj)
        return response