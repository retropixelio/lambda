from utils.api_view import APIView

from repos.firebase import FirebaseRepository

from use_cases.auth import AuthUseCase, PostAuthUseCase

class AuthView(APIView):
    def get(self):
        use_case = AuthUseCase()
        response = use_case.execute()
        return response
    
    def post(self):
        firebase_repo = FirebaseRepository(None)
        use_case = PostAuthUseCase(firebase_repo)
        response = use_case.execute(
            self.request.body, 
            self.request.queryStringParameters
        )
        return response