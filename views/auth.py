from utils.api_view import APIView

from use_cases.auth import AuthUseCase, PostAuthUseCase

class AuthView(APIView):
    def get(self):
        use_case = AuthUseCase()
        response = use_case.execute()
        return response
    
    def post(self):
        use_case = PostAuthUseCase()
        response = use_case.execute(
            self.request.body, 
            self.request.queryStringParameters
        )
        return response