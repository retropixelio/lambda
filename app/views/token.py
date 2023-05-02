from utils.api_view import APIView

from use_cases.token import TokenUseCase

class TokenView(APIView):
    def post(self):
        use_case = TokenUseCase()
        response = use_case.execute(self.request.body)
        return response