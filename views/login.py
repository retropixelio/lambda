from utils.api_view import APIView

from request_objects.login import Login

from repos.firebase import FirebaseRepository

from use_cases.login import LoginUseCase

class LoginView(APIView):
    def post(self):
        request_object = Login.from_dict(self.request.json())
        firebase_repo = FirebaseRepository(self.user)
        use_case = LoginUseCase(firebase_repo)
        response = use_case.execute(request_object)
        return response